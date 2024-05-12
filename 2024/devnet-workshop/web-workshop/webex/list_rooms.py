import os
import requests


access_token = os.getenv("WEBEX_API_TOKEN")

url = 'https://webexapis.com/v1/rooms'

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params = {'max': '100'}
res = requests.get(url, headers=headers, params=params)

print(res.text)
