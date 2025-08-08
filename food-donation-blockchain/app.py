from flask import Flask, render_template, request, redirect, url_for, flash
import time
import json
import os

app = Flask(__name__)
app.secret_key = "secret"

# Blockchain
blockchain = []
money_balance = 0
food_balances = {}  # { "Rice": 10, "Noodles": 5 }

DATA_FILE = "blockchain_data.json"

# -------- Blockchain Functions --------
def load_data():
    global blockchain, money_balance, food_balances
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            blockchain = data.get("blockchain", [])
            money_balance = data.get("money_balance", 0)
            food_balances = data.get("food_balances", {})
    else:
        blockchain.clear()
        money_balance = 0
        food_balances.clear()

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "blockchain": blockchain,
            "money_balance": money_balance,
            "food_balances": food_balances
        }, f)

def add_block(donation_type, sender, receiver, data):
    block = {
        "index": len(blockchain) + 1,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "donation_type": donation_type,
        "sender": sender,
        "receiver": receiver,
        "data": data
    }
    blockchain.append(block)
    save_data()

# -------- Routes --------
@app.route("/")
def home():
    return render_template("home.html", 
                           money_balance=money_balance, 
                           food_balances=food_balances)

@app.route("/donate_money", methods=["GET", "POST"])
def donate_money():
    global money_balance
    if request.method == "POST":
        sender = request.form["name"]
        amount = float(request.form["amount"])
        if amount <= 0:
            flash("Invalid amount.", "danger")
            return redirect(url_for("donate_money"))
        money_balance += amount
        add_block("money", sender, "", {"amount": amount})
        flash("Money donation successful!", "success")
        return redirect(url_for("home"))
    return render_template("form.html", page_type="donate_money")

@app.route("/request_money", methods=["GET", "POST"])
def request_money():
    global money_balance
    if request.method == "POST":
        receiver = request.form["name"]
        amount = float(request.form["amount"])
        if amount <= 0 or amount > money_balance:
            flash("Invalid request amount.", "danger")
            return redirect(url_for("request_money"))
        money_balance -= amount
        add_block("money_request", "", receiver, {"amount": amount})
        flash("Money request fulfilled!", "success")
        return redirect(url_for("home"))
    return render_template("form.html", page_type="request_money", max_money=money_balance)

@app.route("/donate_food", methods=["GET", "POST"])
def donate_food():
    global food_balances
    food_types = ["Rice", "Noodles", "Canned Food", "Biscuits", "Milk"]
    if request.method == "POST":
        sender = request.form["name"]
        food_type = request.form["food_type"]
        quantity = int(request.form["quantity"])
        if quantity <= 0:
            flash("Invalid quantity.", "danger")
            return redirect(url_for("donate_food"))
        food_balances[food_type] = food_balances.get(food_type, 0) + quantity
        add_block("food", sender, "", {"type": food_type, "quantity": quantity})
        flash("Food donation successful!", "success")
        return redirect(url_for("home"))
    return render_template("form.html", page_type="donate_food", food_types=food_types)

@app.route("/request_food", methods=["GET", "POST"])
def request_food():
    global food_balances
    available_types = [ftype for ftype, qty in food_balances.items() if qty > 0]
    if request.method == "POST":
        receiver = request.form["name"]
        food_type = request.form["food_type"]
        quantity = int(request.form["quantity"])
        if food_type not in food_balances or quantity <= 0 or quantity > food_balances[food_type]:
            flash("Invalid request.", "danger")
            return redirect(url_for("request_food"))
        food_balances[food_type] -= quantity
        add_block("food_request", "", receiver, {"type": food_type, "quantity": quantity})
        flash("Food request fulfilled!", "success")
        return redirect(url_for("home"))
    return render_template("form.html", page_type="request_food", food_types=available_types)

@app.route("/history")
def history():
    return render_template("history.html", blockchain=blockchain)

if __name__ == "__main__":
    load_data()
    app.run(debug=True)
