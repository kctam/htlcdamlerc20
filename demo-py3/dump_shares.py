# JWT on NASDAQ
import requests

mybearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2RhbWwuY29tL2xlZGdlci1hcGkiOnsibGVkZ2VySWQiOiJkZW1vIiwiYXBwbGljYXRpb25JZCI6IkhUVFAtSlNPTi1BUEktR2F0ZXdheSIsImFjdEFzIjpbIk5BU0RBUSJdfX0.fRB8XzB-xam9uQXzQbfH9BwxMlGdsFIrudMf1CbU8zQ"
myheaders = {'Authorization': 'Bearer %s' % mybearer}
url_getAllContracts = 'http://localhost:7575/v1/query'

print ("--- dump all Shares contract ---")

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
