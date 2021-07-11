# JWT on NASDAQ
import requests
import hashlib

mybearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2RhbWwuY29tL2xlZGdlci1hcGkiOnsibGVkZ2VySWQiOiJkZW1vIiwiYXBwbGljYXRpb25JZCI6IkhUVFAtSlNPTi1BUEktR2F0ZXdheSIsImFjdEFzIjpbIk5BU0RBUSJdfX0.fRB8XzB-xam9uQXzQbfH9BwxMlGdsFIrudMf1CbU8zQ"
myheaders = {'Authorization': 'Bearer %s' % mybearer}
url_exercise = 'http://localhost:7575/v1/exercise'
url_getAllContracts = 'http://localhost:7575/v1/query'

# lock asset

qty = input("Input the quantity of shares to be locked: ")

secret = input("Input the secret to lock the asset: ")
# secret = 'ce6d0353ec09e8103c8f6b364a4d70f4a8cb7a5093c7f3b90bce5e44ceec7436'
secret_b = str.encode(secret)
hashlock = hashlib.sha256(secret_b).hexdigest()

data = {
  "templateId": "Htlc:Shares",
  "key": {
    "_1": "NASDAQ",
    "_2": "AAPL",
    "_3": "Alice"
  },
  "choice": "Lock",
  "argument": {
    "target": "Bob",
    "quantityToBeLocked": qty, # 10 shares
    "locktime": "120", # 2 minutes
    "hashlock": hashlock
  }
}

res = requests.post(url_exercise, json=data, headers=myheaders)

res_json = res.json()
if res_json['status'] == 200:
  print("Alice's asset is locked. Here is the HTLC contract %s in daml ledger" % res_json['result']['events'][2]['created']['contractId'])
  print()
  print("*** Hashlock *** %s" % hashlock)
else:
  print("Something wrong in locking asset.")

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
