import requests, json
from datetime import datetime
from urllib import parse as urltool

from akamai.edgegrid import EdgeGridAuth
from matplotlib import pyplot as plt
#from matplotlib import ticker as ticker
from matplotlib import dates as mdates

import akamai_api, uploadimg

session = requests.Session()
session.auth = EdgeGridAuth(
    client_token  = akamai_api.client_token,
    client_secret = akamai_api.client_secret,
    access_token  = akamai_api.access_token
)

dateformat = "%Y-%m-%dT%H:%M:%SZ"

headers = {"Content-Type": "application/json"}

body = {
        "objectType": "cpcode",
        "objectIds": [],
        "metrics": [
            "edgeBitsPerSecond",
            "midgressBitsPerSecond",
            "originBitsPerSecond",
            "bytesOffload"
        ]
}



def TrafficImage(cpcode: str, start: datetime, end: datetime):

    url = akamai_api.host + "/reporting-api/v1/reports/todaytraffic-by-time/versions/1/report-data?start={{start}}&end={{end}}&interval=FIVE_MINUTES"
    if akamai_api.accountSwitchKey != "":
        url = url + "&accountSwitchKey=" + urltool.quote(akamai_api.accountSwitchKey)
    

    start_time = urltool.quote(start.strftime(dateformat))
    end_time = urltool.quote(end.strftime(dateformat))
    url = url.replace("{{start}}", start_time)
    url = url.replace("{{end}}", end_time)

    cpcodes = [].append(cpcode)
    body["objectIds"] = cpcodes

    response = session.post(url, headers=headers, data = json.dumps(body))
    print(url)
    print(response.text)

    if response.status_code == 200:

    #with open("data.json") as input_data:
        raw_data = str(response.text)
        data = json.loads(raw_data.replace("N/A", "0.00"))
        #data = json.load(input_data)
        pretty = json.dumps(data, indent=2)
        print(pretty)

        plt_datetime =[]
        plt_edgebits= []
        plt_midbits = []
        plt_originbits = []


        for item in data["data"]:
            plt_datetime.append(datetime.strptime(item["startdatetime"], "%Y-%m-%dT%H:%M:%SZ"))
            plt_edgebits.append(float(item["edgeBitsPerSecond"])/1000/1000)
            plt_midbits.append(float(item["midgressBitsPerSecond"])/1000/1000)
            plt_originbits.append(float(item["originBitsPerSecond"])/1000/1000)

        plt.plot(plt_datetime, plt_edgebits, label="Edge Traffic", color="green")
        plt.plot(plt_datetime, plt_midbits, label="Midgress Traffic", color="purple")
        plt.plot(plt_datetime, plt_originbits, label="Origin Traffic", color="orange")

        dateFormat = mdates.DateFormatter("%m/%d %H:%M")
        plt.gca().xaxis.set_major_formatter(dateFormat)

        plt.ylabel("Bandwidth MBit/s")
        plt.title("Traffic by Time of cpcode " + cpcode)
        plt.savefig('akamai.png')
        plt.legend()

        uploadimg.upload('akamai.png')

        # edge_max = max(plt_edgebits)
        # max_idx = plt_edgebits.index(edge_max)
        # max_position=plt_datetime[max_idx]
        #plt.annotate("Peak: " + str(round(edge_max, 2)) + "Mbps", xy=(max_position, edge_max), xytext=(max_position, edge_max + 5))
        #plt.show()



if __name__ == '__main__':
    start = datetime.strptime("2023-09-11T13:00:00Z", dateformat)
    end = datetime.strptime("2023-09-11T20:00:00Z", dateformat)

    TrafficImage("1417433", start, end)
