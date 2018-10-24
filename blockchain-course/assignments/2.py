names = ["Scooby", "Max", "Don Giovanni", "Nelson", "Bob", "Alexander"]

namesOut = []

for name in names:
  print(f"{name}: {len(name)}")

  if len(name) > 5 and ("n" in name or "N" in name):
    namesOut.append(name)

print()

while len(namesOut) > 0:
  print(namesOut.pop())
