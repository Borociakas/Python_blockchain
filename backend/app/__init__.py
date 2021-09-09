from backend.wallet.transaction import Transaction
import os
import random
import requests
import sys, getopt

from flask import Flask, json, jsonify, request
from flask_cors import CORS

from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub


app = Flask(__name__)
CORS(app, resources={ r'/*': { 'origins': 'http://localhost:3000' } })
blockchain = Blockchain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)

@app.route('/')
def route_default():
    return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/range')
def route_blockchain_range():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))

    return jsonify(blockchain.to_json()[::-1][start:end])

@app.route('/blockchain/lenght')
def route_blockchain_lenght():
    return jsonify(len(blockchain.chain))

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())

    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)

    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)

    if transaction:
        transaction.update(
            wallet, 
            transaction_data['recipient'],
            transaction_data['amount']
        )
    else:
        transaction = Transaction(
            wallet, 
            transaction_data['recipient'],
            transaction_data['amount']
        )

    pubsub.broadcast_transaction(transaction)

    return jsonify(transaction.to_json())

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({ 'address': wallet.address, 'balance': wallet.balance })

ROOT_PORT = 5000
PORT = ROOT_PORT

commandLineArgs = sys.argv[1:]

if(len(commandLineArgs) > 0):
    if(commandLineArgs[0] == "fill"):
        for i in range(15):
            blockchain.add_block([
                Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json(),
                Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json()
            ])
    else:    
        PORT = commandLineArgs[0]

app.run(port=PORT)

result = requests.get(f'http://localhost:{PORT}/blockchain')
print(f'result.json(): {result.json()}')

result_blockchain = Blockchain.from_json(result.json())

try:
    blockchain.replace_chain(result_blockchain.chain)
    print('\n--Successfully synchronized the local chain')
except Exception as e:
    print(f'\n-- Error synchronizing: {e}')

