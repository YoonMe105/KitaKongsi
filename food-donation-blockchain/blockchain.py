import time

class Blockchain:
    def __init__(self):
        self.money_balance = 0.0
        self.food_balance = {}

    def add_money_donation(self, amount):
        # Just add the donated amount to the money balance
        self.money_balance += amount
        print(f"DEBUG: Money donated added. New balance: {self.money_balance}")

    def add_food_donation(self, food_type, quantity, location):
        # Example: add or update food balance
        if location in self.food_balance[food_type]:
            self.food_balance[food_type][location] += quantity
        else:
            self.food_balance[food_type][location] = quantity
        print(f"DEBUG: Food donated added. {quantity} x {food_type} at {location}")


        transaction = {
            "type": "food_donation",
            "food_type": food_type,
            "quantity": quantity,
            "location": location,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)
        self.food_balance[food_type] = self.food_balance.get(food_type, 0) + quantity

    def request_money(self, amount, location):
        if amount <= self.money_balance:
            self.money_balance -= amount
            transaction = {
                "type": "money_request",
                "amount": amount,
                "location": location,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.transactions.append(transaction)
            return True
        return False

    import time

    def request_food(self, food_type, quantity, location):
        # Check if food type exists
        if food_type in self.food_balance:
            # Check if location exists under this food type
            if location in self.food_balance[food_type]:
                # Check if enough quantity available
                if quantity <= self.food_balance[food_type][location]:
                    # Deduct quantity
                    self.food_balance[food_type][location] -= quantity

                    # Record transaction
                    transaction = {
                        "type": "food_request",
                        "food_type": food_type,
                        "quantity": quantity,
                        "location": location,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    self.transactions.append(transaction)

                    return True  # Success

        return False  # Failed due to missing food_type/location or insufficient quantity

