from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from json import loads as from_json
from blockchain import Blockchain
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
      "funds": blockchain.get_balance()
    }, 200)

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
            "funds": blockchain.get_balance()
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
      "funds": blockchain.get_balance()
    }, 201)

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
    "funds": blockchain.get_balance()
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
    # TODO
    print("Booting nodes locally from existing blockchains")
  else:
    wallet = Wallet(id)
    blockchain = Blockchain(wallet.public_key, id)

    app.run(host="0.0.0.0", port=id)
