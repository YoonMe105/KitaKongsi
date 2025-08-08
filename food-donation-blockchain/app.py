from flask import Flask, render_template, request, redirect, url_for, flash
import time

app = Flask(__name__)
app.secret_key = "secret"

# Blockchain data
blockchain = []
remaining_money = 0.0
food_stock = {}  # {food_name: quantity}

# Block structure
def create_block(index, timestamp, donation_type, sender, receiver, amount_or_quantity, item_name=None):
    return {
        "index": index,
        "timestamp": timestamp,
        "donation_type": donation_type,  # "money" or "food"
        "sender": sender,
        "receiver": receiver,
        "amount_or_quantity": amount_or_quantity,
        "item_name": item_name
    }

# Home
@app.route("/")
def home():
    return render_template("index.html", money_balance=remaining_money, food_stock=food_stock)

# Donate money
@app.route("/donate_money", methods=["GET", "POST"])
def donate_money():
    global remaining_money
    if request.method == "POST":
        sender = request.form["sender"]
        amount = float(request.form["amount"])
        if amount <= 0:
            flash("Amount must be greater than zero.")
            return redirect(url_for("donate_money"))
        block = create_block(len(blockchain) + 1, time.strftime("%Y-%m-%d %H:%M:%S"),
                             "money", sender, None, amount)
        blockchain.append(block)
        remaining_money += amount
        flash("Money donation recorded successfully!")
        return redirect(url_for("home"))
    return render_template("donate_money.html")

# Donate food
@app.route("/donate_food", methods=["GET", "POST"])
def donate_food():
    global food_stock
    if request.method == "POST":
        sender = request.form["sender"]
        item_name = request.form["item_name"]
        quantity = int(request.form["quantity"])
        if quantity <= 0:
            flash("Quantity must be greater than zero.")
            return redirect(url_for("donate_food"))
        block = create_block(len(blockchain) + 1, time.strftime("%Y-%m-%d %H:%M:%S"),
                             "food", sender, None, quantity, item_name)
        blockchain.append(block)
        food_stock[item_name] = food_stock.get(item_name, 0) + quantity
        flash("Food donation recorded successfully!")
        return redirect(url_for("home"))
    return render_template("donate_food.html")

# Request money
@app.route("/request_money", methods=["GET", "POST"])
def request_money():
    global remaining_money
    if request.method == "POST":
        receiver = request.form["receiver"]
        request_amount = float(request.form["amount"])
        if request_amount <= 0:
            flash("Amount must be greater than zero.")
            return redirect(url_for("request_money"))
        if request_amount > remaining_money:
            flash("Not enough funds available.")
            return redirect(url_for("request_money"))
        block = create_block(len(blockchain) + 1, time.strftime("%Y-%m-%d %H:%M:%S"),
                             "money_request", None, receiver, request_amount)
        blockchain.append(block)
        remaining_money -= request_amount
        flash("Money request fulfilled!")
        return redirect(url_for("home"))
    return render_template("request_money.html", available_money=remaining_money)

# Request food
@app.route("/request_food", methods=["GET", "POST"])
def request_food():
    global food_stock
    if request.method == "POST":
        receiver = request.form["receiver"]
        item_name = request.form["item_name"]
        quantity = int(request.form["quantity"])
        if quantity <= 0:
            flash("Quantity must be greater than zero.")
            return redirect(url_for("request_food"))
        if item_name not in food_stock or quantity > food_stock[item_name]:
            flash("Not enough stock for this food item.")
            return redirect(url_for("request_food"))
        block = create_block(len(blockchain) + 1, time.strftime("%Y-%m-%d %H:%M:%S"),
                             "food_request", None, receiver, quantity, item_name)
        blockchain.append(block)
        food_stock[item_name] -= quantity
        flash("Food request fulfilled!")
        return redirect(url_for("home"))
    return render_template("request_food.html", food_items=food_stock)

# History
@app.route("/history")
def history():
    return render_template("history.html", blockchain=blockchain)

if __name__ == "__main__":
    app.run(debug=True)
