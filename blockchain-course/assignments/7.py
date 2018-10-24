class Food:
  name = "class name"
  kind = "class kind"

  def __init__(self, name, kind):
    self.name = name
    self.kind = kind

  def __repr__(self):
    return repr(self.__dict__)

  def describe(self):
    print(f"Call me {self.name}, I am {self.kind}")

  @classmethod
  def describe_class(cls):
    print(f"Call me {cls.name}, I am {cls.kind}")

  @staticmethod
  def describe_static(name, kind):
    print(f"Call me {name}, I am {kind}")

class Meat (Food):
  def __init__(self, name):
    super().__init__(name, "meat")

  def cook(self):
    print(f"I am cooking {self.name} which is a {self.kind}")

class Fruit (Food):
  def __init__(self, name):
    super().__init__(name, "fruit")

  def clean(self):
    print(f"I am cleaning {self.name} which is a {self.kind}")

apple = Food("apple", "fruit")
apple.describe()
Food.describe_class()
Food.describe_static("static name", "static kind")

meat = Meat("seabass")
meat.cook()

fruit = Fruit("mango")
fruit.clean()
print(f"Fruit: {fruit}")
