"""Application"""

from uuid import uuid4
from block import Block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet

class Node:
  def __init__(self, *args, **kwargs):
    self.wallet = Wallet.create()
    self.blockchain = Blockchain(self.wallet.public_key)

  def get_user_choice(self):
    return input("Your choice: ")

  def get_transaction_value(self):
    """Returns input of the user - a new transaction"""
    recipient = input("Recipient of transaction? ")
    amount = float(input("Your transaction amount: "))

    return recipient, amount

  def print_blockchain_elements(self):
    # Output the blockchain list to the console
    for block in self.blockchain.chain:
      print(f"Outputting Block: {block}")
    else:
      print("-" * 25)

  def listen_for_input(self):
    while True:
      print("\nPlease choose")
      print("1: Add a new transaction")
      print("2: Mine a new block")
      print("3: Output the blockchain blocks")
      print("4: Check transaction validity")
      print("5: Create wallet")
      print("6: Load wallet")
      print("7: Save wallet")
      print("h: Manipulate the chain")
      print("q: Quit")
      user_choice = self.get_user_choice()

      if user_choice == "1":
        recipient, amount = self.get_transaction_value()

        signature = self.wallet.sign(self.wallet.public_key, recipient, amount)

        if self.blockchain.add_transaction(self.wallet.public_key, recipient, amount, signature):
          print("Added transaction")
        else:
          print("Transaction failed")

        print(f"\nOpen transactions: {self.blockchain.open_transactions}")

      elif user_choice == "2":
        if not self.blockchain.mine_block():
          print("Mining failed - Have you been hacked?")

      elif user_choice == "3":
        self.print_blockchain_elements()

      elif user_choice == "4":
        if Transaction.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
          print("All transactions are valid")
        else:
          print("NOT all transactions are valid")

      elif user_choice == "5":
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

      elif user_choice == "6":
        self.wallet.load_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

      elif user_choice == "7":
        self.wallet.save_keys()

      elif user_choice == "h":
        if len(self.blockchain.chain) >= 1:
          hackedBlock = Block.genesis_block()
          hackedBlock.transactions = [Transaction(sender = "hacker1", recipient = "hacker2", amount = 100, signature = "hacked")]

          self.blockchain.chain[0] = hackedBlock

      elif user_choice == "q":
        break

      else:
        print("Input invalid, please pick a value from the list!")

      if not self.blockchain.verify_chain():
        print("\nCorrupt Blockchain:")
        self.print_blockchain_elements()
        break

      print(f"\nBalance of {self.wallet.public_key}: {self.blockchain.get_balance():6.2f}\n")

    print("\nDone!")

if "__main__" == __name__:
  node = Node()
  node.listen_for_input()
