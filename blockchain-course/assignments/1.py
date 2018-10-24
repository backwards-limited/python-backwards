name = input("Your name: ")
age = int(input("Your age: "))

def me():
  return f"{name} {age}"

def two(first, second):
  return f"{first} {second}"

def decades(age):
  decades = age // 10
  decadesMsg = "decades"

  if decades == 1:
    decadesMsg = "decade"

  return f"You have lived {decades} {decadesMsg}"

print()

print(me())

print(two("Hi", "There"))

print(decades(age))