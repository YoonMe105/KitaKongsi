from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecret"

# Simple Blockchain class stub for demonstration
class Blockchain:
    def __init__(self):
        self.money_balance = 0.0
        self.food_balance = {}

    def add_money_donation(self, amount):
        self.money_balance += amount
        print(f"DEBUG: Money donated added. New balance: {self.money_balance}")

    def add_food_donation(self, food_type, quantity, location=None):
        if food_type in self.food_balance:
            self.food_balance[food_type] += quantity
        else:
            self.food_balance[food_type] = quantity
        print(f"DEBUG: Food donated added. {quantity} x {food_type}")

    def history():
        all_transactions = []
        for block in blockchain.chain:
            for tx in block.transactions:
                all_transactions.append(tx)
        return render_template("history.html", transactions=all_transactions)

blockchain = Blockchain()

used_codes_file = "used_codes.txt"

def load_used_codes():
    try:
        with open(used_codes_file, "r") as f:
            codes = set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        codes = set()
    return codes

def save_used_code(code):
    with open(used_codes_file, "a") as f:
        f.write(code + "\n")

used_codes = load_used_codes()

@app.route("/")
def about():
    return render_template("about.html")

@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        donation_type = request.form.get("donation_type")

        if not donation_type:
            flash("Donation type is required.", "danger")
            return redirect(url_for("donate"))

        # MONEY DONATION (no location)
        if donation_type == "money":
            amount_str = request.form.get("amount", "").strip()
            print("DEBUG: Amount entered:", repr(amount_str))

            if not amount_str:
                flash("Please enter an amount.", "danger")
                return redirect(url_for("donate"))

            try:
                amount = float(amount_str)
            except ValueError:
                flash("Please enter a valid numeric amount.", "danger")
                return redirect(url_for("donate"))

            if amount <= 0:
                flash("Please enter an amount greater than zero.", "danger")
                return redirect(url_for("donate"))

            blockchain.add_money_donation(amount)
            flash(f"Thank you for donating RM{amount:.2f}!", "success")

        # FOOD DONATION (unchanged)
        elif donation_type == "food":
            food_type = request.form.get("food_type", "").strip()
            quantity_str = request.form.get("quantity", "").strip()

            if not food_type or not quantity_str:
                flash("Please enter food type, quantity.", "danger")
                return redirect(url_for("donate"))

            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    raise ValueError
                blockchain.add_food_donation(food_type, quantity)
                flash("Thank you for donating food!", "success")
            except (ValueError, TypeError):
                flash("Please enter a valid quantity greater than zero.", "danger")

        else:
            flash("Invalid donation type selected.", "danger")

        return redirect(url_for("donate"))

    # GET request
    return render_template(
        "donate.html",
        money_balance=blockchain.money_balance,
        food_balance=blockchain.food_balance,
    )

@app.route("/request", methods=["GET", "POST"])
def request_help():
    global used_codes 
    
    if request.method == "POST":
        request_type = request.form.get("request_type")
        verification_code = request.form.get("verification_code", "").strip()

        if verification_code in ("1879", "1258") and verification_code not in used_codes:
            used_codes.add(verification_code)
            save_used_code(verification_code)
            print(used_codes)

            if request_type == "money":
                if blockchain.money_balance >= 100:
                    blockchain.money_balance -= 100
                    flash("RM100 deducted from money donations.", "success")
                else:
                    flash("Insufficient money balance.", "danger")

            elif request_type == "food":
                total_food = sum(blockchain.food_balance.values())
                if total_food >= 2:
                    qty_to_deduct = 2
                    for food_type in list(blockchain.food_balance.keys()):
                        available = blockchain.food_balance[food_type]
                        if available >= qty_to_deduct:
                            blockchain.food_balance[food_type] -= qty_to_deduct
                            qty_to_deduct = 0
                            break
                        else:
                            blockchain.food_balance[food_type] = 0
                            qty_to_deduct -= available
                    flash("2 units of food deducted.", "success")
                else:
                    flash("Insufficient food balance.", "danger")
        elif verification_code in used_codes:
            print(verification_code)
            flash("This verification code has already been used.", "danger")
        elif verification_code not in ("22","24"):   
            flash("Invalid verification code.", "danger")

        # IMPORTANT: Just render the template without redirect!
        return render_template(
            "request.html",
            money_balance=blockchain.money_balance,
            food_balance=blockchain.food_balance,
        )

    # GET request
    return render_template(
        "request.html",
        money_balance=blockchain.money_balance,
        food_balance=blockchain.food_balance,
    )


if __name__ == "__main__":
    app.run(debug=True)
