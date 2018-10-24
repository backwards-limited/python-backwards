from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii

class Wallet:
  file_name = "wallet.txt"

  @staticmethod
  def create():
    wallet = Wallet()
    wallet.create_keys()
    return wallet

  def __init__(self, *args, **kwargs):
    self.public_key = None
    self.private_key = None

  def create_keys(self):
    def generate_keys():
      private_key = RSA.generate(1024, Crypto.Random.new().read)
      public_key = private_key.publickey()

      return (binascii.hexlify(private_key.exportKey(format = "DER")).decode(),
              binascii.hexlify(public_key.exportKey(format = "DER")).decode())

    private_key, public_key = generate_keys()
    self.private_key = private_key
    self.public_key = public_key

  def save_keys(self):
    if self.public_key != None and self.private_key != None:
      try:
        with open(Wallet.file_name, mode = "w") as file:
          file.write(self.public_key)
          file.write("\n")
          file.write(self.private_key)
      except IOError:
        print("Failed to save wallet")

  def load_keys(self):
    try:
      with open(Wallet.file_name, mode = "r") as file:
        self.public_key = file.readline().rstrip("\n")
        self.private_key = file.readline().rstrip("\n")
    except IOError:
      print("Failed to load wallet")

  def sign(self, sender, recipient, amount):
    signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
    hashedPayload = SHA256.new((str(sender) + str(recipient) + str(amount)).encode("utf8"))

    signature = signer.sign(hashedPayload)

    return binascii.hexlify(signature).decode("ascii")