import json
import csv
import requests
from datetime import date

url = "https://certificationapi.oshwa.org/api/projects"

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <Token>'
}

response = requests.request("GET", url, headers=headers, data=payload)

data = json.loads(response.text.encode('utf8'))
for element in data:
    element.pop('publicContact', None)
    element.pop('previousVersions', None)
    element.pop('citations', None)

with open('oshwa_api_' + str(date.today()) + '.csv', 'w',encoding="utf-8") as f:
    writer = csv.writer(f,quoting=csv.QUOTE_ALL)
    writer.writerow(["UID","Creator","Country","Project Name","Website","Version","Description","Primary Types","Additional Types","Documentation","Hardware License","Software License","Documentation License","Certification Date"])
    for row in data:
        writer.writerow(row.values())
