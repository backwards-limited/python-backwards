from flask import Flask, jsonify
from flask_cors import CORS
from blockchain import Blockchain
from wallet import Wallet

app = Flask(__name__)
CORS(app) # Since we have node communicating we need to allow calls from "other" clients, not just what is served by this node/server.

wallet = Wallet()
blockchain = Blockchain(wallet.public_key)

@app.route("/healthz", methods=["GET"])
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
    return jsonify({
      "data": {
        "message": "Block added successfully",
        "block": block.dict()
      }
    }), 201

@app.route("/chain", methods = ["GET"])
def chain():
  chain_dict = [block.dict() for block in blockchain.chain]
  return jsonify(chain_dict), 200

def reset_blockchain(responseCode):
  global blockchain
  blockchain = Blockchain(wallet.public_key)

  return jsonify({
      "data": {
          "public-key": wallet.public_key,
          "private-key": wallet.private_key
      }
  }), responseCode

def fail(message, responseCode):
  return jsonify({
      "error": {
          "message": message
      }
  }), responseCode

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 5000)
