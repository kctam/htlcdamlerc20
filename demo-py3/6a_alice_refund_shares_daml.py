# JWT on NASDAQ
import requests

mybearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2RhbWwuY29tL2xlZGdlci1hcGkiOnsibGVkZ2VySWQiOiJkZW1vIiwiYXBwbGljYXRpb25JZCI6IkhUVFAtSlNPTi1BUEktR2F0ZXdheSIsImFjdEFzIjpbIk5BU0RBUSJdfX0.fRB8XzB-xam9uQXzQbfH9BwxMlGdsFIrudMf1CbU8zQ"
myheaders = {'Authorization': 'Bearer %s' % mybearer}
url_exercise = 'http://localhost:7575/v1/exercise'
url_fetch = 'http://localhost:7575/v1/fetch'
url_getAllContracts = 'http://localhost:7575/v1/query'

request_id = input("Enter HTLC in daml for withdrawing asset: ")

data = {
  "contractId": request_id
}

res = requests.post(url_fetch, json=data, headers=myheaders)

res_json = res.json()
if res_json['status'] == 200:
  print("Record fetched")
else:
  print("Record not found.")
  exit()

data = {
  "templateId": "Htlc:Htlc",
  "contractId": request_id,
  "choice": "Refund",
  "argument": {}
}

res = requests.post(url_exercise, json=data, headers=myheaders)

res_json = res.json()
if res_json['status'] == 200:
  print("Asset refunded.")
else:
  print("Something wrong.")
  exit()

# dump share balance on daml ledger
print ()
print ("--- dump all Shares contract in daml ledger ---")

res = requests.post(
  url_getAllContracts,
  json={
    "templateIds": ["Htlc:Shares"]
  },
  headers=myheaders
)

res_json = res.json()

all_shares = res_json['result']
for each in all_shares:
  print("Owner %s is holding %d shares of AAPL." % (each['payload']['owner'], int(each['payload']['quantity'])))


