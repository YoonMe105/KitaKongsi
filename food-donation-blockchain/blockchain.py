import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.money_balance = 0
        self.food_balance = {}
        self.create_genesis_block()

    def create_genesis_block(self):
        self.chain.append({
            "index": 0,
            "timestamp": time.time(),
            "type": "genesis",
            "data": "First block",
            "previous_hash": "0"
        })

    def add_block(self, data_type, data):
        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "type": data_type,
            "data": data,
            "previous_hash": self.chain[-1]
        }
        self.chain.append(block)

    def add_money_donation(self, amount):
        self.money_balance += amount
        self.add_block("money_donation", {"amount": amount})

    def add_food_donation(self, food_type, quantity):
        self.food_balance[food_type] = self.food_balance.get(food_type, 0) + quantity
        self.add_block("food_donation", {"type": food_type, "quantity": quantity})
