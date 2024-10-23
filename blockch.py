# importing the required libraries
import hashlib
import json
from time import time

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

block_chain = Block_chain()
transaction1 = block_chain.newTransaction("Satoshi", "Alex", '10 BTC')
transaction2 = block_chain.newTransaction("Alex", "Satoshi", '2 BTC')
transaction3 = block_chain.newTransaction("Satoshi", "James", '10 BTC')
block_chain.newBlock(10123)

transaction4 = block_chain.newTransaction("Alex", "Lucy", '2 BTC')
transaction5 = block_chain.newTransaction("Lucy", "Justin", '1 BTC')
transaction6 = block_chain.newTransaction("Justin", "Alex", '1 BTC')
block_chain.newBlock(10384)

# Printing the blockchain data in an organized manner
print("Blockchain:")
for block in block_chain.chain:
    print("\nBlock No:", block['index'])
    print("Timestamp:", block['timestamp'])
    print("Proof:", block['proof'])
    print("Previous Hash:", block['previous_hash'])
    print("Transactions:")
    for transaction in block['transactions']:
        print("  - Sender:", transaction['sender'])
        print("    Recipient:", transaction['recipient'])
        print("    Amount:", transaction['amount'])
    print("-" * 30)
