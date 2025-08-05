import hashlib
import time
import json
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Just a basic example
        genesis_block = {
            'index': 0,
            'data': 'Genesis Block',
            'previous_hash': '0'
        }
        self.chain.append(genesis_block)

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = {
            'index': len(self.chain),
            'data': data,
            'previous_hash': hash(str(last_block))
        }
        self.chain.append(new_block)

