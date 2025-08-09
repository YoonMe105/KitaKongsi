import time
import hashlib
import json

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions  # list of dicts
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 4
        self.money_balance = 0.0
        self.food_balance = {}  # {food_type: quantity}

    def create_genesis_block(self):
        return Block(0, [], time.time(), "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            print("No transactions to mine.")
            return False

        # Update balances before mining
        for tx in self.pending_transactions:
            self._update_balances(tx)

        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            timestamp=time.time(),
            previous_hash=self.get_latest_block().hash
        )
        print(f"Mining block #{new_block.index} with {len(new_block.transactions)} transactions...")
        new_block.mine_block(self.difficulty)
        print(f"Block mined with hash: {new_block.hash}")

        self.chain.append(new_block)
        self.pending_transactions = []
        return True

    def _update_balances(self, tx):
        t = tx.get("type")
        if t == "money_donation":
            amount = tx.get("amount", 0)
            self.money_balance += amount

        elif t == "food_donation":
            food_type = tx.get("food_type")
            quantity = tx.get("quantity", 0)
            if food_type not in self.food_balance:
                self.food_balance[food_type] = 0
            self.food_balance[food_type] += quantity

        elif t == "money_request":
            amount = tx.get("amount", 0)
            if amount <= self.money_balance:
                self.money_balance -= amount
            else:
                print("Warning: Money request exceeds balance. Ignored.")

        elif t == "food_request":
            food_type = tx.get("food_type")
            quantity = tx.get("quantity", 0)
            if food_type in self.food_balance and quantity <= self.food_balance[food_type]:
                self.food_balance[food_type] -= quantity
            else:
                print("Warning: Food request invalid or insufficient quantity. Ignored.")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]

            if current.hash != current.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False

            if current.previous_hash != prev.hash:
                print(f"Invalid previous hash linkage at block {i}")
                return False

        return True

    # Convenience methods for transactions

    def add_money_donation(self, amount):
        if amount <= 0:
            raise ValueError("Donation amount must be positive")
        tx = {
            "type": "money_donation",
            "amount": amount,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.add_transaction(tx)

    def add_food_donation(self, food_type, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        tx = {
            "type": "food_donation",
            "food_type": food_type,
            "quantity": quantity,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.add_transaction(tx)

    def request_money(self, amount):
        if amount <= 0:
            raise ValueError("Request amount must be positive")
        tx = {
            "type": "money_request",
            "amount": amount,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.add_transaction(tx)

    def request_food(self, food_type, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        tx = {
            "type": "food_request",
            "food_type": food_type,
            "quantity": quantity,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.add_transaction(tx)
