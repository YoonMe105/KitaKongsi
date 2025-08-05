from flask import Flask, request, jsonify, render_template
from blockchain import Blockchain

app = Flask(__name__)
my_blockchain = Blockchain()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/donate', methods=['POST'])
def donate():
    data = request.json
    required_fields = ['food', 'quantity', 'location']
    if not all(field in data and data[field].strip() for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    my_blockchain.add_block(data)
    return jsonify({"message": "Donation recorded successfully!"})

@app.route('/donations', methods=['GET'])
def donations():
    return jsonify(my_blockchain.get_chain())

if __name__ == '__main__':
    app.run(debug=True)
