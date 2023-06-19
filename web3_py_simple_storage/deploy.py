from solcx import compile_standard
from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect to ganache
w3 = Web3(
    Web3.HTTPProvider("https://sepolia.infura.io/v3/cbf22d99829440379e04cbe205c5c999")
)
chain_id = 11155111
my_address = "0xbe89AF2Ae5c9E9422609a108eE8995226C0eb4D4"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get latest transaction
nonce = w3.eth.get_transaction_count(my_address)


# 1. Build the contract deploy transaction
transaction = SimpleStorage.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# 2. Sign the transaction
print("Deploying Contract...")
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# 3. Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed")

# working with contract, always need contract address , contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call -> Simulate making the call and getting a return value
# transact -> actually make a state change

# initial value of number
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")

store_txn = simple_storage.functions.store(15).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key=private_key)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)
print("Updated")

print(simple_storage.functions.retrieve().call())
