import os
import random
import requests
import sys, getopt

from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub


app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)

@app.route('/')
def route_default():
    return 'Welcome to the blockchain'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'
    blockchain.add_block(transaction_data)

    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)

    return jsonify(block.to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT

commandLineArgs = sys.argv[1:]

if(len(commandLineArgs) > 0):
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

