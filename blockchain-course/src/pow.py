from hashlib import sha256

class ProofOfWork:
  @staticmethod
  def valid_proof(last_hash, transactions, proof):
    guess = (str(last_hash) + str([tx.to_ordered_dict() for tx in transactions]) + str(proof)).encode()
    guess_hash = sha256(guess).hexdigest()

    return guess_hash[0: 2] == "00"

  @classmethod
  def proof_of_work(cls, blockchain):
    last_block = blockchain.chain[-1]
    last_hash = last_block.hash()

    proof = 0

    while not cls.valid_proof(last_hash, blockchain.open_transactions, proof):
      proof += 1

    return proof
