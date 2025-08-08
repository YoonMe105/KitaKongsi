import hashlib
import json
import time

class DonationBlock:
    def __init__(self, index, timestamp, donation_type, sender, receiver, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.donation_type = donation_type  # "food" or "money"
        self.sender = sender
        self.receiver = receiver
        self.data = data  # Quantity or amount
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "donation_type": self.donation_type,
            "sender": self.sender,
            "receiver": self.receiver,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "donation_type": self.donation_type,
            "sender": self.sender,
            "receiver": self.receiver,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = DonationBlock(
            index=0,
            timestamp=time.time(),
            donation_type="genesis",
            sender="N/A",
            receiver="N/A",
            data="Genesis Block",
            previous_hash="0"
        )
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, donation_type, sender, receiver, data):
        last_block = self.get_last_block()
        new_block = DonationBlock(
            index=len(self.chain),
            timestamp=time.time(),
            donation_type=donation_type,
            sender=sender,
            receiver=receiver,
            data=data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def to_list(self):
        return [block.to_dict() for block in self.chain]
