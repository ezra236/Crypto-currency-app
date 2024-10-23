# importing the required libraries
import hashlib
import json
from time import time
from flask import Flask, request, jsonify

# creating the Block_chain class
class Block_chain(object):
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        
        self.newBlock(previousHash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", the_proof=100)

    # Creating a new block listing key/value pairs of 
    # block information in a JSON object.
    # Reset the list of pending transactions & 
    # append the newest block to the chain.
    def newBlock(self, the_proof, previousHash=None):
        the_block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pendingTransactions,
            'proof': the_proof,
            'previous_hash': previousHash or self.hash(self.chain[-1]),
        }
        self.pendingTransactions = []
        self.chain.append(the_block)

        return the_block

    # Searching the blockchain for the most recent block.
    @property
    def lastBlock(self):
        return self.chain[-1]

    # Adding a transaction with relevant info to the 'blockpool' - list of pending tx's.
    def newTransaction(self, the_sender, the_recipient, the_amount):
        the_transaction = {
            'sender': the_sender,
            'recipient': the_recipient,
            'amount': the_amount
        }
        self.pendingTransactions.append(the_transaction)
        return self.lastBlock['index'] + 1

    # receiving one block. Turning it into a string, turning that into 
    # Unicode (for hashing). Hashing with SHA256 encryption, 
    # then translating the Unicode into a hexadecimal string.
    def hash(self, the_block):
        stringObject = json.dumps(the_block, sort_keys=True)
        blockString = stringObject.encode()

        rawHash = hashlib.sha256(blockString)
        hexHash = rawHash.hexdigest()

        return hexHash

# Create a Flask web application
app = Flask(__name__)
block_chain = Block_chain()

# Root route
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Blockchain API! Use /transactions/new to create a transaction, /mine to mine a block, or /chain to view the blockchain."

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # Get transaction details from the request
    values = request.get_json()
    
    # Check if the required fields are in the request
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new transaction
    index = block_chain.newTransaction(values['sender'], values['recipient'], values['amount'])
    
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    # Create a new block by mining the current pending transactions
    last_block = block_chain.lastBlock
    proof = 10123  # Placeholder proof
    previous_hash = block_chain.hash(last_block)
    
    block_chain.newBlock(proof, previous_hash)
    
    response = {
        'message': 'New Block Forged',
        'index': block_chain.lastBlock['index'],
        'transactions': block_chain.lastBlock['transactions'],
        'proof': block_chain.lastBlock['proof'],
        'previous_hash': block_chain.lastBlock['previous_hash']
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain)
    }
    return jsonify(response), 200

# Running the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
