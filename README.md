# htlcdamlerc20
Hashed Timelock Contract (HTLC) demonstration for assets in daml ledger and ERC20 token.

The HTLC used in this demonstration is from [here](https://github.com/chatch/hashed-timelock-contract-ethereum). Modification is done: type for preimage is changed from bytes32 to string.

## Prerequisite
* ganache-cli
* daml sdk 1.14.0
* python3
* python3 web3 library

## Demonstration steps

### Step 1: Preparation

We need several terminals for setting up the environment.

Daml Sandbox
```
./startSandbox.sh
```

Daml JSON-API
```
./startJSONAPI.sh
```

Ethereum (ganache-cli)
```
ganache-cli -m abcdef
```
Note: Use this mnemonic as the account information is hardcoded.

Event listener
```
cd demo-py3
python3 e99_eventlistener.py
```

### Step 2: Deploy contracts and setup token balances for both Alice and Bob

It is hardcoded with USD1,000 for both accounts

Open a terminal for all commands from now on.

```
cd demo-py3
python3 1a_deploy_eth_contracts.py
```

### Step 3: Setup Shares in daml ledger

It is hardcoded with 100 shares of AAPL in Alice's account. None in Bob's.
```
python3 1_setup.py
```

### Step 4: Alice locks some shares (e.g. 10 shares)
```
python3 2_alice_lock_shares_daml.py
```
Alice specifies the number of shares to be locked, and a secret that only Alice knows.

Note that two pieces of information are returned
* HTLC contract in Daml ledger for Alice's asset, which will be used when Bob's withdrawal or Alice's refunding
* Hashlock value: which will be used in Step 5 when Bob locks his asset in Ethereum.

### Step 5: Bob locks his USD (e.g. USD150)
```
python3 3_bob_locks_USD_eth.py
```
When asked, use the *Hashlock* value obtained in Step 4. The HTLC contract ID for Bob's asset in Ethereum is returned in the event listener terminal.

### Step 6: Alice unlocks Bob's USD asset in Ethereum
```
python3 4_alice_withdraw_USD_eth.py
```
When asked, Alice first enters the HTLC contract for Bob's asset (in event listerner terminal of Step 5) and her secret. The result shows that the amount of USD is now in Alice's account.

### Step 7: Bob unlocks Alice's Shares in Daml ledger
```
python3 5_bob_withdraw_shares_daml.py
```
When asked, Bob first enters his HTLC contract (in event listener terminal of Step 5). Then he obtains the secret Alice leaves in the record. Now Bob enters Alice's HTLC in the daml ledger (Step 4). The result shows that the sahres is now in Bob's account.

### Alternatively, both sides refund

Rather than swapping (Step 6 and 7), after time interval expires (2 minutes), both sides can get refund their assets.
```
python3 6a_alice_refund_shares_daml.py
```
Alice provides her HTLC in the daml ledger (Step 4) and gets back the shares.

```
python3 6b_bob_refund_USD_eth.py
```
Bob provides his HTLC in the Ethereum (in event listerner of Step 5) and gets back his USD tokens.
