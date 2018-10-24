from collections import OrderedDict
from utility.printable import Printable

class Transaction (Printable):
  @staticmethod
  def verify_transactions(transactions, get_balance):
    return all([tx.verify(get_balance) for tx in transactions])

  def __init__(self, sender, recipient, amount):
    self.sender = sender
    self.recipient = recipient
    self.amount = amount

  def __repr__(self):
    return repr(self.__dict__)

  def counterpart(self, who):
    return self.__getattribute__(who)

  def to_ordered_dict(self):
    return OrderedDict([
      ("sender", self.sender),
      ("recipient", self.recipient),
      ("amount", self.amount)
    ])

  def verify(self, get_balance):
    return get_balance() >= self.amount
