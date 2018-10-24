"""
Regarding this module "utility" we can control what is exported, though it is better to control this at the file level much like Haskell.
E.g.

from utility.hash import hash

__all__ = ["hash"]
"""