import json
import requests
from datetime import date
import pandas as pd

url = "https://certificationapi.oshwa.org/api/projects"

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <token>'
}

response = requests.request("GET", url, headers=headers, data=payload)

pdObj = pd.read_json(response.content, orient='records')
csvData = pdObj.to_csv('oshwa_api_' + str(date.today()) + '.csv', index=False)
print("Write successful")
