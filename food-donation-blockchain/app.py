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

    def add_food_donation(self, food_type, quantity, location):
        if food_type in self.food_balance:
            self.food_balance[food_type] += quantity
        else:
            self.food_balance[food_type] = quantity
        print(f"DEBUG: Food donated added. {quantity} x {food_type} at {location}")

blockchain = Blockchain()

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
            location = request.form.get("location", "").strip()

            if not food_type or not quantity_str or not location:
                flash("Please enter food type, quantity, and location.", "danger")
                return redirect(url_for("donate"))

            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    raise ValueError
                blockchain.add_food_donation(food_type, quantity, location)
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
    if request.method == "POST":
        request_type = request.form.get("request_type")

        if not request_type:
            flash("Request type is required.", "danger")
            return redirect(url_for("request_help"))

        # MONEY REQUEST
        if request_type == "money":
            amount_str = request.form.get("amount", "").strip()
            print("DEBUG: Raw amount entered ->", repr(amount_str))

            if not amount_str:
                flash("Please enter a valid amount greater than zero.", "danger")
                return redirect(url_for("request_help"))

            try:
                cleaned_amount = amount_str.replace(",", "").replace("RM", "").replace("$", "").strip()
                print("DEBUG: Cleaned amount ->", repr(cleaned_amount))

                amount = float(cleaned_amount)
                if amount <= 0:
                    raise ValueError

                blockchain.money_balance -= amount
                flash("Money Request Approved!", "success")

            except ValueError:
                flash("Please enter a valid amount greater than zero.", "danger")

        # FOOD REQUEST
        elif request_type == "food":
            food_type = request.form.get("food_type", "").strip()
            quantity_str = request.form.get("quantity", "").strip()
            location = request.form.get("location", "").strip()

            if not food_type or not quantity_str or not location:
                flash("Please enter food type, quantity, and location.", "danger")
                return redirect(url_for("request_help"))

            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    raise ValueError
                if (
                    food_type in blockchain.food_balance
                    and quantity <= blockchain.food_balance[food_type]
                ):
                    blockchain.food_balance[food_type] -= quantity
                    flash(f"Food request approved: {quantity} x {food_type} sent to {location}!", "success")
                else:
                    flash("Not enough food available!", "danger")
            except (ValueError, TypeError):
                flash("Please enter a valid quantity greater than zero.", "danger")

        else:
            flash("Invalid request type selected.", "danger")

        return redirect(url_for("request_help"))

    return render_template(
        "request.html",
        money_balance=blockchain.money_balance,
        food_balance=blockchain.food_balance,
    )

if __name__ == "__main__":
    app.run(debug=True)
