# blockchain.py
import time
import hashlib
import json

def now_str():
    """Return current local time as a readable string."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions  # list of dicts
        self.timestamp = timestamp        # string
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
    def __init__(self, difficulty=2):
        # genesis block with string timestamp
        self.chain = [Block(0, [], now_str(), "0")]
        self.pending_transactions = []
        self.difficulty = difficulty
        self.money_balance = 0.0
        self.food_balance = {}  # {food_type: qty}

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        # ensure timestamp exists and is string
        if "timestamp" not in transaction or not transaction["timestamp"]:
            transaction["timestamp"] = now_str()
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return False

        # ensure timestamps exist for each pending tx
        for tx in self.pending_transactions:
            if "timestamp" not in tx or not tx["timestamp"]:
                tx["timestamp"] = now_str()

        # update balances (this may add 'status' to tx if rejected)
        for tx in self.pending_transactions:
            self._update_balances(tx)

        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),
            timestamp=now_str(),
            previous_hash=self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return True

    def _update_balances(self, tx):
        t = tx.get("type")
        if t == "money_donation":
            self.money_balance += float(tx.get("amount", 0))
        elif t == "food_donation":
            ft = tx.get("food_type")
            q = int(tx.get("quantity", 0))
            self.food_balance[ft] = self.food_balance.get(ft, 0) + q
        elif t == "money_request":
            amt = float(tx.get("amount", 0))
            if amt <= self.money_balance:
                self.money_balance -= amt
            else:
                tx["status"] = "rejected_insufficient_money"
        elif t == "food_request":
            ft = tx.get("food_type")
            q = int(tx.get("quantity", 0))
            if self.food_balance.get(ft, 0) >= q:
                self.food_balance[ft] -= q
            else:
                tx["status"] = "rejected_insufficient_food"

    def get_all_transactions(self):
        history = []
        # skip genesis
        for block in self.chain[1:]:
            for tx in block.transactions:
                # ensure timestamp is string (defensive)
                if "timestamp" not in tx or not tx["timestamp"]:
                    tx["timestamp"] = now_str()
                history.append(tx)
        # also include any pending ones (should be empty if you mine immediately)
        for tx in self.pending_transactions:
            if "timestamp" not in tx or not tx["timestamp"]:
                tx["timestamp"] = now_str()
            history.append(tx)
        return history

    # convenience helpers
    def add_money_donation(self, amount):
        self.add_transaction({
            "type": "money_donation",
            "amount": float(amount),
            "timestamp": now_str()
        })

    def add_food_donation(self, food_type, quantity):
        self.add_transaction({
            "type": "food_donation",
            "food_type": food_type,
            "quantity": int(quantity),
            "timestamp": now_str()
        })

    def request_money(self, amount):
        self.add_transaction({
            "type": "money_request",
            "amount": float(amount),
            "timestamp": now_str()
        })

    def request_food(self, food_type, quantity):
        self.add_transaction({
            "type": "food_request",
            "food_type": food_type,
            "quantity": int(quantity),
            "timestamp": now_str()
        })
