from copy import deepcopy
from functools import reduce
from json import dumps as to_json
from json import loads as from_json
from block import Block
from transaction import Transaction
from pow import ProofOfWork as pow

class Blockchain:
  file_name = "blockchain.txt"

  mining_reward = 10

  def __init__(self, id):
    self.id = id

    # Initialising our blockchain list
    self.chain = [Block.genesis_block()]

    # Open/Unconfirmed transactions
    self.open_transactions = []

    self.load_data()

  def load_data(self):
    try:
      with open(Blockchain.file_name, mode = "r") as file:
        def parse_transaction(transaction):
          return Transaction(transaction["sender"], transaction["recipient"], transaction["amount"])

        def load_blockchain(loaded_blockchain):
          if len(loaded_blockchain) > 0:
            self.chain = []

            for block in from_json(loaded_blockchain):
              self.chain.append(
                Block(
                  block["index"],
                  block["previous_hash"],
                  [parse_transaction(tx) for tx in block["transactions"]],
                  block["proof"],
                  block["timestamp"]
                )
              )

        def load_open_transactions(loaded_open_transactions):
          if len(loaded_open_transactions) > 0:
            self.open_transactions = []

            for tx in from_json(loaded_open_transactions):
              self.open_transactions.append(parse_transaction(tx))

        load_blockchain(file.readline().rstrip("\n"))
        load_open_transactions(file.readline().rstrip("\n"))

    except FileNotFoundError:
      print("Warning: No existing Blockchain to load - New one will be created upon first 'mine'")

  def save_data(self):
    with open(Blockchain.file_name, mode = "w") as file:
      print("Saving")
      print(self.chain)
      file.write(to_json([block.__dict__.copy() for block in [Block(b.index, b.previous_hash, [tx.__dict__ for tx in b.transactions], b.proof, b.timestamp) for b in self.chain]]))
      file.write("\n")
      file.write(to_json([tx.__dict__.copy() for tx in self.open_transactions]))

  def get_last_blockchain_value(self):
    """Returns the last value of the current blockchain"""
    if len(self.chain) == 0:
      return None
    else:
      return self.chain[-1]

  def add_transaction(self, sender, recipient, amount):
    """ 
    Append a new transaction to list of open transactions

    Arguments:
      :sender: The sender of the coins
      :recipient: The recipient of the coins
      :amount: The amount of coins sent with the transaction
    """
    if self.id == None:
      return False

    transaction = Transaction(sender, recipient, amount)

    if transaction.verify(self.get_balance):
      self.open_transactions.append(transaction)

      # participants.add(sender)
      # participants.add(recipient)

      self.save_data()

      return True

    else:
      return False

  def get_balance(self):
    participant = self.id

    def amount(who):
      def participants(transaction):
        return transaction.counterpart(who) == participant

      participantTransactionAmountsPerBlock = [[tx.amount for tx in block.transactions if participants(tx)] for block in self.chain]
      print(f"{who} transaction amounts per block = {participantTransactionAmountsPerBlock}")
      
      return reduce(
        lambda acc, participantTransactionAmounts: acc + sum(participantTransactionAmounts) if len(participantTransactionAmounts) > 0 else acc,
        participantTransactionAmountsPerBlock,
        0
      )

    def amountOutstanding(who):
      return sum([tx.amount for tx in self.open_transactions if tx.counterpart(who) == participant])

    return amount("recipient") - amount("sender") - amountOutstanding("sender")

  def mine_block(self):
    if self.id == None:
      return False

    last_block = self.chain[-1]
    hashed_block = last_block.hash()

    reward_transaction = Transaction(sender = "MINING", recipient = self.id, amount = self.mining_reward)

    copied_transactions = self.open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = Block(
      index = len(self.chain),
      previous_hash = hashed_block,
      transactions = copied_transactions,
      proof = pow.proof_of_work(self)
    )

    self.chain.append(block)

    # Reset
    self.open_transactions = []
    self.save_data()

    return True

  def verify_chain(self):
    """Verify the current blockchain, returning True if valid, otherwise False - Note we skip the first genesis entry"""
    for index, block in enumerate(self.chain):
      if index == 0:
        if str(block) != str(Block.genesis_block()):
          return False
      else:
        if block.previous_hash != self.chain[index - 1].hash():
          print("block.previous_hash = " + block.previous_hash)
          print("self.chain[index - 1].hash() = " + self.chain[index - 1].hash())
          return False

        transactionsExcludingLastReward = block.transactions[: -1]

        if not pow.valid_proof(block.previous_hash, transactionsExcludingLastReward, block.proof):
          print("Proof of Work invalid")
          return False

    return True