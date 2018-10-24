from hashlib import sha256

# Example of controlling what is exported (as ugly strings) - a bit like Haskell's: module Blah (stuff to export)
__all__ = ["hash"]

def hash(string, algorithm = sha256):
  """
  Hashes a string and returns a hashed string of 64 characters.
  Note that the generated hash is actually a byte hash, and this can be converted to a String using hexdigest().

  Arguments:
    :string: The string to be hashed
  """

  return algorithm(string).hexdigest()
