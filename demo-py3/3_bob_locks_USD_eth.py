from web3 import Web3
import time
import hashlib

# use ganache-cli -m abcdef to bring up a local ethereum network
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
bob = "0xDb2eD3D31565183CC4e644d04aCdAcd3d1430523"
bob_privkey = "0x8a32f3bd875cfda851b50fbec2b7395844c2c8be741a3a3d537808d6357a745a"

htlcerc20_abi = htlcerc20_abi = [ { "anonymous": False, "inputs": [ { "indexed": True, "internalType": "bytes32", "name": "contractId", "type": "bytes32" }, { "indexed": True, "internalType": "address", "name": "sender", "type": "address" }, { "indexed": True, "internalType": "address", "name": "receiver", "type": "address" }, { "indexed": False, "internalType": "address", "name": "tokenContract", "type": "address" }, { "indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256" }, { "indexed": False, "internalType": "bytes32", "name": "hashlock", "type": "bytes32" }, { "indexed": False, "internalType": "uint256", "name": "timelock", "type": "uint256" } ], "name": "HTLCERC20New", "type": "event" }, { "anonymous": False, "inputs": [ { "indexed": True, "internalType": "bytes32", "name": "contractId", "type": "bytes32" } ], "name": "HTLCERC20Refund", "type": "event" }, { "anonymous": False, "inputs": [ { "indexed": True, "internalType": "bytes32", "name": "contractId", "type": "bytes32" } ], "name": "HTLCERC20Withdraw", "type": "event" }, { "inputs": [ { "internalType": "bytes32", "name": "_contractId", "type": "bytes32" } ], "name": "getContract", "outputs": [ { "internalType": "address", "name": "sender", "type": "address" }, { "internalType": "address", "name": "receiver", "type": "address" }, { "internalType": "address", "name": "tokenContract", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "bytes32", "name": "hashlock", "type": "bytes32" }, { "internalType": "uint256", "name": "timelock", "type": "uint256" }, { "internalType": "bool", "name": "withdrawn", "type": "bool" }, { "internalType": "bool", "name": "refunded", "type": "bool" }, { "internalType": "string", "name": "preimage", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_receiver", "type": "address" }, { "internalType": "bytes32", "name": "_hashlock", "type": "bytes32" }, { "internalType": "uint256", "name": "_timelock", "type": "uint256" }, { "internalType": "address", "name": "_tokenContract", "type": "address" }, { "internalType": "uint256", "name": "_amount", "type": "uint256" } ], "name": "newContract", "outputs": [ { "internalType": "bytes32", "name": "contractId", "type": "bytes32" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "_contractId", "type": "bytes32" } ], "name": "refund", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "_contractId", "type": "bytes32" }, { "internalType": "string", "name": "_preimage", "type": "string" } ], "name": "withdraw", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" } ]
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

price = input("Input price to pay: ")
price = int(price)

# bob approves htlcerc20 to collect 90 tokens
nonce = w3.eth.getTransactionCount(bob)
tx = token_usd_contract.functions.approve(
    htlcerc20_id,
    price
).buildTransaction({
    'gas': 70000,
    'from': bob,
    'nonce': nonce
})
signed_tx = w3.eth.account.signTransaction(tx, private_key=bob_privkey)
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
w3.eth.waitForTransactionReceipt(tx_hash)
print("Allowance approved.")

# prepare USD locking for 2 minutes
alice = "0x2b55CD0D2a47044c4C1C2295eA5317c4eB7C8ED2"
hashlock = input("Input hash (in string): ")

time = int(time.time())
time_2min = time + 120

nonce = w3.eth.getTransactionCount(bob)
tx = htlcerc20_contract.functions.newContract(
    alice,
    hashlock,
    time_2min,
    token_usd_id,
    price
).buildTransaction({
    'gas': 700000,
    'from': bob,
    'nonce': nonce
})

signed_tx = w3.eth.account.signTransaction(tx, private_key=bob_privkey)
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
w3.eth.waitForTransactionReceipt(tx_hash)

alice_balance = token_usd_contract.functions.balanceOf(alice).call()
bob_balance = token_usd_contract.functions.balanceOf(bob).call()
print()
print("Balance:")
print("Alice: USD %s" % alice_balance)
print("Bob: USD %s" % bob_balance)