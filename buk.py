import requests
import json

headers = {'content-type': 'application/json', 'auth_token': 'daSY92P7JMXZzFBkZCDDMYiU'}
url = 'https://tecton.buk.cl/api/v1/accounting/export?month=10&year=2019'
r = requests.get(url, headers=headers)

print(r.content)
buk = json.loads(r.content)
print(buk["data"]["76.407.152-2"]["Constructora Tecton S.p.A."])