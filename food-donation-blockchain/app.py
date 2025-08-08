from flask import Flask, render_template, request, redirect, url_for, flash
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = "supersecret"

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

        if donation_type == "money":
            amount = request.form.get("amount")
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError
                blockchain.add_money_donation(amount)
                flash("Thank you for donating money!", "success")
            except (ValueError, TypeError):
                flash("Please enter a valid amount greater than zero.", "danger")

        elif donation_type == "food":
            food_type = request.form.get("food_type")
            quantity = request.form.get("quantity")
            if not food_type or not quantity:
                flash("Please enter food type and quantity.", "danger")
                return redirect(url_for("donate"))
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError
                blockchain.add_food_donation(food_type, quantity)
                flash("Thank you for donating food!", "success")
            except (ValueError, TypeError):
                flash("Please enter a valid quantity greater than zero.", "danger")

        else:
            flash("Invalid donation type selected.", "danger")

        return redirect(url_for("donate"))

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

        if request_type == "money":
            amount = request.form.get("amount")
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError
                if amount <= blockchain.money_balance:
                    blockchain.money_balance -= amount
                    flash(f"Money request approved: {amount} units sent!", "success")
                else:
                    flash("Not enough funds available!", "danger")
            except (ValueError, TypeError):
                flash("Please enter a valid amount greater than zero.", "danger")

        elif request_type == "food":
            food_type = request.form.get("food_type")
            quantity = request.form.get("quantity")
            if not food_type or not quantity:
                flash("Please enter food type and quantity.", "danger")
                return redirect(url_for("request_help"))
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError
                if (
                    food_type in blockchain.food_balance
                    and quantity <= blockchain.food_balance[food_type]
                ):
                    blockchain.food_balance[food_type] -= quantity
                    flash(f"Food request approved: {quantity} x {food_type} sent!", "success")
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
