from collections import OrderedDict
from json import dumps as to_json
from time import time
from utility.hash import hash
from utility.printable import Printable

class Block (Printable):
  @staticmethod
  def genesis_block():
    return Block(
      index = 0,
      previous_hash = "",
      transactions = [],
      proof = 100,
      timestamp = 0
    )

  def __init__(self, index, previous_hash, transactions, proof, timestamp = None):
    self.index = index
    self.previous_hash = previous_hash
    self.transactions = transactions
    self.proof = proof
    self.timestamp = time() if timestamp is None else timestamp

  def hash(self):
    """
    Hashes block and returns a string representation of it (as a 64 characters).
    This block is first converted to JSON.
    Said JSON is encoded a UTF-8 String and then hashed with the SHA256 algorithm.
    The hash that is actually generated is a byte hash, and this can be converted to a String using hexdigest().
    """

    block_dict = self.__dict__.copy()
    block_dict["transactions"] = [tx.to_ordered_dict() for tx in block_dict["transactions"]]

    return hash(to_json(block_dict, sort_keys = True).encode())
    # return hash(to_json(self.__dict__.copy(), sort_keys=True).encode())