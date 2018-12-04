from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from json import loads as from_json
from block import Block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet

app = Flask(__name__)
CORS(app)  # Since we have node communicating we need to allow calls from "other" clients, not just what is served by this node/server.

@app.route("/", methods = ["GET"])
def node_ui():
  return send_from_directory("ui", "node.html")

@app.route("/network", methods = ["GET"])
def newtwork_ui():
  return send_from_directory("ui", "network.html")

@app.route("/healthz", methods = ["GET"])
def health():
  return "Good to go!"

@app.route("/wallet", methods = ["POST"])
def create_keys():
  wallet.create_keys()

  if wallet.save_keys():
    return reset_blockchain(201)
  else:
    return fail(500, message = "Saving keys failed")

@app.route("/wallet", methods = ["GET"])
def load_keys():
  if wallet.load_keys():
    return reset_blockchain(200)
  else:
    return fail(500, message = "Loading keys failed")

@app.route("/balance", methods = ["GET"])
def balance():
  if wallet.public_key == None:
    return fail(500, message = "No wallet")
  else:
    return success(200, "Fetched balance successfully", {
      "funds": blockchain.get_balance(wallet.public_key)
    })

@app.route("/transaction/broadcast", methods = ["POST"])
def transaction_broadcast():
  try:
    json = from_json(request.data)
    transaction = blockchain.add_transaction(json["sender"], json["recipient"], json["amount"], json["signature"], is_receiving = True)

    if transaction == None:
      return fail(500, message = "Failed to add broadcast transaction")
    else:
      return success(201, "Successfully added broadcast transaction", {
        "transaction": dict(transaction.to_ordered_dict())
      })

  except (ValueError, KeyError, TypeError):
    return fail(400, message = "Failed to add broadcast transaction")

@app.route("/transaction", methods = ["POST"])
def add_transaction():
  if wallet.public_key == None:
    return fail(400, message = "Cannot add transaction - no existing wallet")
  else:
    json = request.get_json()

    if json:
      required_fields = ["recipient", "amount"]

      if all(field in json for field in required_fields):
        recipient = json["recipient"]
        amount = json["amount"]
        signature = wallet.sign(wallet.public_key, recipient, amount)

        transaction = blockchain.add_transaction(wallet.public_key, recipient, amount, signature)

        if transaction == None:
          return fail(500, message = "Failed to add transaction")
        else:
          return success(201, "Transaction added successfully", {
            "transaction": dict(transaction.to_ordered_dict()),
            "funds": blockchain.get_balance(wallet.public_key)
          })

      else:
        return fail(400, message = "Required data is missing")

    else:
      return fail(400, message = "No appropriate transaction data given")

@app.route("/mine", methods = ["POST"])
def mine():
  if blockchain.resolve_conflicts:
    return fail(409, "Resolve conflicts first, block not added")

  block = blockchain.mine_block()

  if block is None:
    return fail(500, "Adding a block failed", {
      "wallet-exists": wallet.public_key != None
    })

  else:
    return success(201, "Block added successfully", {
      "block": block.dict(),
      "funds": blockchain.get_balance(wallet.public_key)
    })

@app.route("/block/broadcast", methods = ["POST"])
def block_broadcast():
  try:
    json = from_json(request.data)["block"]

    txs = [Transaction(tx["sender"], tx["recipient"], tx["amount"], tx["signature"]) for tx in json["transactions"]]
    block = Block(json["index"], json["previous-hash"], txs, json["proof"], json["timestamp"])

    if block.index == blockchain.chain[-1].index + 1:
      if blockchain.add_block(block):
        return success(201, "Successfully added broadcast block", {
          "block": block.dict()
        })
      else:
        return fail(409, message = "Failed to add conflicting broadcast block")

    elif block.index > blockchain.chain[-1].index:
      blockchain.resolve_conflicts = True

      return success(200, "Blockchain seems to differ from local blockchain")  # TODO
    else:
      return fail(409, message = "Broadcast blockchain is shorter - Not added")

  except (ValueError, KeyError, TypeError):
    return fail(400, message = "Failed to add broadcast block")

@app.route("/transactions", methods = ["GET"])
def transactions():
  return success(200, json = {
    "transactions": [tx.__dict__ for tx in blockchain.open_transactions]
  })

@app.route("/chain", methods = ["GET"])
def chain():
  chain_dict = [block.dict() for block in blockchain.chain]

  return success(200, json = {
    "blockchain": chain_dict
  })

@app.route("/node", methods = ["POST"])
def add_node():
  try:
    json = from_json(request.data)
    blockchain.add_peer_node(json["node-ip"])

    return success(201, "Node added successfully", {
      "nodes": list(blockchain.peer_node_ips)
    })

  except (ValueError, KeyError, TypeError):
    return fail(400, message = "Valid node IP not provided")

@app.route("/node/<node_ip>", methods = ["DELETE"])
def remove_node(node_ip):
  if node_ip in blockchain.peer_node_ips:
    blockchain.remove_peer_node(node_ip)

    return success(200, f"Node {node_ip} removed", {
      "nodes": list(blockchain.peer_node_ips)
    })
  else:
    return fail(400, message = f"Given node {node_ip} not found for removal")

@app.route("/nodes", methods = ["GET"])
def nodes():
  return success(200, json = {
    "nodes": list(blockchain.peer_node_ips)
  })

@app.route("/resolve-conflicts", methods = ["POST"])
def resolve_conflicts():
  if blockchain.resolve():
    return success(200, "Chain was replaced")
  else:
    return success(200, "Local chain kept")

def reset_blockchain(responseCode):
  global blockchain
  blockchain = Blockchain(wallet.public_key, id)

  return success(responseCode, json = {
    "public-key": wallet.public_key,
    "private-key": wallet.private_key,
    "funds": blockchain.get_balance(wallet.public_key)
  })

def success(responseCode, message = "", json = None):
  return response("data", responseCode, message, json)

def fail(responseCode, message = "", json = None):
  return response("error", responseCode, message, json)

def response(category, responseCode, message = "", json = None):
  j = {
    category: {
    }
  }

  if message.strip():
    j[category].update({"message": message})

  if json is not None:
    j[category].update(json)

  return jsonify(j), responseCode

if __name__ == "__main__":
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument("-p", "--port", type = int)
  args = parser.parse_args()

  id = args.port

  if id is None:
    # Booting: python node.py
    # TODO
    print("Booting nodes locally from existing blockchains - WIP where we currently hardcode a node on port 5000")
    port_hard_coded = 5000
    wallet = Wallet(port_hard_coded)
    blockchain = Blockchain(wallet.public_key, port_hard_coded)

    app.run(host = "0.0.0.0", port = port_hard_coded)
  else:
    # Booting: python node.py --port=5001 and python node.py --port=5002 etc.
    wallet = Wallet(id)
    blockchain = Blockchain(wallet.public_key, id)

    app.run(host = "0.0.0.0", port = id)