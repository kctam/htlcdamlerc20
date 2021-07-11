from web3 import Web3
import asyncio

# use ganache-cli -m abcdef to bring up a local ethereum network
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

htlcerc20_abi = [ { "anonymous": False, "inputs": [ { "indexed": True, "internalType": "bytes32", "name": "contractId", "type": "bytes32" }, { "indexed": True, "internalType": "address", "name": "sender", "type": "address" }, { "indexed": True, "internalType": "address", "name": "receiver", "type": "address" }, { "indexed": False, "internalType": "address", "name": "tokenContract", "type": "address" }, { "indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256" }, { "indexed": False, "internalType": "bytes32", "name": "hashlock", "type": "bytes32" }, { "indexed": False, "internalType": "uint256", "name": "timelock", "type": "uint256" } ], "name": "HTLCERC20New", "type": "event" }, { "anonymous": False, "inputs": [ { "indexed": True, "internalType": "bytes32", "name": "contractId", "type": "bytes32" } ], "name": "HTLCERC20Refund", "type": "event" }, { "anonymous": False, "inputs": [ { "indexed": True, "internalType": "bytes32", "name": "contractId", "type": "bytes32" } ], "name": "HTLCERC20Withdraw", "type": "event" }, { "inputs": [ { "internalType": "bytes32", "name": "_contractId", "type": "bytes32" } ], "name": "getContract", "outputs": [ { "internalType": "address", "name": "sender", "type": "address" }, { "internalType": "address", "name": "receiver", "type": "address" }, { "internalType": "address", "name": "tokenContract", "type": "address" }, { "internalType": "uint256", "name": "amount", "type": "uint256" }, { "internalType": "bytes32", "name": "hashlock", "type": "bytes32" }, { "internalType": "uint256", "name": "timelock", "type": "uint256" }, { "internalType": "bool", "name": "withdrawn", "type": "bool" }, { "internalType": "bool", "name": "refunded", "type": "bool" }, { "internalType": "string", "name": "preimage", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "_receiver", "type": "address" }, { "internalType": "bytes32", "name": "_hashlock", "type": "bytes32" }, { "internalType": "uint256", "name": "_timelock", "type": "uint256" }, { "internalType": "address", "name": "_tokenContract", "type": "address" }, { "internalType": "uint256", "name": "_amount", "type": "uint256" } ], "name": "newContract", "outputs": [ { "internalType": "bytes32", "name": "contractId", "type": "bytes32" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "_contractId", "type": "bytes32" } ], "name": "refund", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "bytes32", "name": "_contractId", "type": "bytes32" }, { "internalType": "string", "name": "_preimage", "type": "string" } ], "name": "withdraw", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "nonpayable", "type": "function" } ]

# read htlc-erc contract ID
htlcerc20_file = open("htlc-erc20-contractid", "r")
htlcerc20_id = htlcerc20_file.read()
htlcerc20_contract = w3.eth.contract(
  address=htlcerc20_id,
  abi=htlcerc20_abi
)

def handle_event(event):
  print("Contract ID on HTLC: %s " % event['args']['contractId'].hex())

async def log_loop(event_filter, poll_interval):
  while True:
    for event in event_filter.get_new_entries():
      handle_event(event)
    await asyncio.sleep(poll_interval)

def main():
  event_filter = htlcerc20_contract.events.HTLCERC20New.createFilter(fromBlock='latest')
  loop = asyncio.get_event_loop()
  try:
    loop.run_until_complete(
      asyncio.gather(
        log_loop(event_filter, 2)
      )
    )
  finally:
    loop.close()

if __name__ == "__main__":
  main()