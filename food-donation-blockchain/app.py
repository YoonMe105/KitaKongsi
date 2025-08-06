from flask import Flask, render_template
from blockchain import Blockchain  # Import your Blockchain class

app = Flask(__name__)
blockchain = Blockchain()  # Create an instance

@app.route('/')
def index():
    return render_template('index.html', chain=blockchain.chain)

if __name__ == '__main__':
    app.run(debug=True)
