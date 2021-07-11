from web3 import Web3
import requests

# use ganache-cli -m abcdef to bring up a local ethereum network
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
bob = "0xDb2eD3D31565183CC4e644d04aCdAcd3d1430523"

htlcerc20_abi = [ { "anonymous": False, "inputs": [ { "indexed": True, "internalType": "bytes32", "name": "contractId", "type": "bytes32" }, { "indexed": True, "internalType": "address", "name": "sender", "type": "address" }, { "indexed": True, "internalType": "address", "name": "receiver", "type": "address" }, { "indexed": False, "internalType": "address", "name": "tokenContract", "type": "address" }, { "indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256" }, { "indexed": False, "internalType": "bytes32", "name": "hashlock", "type": "bytes32" }, { "indexed": False, "internalType": "uint256", "name": "timelock", "type": "uint256" } ], "name": "HTLCERC20New", "type": "event" }, { "anonymous": False, "inputs": [ { "indexed": True, "internalType": "bytes32", "name": "contractId", "type": "bytes32" } ], "name": "HTLCERC20Refund", "type": "event" }, { "anonymous": False, "inputs": [ { "indexed": True, "internalType": "bytes32", "name": "contractId", "type": "bytes32" } ], "name": "HTLCERC20Withdraw", "type": "event" }, { "inputs": [ { "internalType": "bytes32", "name": "_contractId", "type": "bytes32" } ], "name": "getContract", "outputs": [ { "internalType": "address", "name": "sender", "type": "address" }, { "internalType": "address", "name": "receiver", "type": "address" }, { "internalType": "address", "name": "tokenContract", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "bytes32", "name": "hashlock", "type": "bytes32" }, { "internalType": "uint256", "name": "timelock", "type": "uint256" }, { "internalType": "bool", "name": "withdrawn", "type": "bool" }, { "internalType": "bool", "name": "refunded", "type": "bool" }, { "internalType": "string", "name": "preimage", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_receiver", "type": "address" }, { "internalType": "bytes32", "name": "_hashlock", "type": "bytes32" }, { "internalType": "uint256", "name": "_timelock", "type": "uint256" }, { "internalType": "address", "name": "_tokenContract", "type": "address" }, { "internalType": "uint256", "name": "_amount", "type": "uint256" } ], "name": "newContract", "outputs": [ { "internalType": "bytes32", "name": "contractId", "type": "bytes32" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "_contractId", "type": "bytes32" } ], "name": "refund", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "_contractId", "type": "bytes32" }, { "internalType": "string", "name": "_preimage", "type": "string" } ], "name": "withdraw", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" } ]
token_abi = [{"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"uint256","name":"_totalsupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]

# read htlc-erc contract ID
htlcerc20_file = open("htlc-erc20-contractid", "r")
htlcerc20_id = htlcerc20_file.read()
htlcerc20_contract = w3.eth.contract(
    address=htlcerc20_id,
    abi=htlcerc20_abi
)

# read USD token ID
token_file = open("token-usd-contractid", "r")
token_usd_id = token_file.read()
token_usd_contract = w3.eth.contract(
    address=token_usd_id,
    abi=token_abi
)

# retrieves preimage from Alice's input
contractid = input("Bob's USD contract ID: ")
res = htlcerc20_contract.functions.getContract(contractid).call()
preimage = res[8]
print("Alice's secret: %s " % preimage)

# unlock shares in daml ledger

mybearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2RhbWwuY29tL2xlZGdlci1hcGkiOnsibGVkZ2VySWQiOiJkZW1vIiwiYXBwbGljYXRpb25JZCI6IkhUVFAtSlNPTi1BUEktR2F0ZXdheSIsImFjdEFzIjpbIk5BU0RBUSJdfX0.fRB8XzB-xam9uQXzQbfH9BwxMlGdsFIrudMf1CbU8zQ"
myheaders = {'Authorization': 'Bearer %s' % mybearer}
url_exercise = 'http://localhost:7575/v1/exercise'
url_fetch = 'http://localhost:7575/v1/fetch'
url_getAllContracts = 'http://localhost:7575/v1/query'

request_id = input("Enter HTLC in demal for withdrawing asset: ")

data = {
  "contractId": request_id
}

res = requests.post(url_fetch, json=data, headers=myheaders)

res_json = res.json()
if res_json['status'] == 200:
  print("Record fetched")
  hashlock = res_json['result']['payload']['hashlock']
else:
  print("Record not found.")
  exit()

data = {
  "templateId": "Htlc:Htlc",
  "contractId": request_id,
  "choice": "Withdraw",
  "argument": {
    "secret": preimage
  }
}

res = requests.post(url_exercise, json=data, headers=myheaders)

res_json = res.json()
if res_json['status'] == 200:
  print("Asset unlocked.")
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

