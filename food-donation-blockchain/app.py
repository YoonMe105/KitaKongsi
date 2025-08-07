from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = "secret"

blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'GET':
        return render_template('donate.html')

    data = request.get_json()
    food = data.get("food")
    quantity = data.get("quantity")
    location = data.get("location")

    if not food or not quantity or not location:
        return jsonify({"error": "Missing food, quantity, or location."}), 400

    donation_data = {
        "food": food,
        "quantity": quantity,
        "location": location
    }

    block = blockchain.add_block(
        donation_type="food",
        sender="anonymous",
        receiver=location,
        data=donation_data
    )

    return jsonify({"message": f"Food donation recorded in block #{block.index}!"})

@app.route('/donations')
def donations():
    return jsonify(blockchain.to_list())

@app.route('/history')
def history():
    return render_template('history.html', donations=blockchain.to_list())

@app.route('/receive', methods=['GET', 'POST'])
def receive():
    if request.method == 'POST':
        donation_type = request.form['donation_type']
        wallet_address = request.form['wallet_address'].strip()

        if not wallet_address.startswith("0x") or len(wallet_address) != 42:
            flash("Invalid wallet address. Please use a valid crypto address (e.g., MetaMask).")
            return redirect(url_for('receive'))

        flash(f"Your request to receive {donation_type} has been submitted! A donor will be matched soon.")
        return redirect(url_for('receive'))

    return render_template('receive.html')

@app.route('/donate-money', methods=['GET', 'POST'])
def donate_money():
    if request.method == 'POST':
        sender = request.form['sender'].strip()
        receiver = request.form['receiver'].strip()
        amount = request.form['amount'].strip()

        # Validate Ethereum addresses
        if not (sender.startswith("0x") and len(sender) == 42):
            flash("Invalid sender wallet address.")
            return redirect(url_for('donate_money'))

        if not (receiver.startswith("0x") and len(receiver) == 42):
            flash("Invalid receiver wallet address.")
            return redirect(url_for('donate_money'))

        try:
            amount_float = float(amount)
            if amount_float <= 0:
                flash("Donation amount must be a positive number.")
                return redirect(url_for('donate_money'))
        except ValueError:
            flash("Invalid donation amount.")
            return redirect(url_for('donate_money'))

        donation_data = {
            "amount": amount,
            "currency": "ETH"
        }

        block = blockchain.add_block(
            donation_type="money",
            sender=sender,
            receiver=receiver,
            data=donation_data
        )

        flash(f"{amount} ETH donated successfully from {sender} to {receiver}!")
        return redirect(url_for('index'))

    return render_template('donate_money.html')

@app.route('/blockchain_data')
def blockchain_data():
    return jsonify([
        block.to_dict()
        for block in blockchain.chain
        if block.donation_type != "genesis"
    ])

@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    app.run(debug=True)
