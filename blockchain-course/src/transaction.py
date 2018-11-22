from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import binascii
from collections import OrderedDict
from utility.printable import Printable

class Transaction (Printable):
  mining = "mining"

  @staticmethod
  def verify_transactions(transactions, get_balance):
    return all([tx.verify(get_balance(tx.sender), False) for tx in transactions])

  def __init__(self, sender, recipient, amount, signature):
    self.sender = sender
    self.recipient = recipient
    self.amount = amount
    self.signature = signature

  def __repr__(self):
    return repr(self.__dict__)

  def counterpart(self, who):
    return self.__getattribute__(who)

  def to_ordered_dict(self):
    return OrderedDict([
      ("sender", self.sender),
      ("recipient", self.recipient),
      ("amount", self.amount),
      ("signature", self.signature)
    ])

  def verify(self, get_balance, check_funds = True):
    if check_funds and get_balance(self.sender) < self.amount:
      return False
    else:
      public_key = RSA.importKey(binascii.unhexlify(self.sender))
      verifier = PKCS1_v1_5.new(public_key)
      hashedPayload = SHA256.new((str(self.sender) + str(self.recipient) + str(self.amount)).encode("utf8"))

      return verifier.verify(hashedPayload, binascii.unhexlify(self.signature))
