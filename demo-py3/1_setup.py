# JWT on NASDAQ
import requests

mybearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2RhbWwuY29tL2xlZGdlci1hcGkiOnsibGVkZ2VySWQiOiJkZW1vIiwiYXBwbGljYXRpb25JZCI6IkhUVFAtSlNPTi1BUEktR2F0ZXdheSIsImFjdEFzIjpbIk5BU0RBUSJdfX0.fRB8XzB-xam9uQXzQbfH9BwxMlGdsFIrudMf1CbU8zQ"
myheaders = {'Authorization': 'Bearer %s' % mybearer}
url_allocateParties = 'http://localhost:7575/v1/parties/allocate'
url_create = 'http://localhost:7575/v1/create'
url_exercise = 'http://localhost:7575/v1/exercise'
url_getAllContracts = 'http://localhost:7575/v1/query'

# allocate party
print("--- allocate parties ---")
parties = ["NASDAQ","Alice","Bob"]
for party in parties:
  data = {
    "identifierHint": party,
    "displayName": party
  }
  res = requests.post(url_allocateParties, json=data, headers=myheaders)
  res_json = res.json()
  if res_json['status'] == 200:
    print("Account %s created" % party)
  else:
    print("Something wrong in party allocation.")

# create Shares for parties
print("--- allocate shares for parties ---")
allocations = [("Alice","100"),("Bob","0")]
for (owner, quantity) in allocations:
  data = {
    "templateId": "Htlc:Shares",
    "payload": {
      "exchange": "NASDAQ",
      "owner": owner,
      "ticker": "AAPL",
      "quantity": quantity
    }
  }
  res = requests.post(url_create, json=data, headers=myheaders)
  res_json = res.json()
  if res_json['status'] == 200:
    print("%s of AAPL are allocated to %s." % (quantity,owner))
  else:
    print("Something wrong in share allocation.")

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
