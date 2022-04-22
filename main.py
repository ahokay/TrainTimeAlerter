from bs4 import BeautifulSoup as bs
import requests

url = "https://ojp.nationalrail.co.uk/service/ldbboard/dep/WCB"
webhookurl = "https://maker.ifttt.com/trigger/bitcoin/with/key/hUVRJhLAo8VbMsBmNKKQIb5hY0G1fauQQ493N-Thg8e"


def getInfo():
    r = requests.get(url)
    rsoup = bs(r.text, "html.parser")
    table = rsoup.find("tbody")
    collection = table.findAll("tr")
    output = []
    for i in collection:
        lst = []
        lst.append(getTime(i))
        lst.append(getDestination(i))
        lst.append(getArrivalTime(i))
        output.append(lst)
    notification(output)


def getTime(info):
    time = info.find("td").text
    return time


def getArrivalTime(info):
    arrival = info.find("td", {"class": "status"}).text
    return arrival


def getDestination(info):
    destination = info.find("td", {"class": "destination"}).text
    recent = ""
    while " " in destination:
        destination = destination.strip(" ")
        destination = destination.strip("\n")
        if recent == destination:
            break
        else:
            recent = destination
    destination = destination[:destination.find("\xa0")]
    return destination

def notification(output):
    string = ""
    first = True
    for line in output:
        if first:
            string += f"{line[0]}  {line[1]}  {line[2]}"
            first = False
        else:
            string += f"<br \>{line[0]}  {line[1]}  {line[2]}"
    data = {"value1": string}
    requests.post(webhookurl, data)


getInfo()