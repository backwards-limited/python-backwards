from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from json import loads as from_json
from block import Block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet

app = Flask(__name__)
CORS(app) # Since we have node communicating we need to allow calls from "other" clients, not just what is served by this node/server.

@app.route("/", methods = ["GET"])
def node_ui():
  return send_from_directory("ui", "node.html")

@app.route("/network", methods = ["GET"])
def newtwork_ui():
  return send_from_directory("ui", "network.html")

@app.route("/healthz", methods= ["GET"])
def health():
  return "Good to go!"

@app.route("/wallet", methods = ["POST"])
def create_keys():
  wallet.create_keys()

  if wallet.save_keys():
    return reset_blockchain(201)
  else:
    return fail("Saving keys failed", 500)

@app.route("/wallet", methods = ["GET"])
def load_keys():
  if wallet.load_keys():
    return reset_blockchain(200)
  else:
    return fail("Loading keys failed", 500)

@app.route("/balance", methods = ["GET"])
def balance():
  if wallet.public_key == None:
    return fail("No wallet", 500)
  else:
    return success({
      "message": "Fetched balance successfully",
      "funds": blockchain.get_balance(wallet.public_key)
    }, 200)

@app.route("/transaction/broadcast", methods = ["POST"])
def transaction_broadcast():
  try:
    json = from_json(request.data)
    transaction = blockchain.add_transaction(json["sender"], json["recipient"], json["amount"], json["signature"], is_receiving = True)
    
    if transaction == None:
      return fail("Failed to add broadcast transaction", 500)
    else:
      return success({
        "message": "Successfully added broadcast transaction",
        "transaction": dict(transaction.to_ordered_dict())
      }, 201)

  except (ValueError, KeyError, TypeError):
    return fail("Failed to add broadcast transaction", 400)

@app.route("/transaction", methods = ["POST"])
def add_transaction():
  if wallet.public_key == None:
    return fail("Cannot add transaction - no existing wallet", 400)
  else:
    json = request.get_json()

    if json:
      required_fields = ["recipient", "amount"]

      if all(field in json for field in required_fields):
        recipient = json["recipient"]
        amount = json["amount"]
        signature = wallet.sign(wallet.public_key, recipient, amount)

        transaction = blockchain.add_transaction(wallet.public_key, recipient, amount, signature)

        if transaction  == None:
          return fail("Failed to add transaction", 500)
        else:
          return success({
            "message": "Transaction added successfully",
            "transaction": dict(transaction.to_ordered_dict()),
            "funds": blockchain.get_balance(wallet.public_key)
          }, 201)

      else:
        return fail("Required data is missing", 400)

    else:
      return fail("No appropriate transaction data given", 400)

@app.route("/mine", methods = ["POST"])
def mine():
  block = blockchain.mine_block()

  if block == None:
    return jsonify({
        "error": {
            "message": "Adding a block failed",
            "wallet-exists": wallet.public_key != None
        }
    }), 500

  else:
    return success({
      "message": "Block added successfully",
      "block": block.dict(),
      "funds": blockchain.get_balance(wallet.public_key)
    }, 201)

@app.route("/block/broadcast", methods = ["POST"])
def block_broadcast():
  try:
    json = from_json(request.data)["block"]

    transactions = [Transaction(tx["sender"], tx["recipient"], tx["amount"], tx["signature"]) for tx in json["transactions"]]
    block = Block(json["index"], json["previous-hash"], transactions, json["proof"], json["timestamp"])

    if block.index == blockchain.chain[-1].index + 1:
      if blockchain.add_block(block):
        return success({
          "message": "Successfully added broadcast block",
          "block": block.dict()
        }, 201)
      else:
        return fail("Failed to add broadcast block", 500)  
    elif block.index > blockchain.chain[-1].index:
      pass  
    else:
      return fail("Broadcast blockchain is shorter - Not added", 409)
      
  except (ValueError, KeyError, TypeError):
    return fail("Failed to add broadcast block", 400)

@app.route("/transactions", methods = ["GET"])
def transactions():
  return success({
    "transactions": [tx.__dict__ for tx in blockchain.open_transactions]
  }, 200)

@app.route("/chain", methods = ["GET"])
def chain():
  chain_dict = [block.dict() for block in blockchain.chain]
  return jsonify(chain_dict), 200

@app.route("/node", methods = ["POST"])
def add_node():
  try:
    json = from_json(request.data)
    blockchain.add_peer_node(json["node-ip"])

    return success({
      "message": "Node added successfully",
      "nodes": list(blockchain.peer_node_ips)
    }, 201)

  except (ValueError, KeyError, TypeError):
    return fail("Valid node IP not provided", 400)

@app.route("/node/<node_ip>", methods = ["DELETE"])
def remove_node(node_ip):
  if node_ip in blockchain.peer_node_ips:
    blockchain.remove_peer_node(node_ip)

    return success({
      "message": f"Node {node_ip} removed",
      "nodes": list(blockchain.peer_node_ips)
    }, 200)
  else:
    return fail(f"Given node {node_ip} not found for removal", 400)  

@app.route("/nodes", methods = ["GET"])
def nodes():
  return success({
    "nodes": list(blockchain.peer_node_ips)
  }, 200)

def reset_blockchain(responseCode):
  global blockchain
  blockchain = Blockchain(wallet.public_key, id)

  return success({
    "public-key": wallet.public_key,
    "private-key": wallet.private_key,
    "funds": blockchain.get_balance(wallet.public_key)
  }, responseCode)

def success(json, responseCode):
  j = {
    "data": {}
  }

  j["data"] = json

  return jsonify(j), responseCode

def fail(message, responseCode):
  return jsonify({
    "error": {
      "message": message
    }
  }), responseCode

if __name__ == "__main__":
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument("-p", "--port", type = int)
  args = parser.parse_args()

  id = args.port

  if id == None:
    # Booting: python node.py
    # TODO
    print("Booting nodes locally from existing blockchains - WIP where we currently hardcode a node on port 5000")
    port_hard_coded = 5000
    wallet = Wallet(port_hard_coded)
    blockchain = Blockchain(wallet.public_key, port_hard_coded)

    app.run(host="0.0.0.0", port = port_hard_coded)
  else:
    # Booting: python node.py --port=5001 and python node.py --port=5002 etc.
    wallet = Wallet(id)
    blockchain = Blockchain(wallet.public_key, id)

    app.run(host="0.0.0.0", port = id)