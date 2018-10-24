"""Extending this class makes a subclass printable to display its contents as a dictionary"""

class Printable:
  def __repr__(self):
    return repr(self.__dict__)