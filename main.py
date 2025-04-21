from flask import Flask, request, render_template, jsonify
from students_part import nodes
from node import Node

app = Flask(__name__)

# Create a new node with a unique ID (e.g., 1)
node = Node(id=1)

# Append the node to the list of nodes
nodes.append(node)

@app.route('/')
def index():
    return render_template('index.html')  # This will render the HTML form

@app.route('/send', methods=['POST'])
def send_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = int(request.form['amount'])

    # Assuming create_transaction is a method of Node
    tx = node.create_transaction(sender, receiver, amount)

    # You can render a response or simply return a JSON as follows:
    return jsonify({'message': 'Transaction sent', 'transaction': tx.to_dict()}), 200

@app.route('/mine', methods=['GET'])
def mine_block():
    block = node.mine_block()
    if block:
        return jsonify({'message': 'Block mined', 'block': block.to_dict()}), 200
    else:
        return jsonify({'message': 'Nothing to mine'}), 400

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.to_dict() for block in node.blockchain.chain]
    return jsonify({'length': len(chain_data), 'chain': chain_data}), 200

if __name__ == '__main__':
    app.run(port=5000)
