# Write to file
file = open("demo.txt", mode = "w")

file.write("Hello from Python 1\n")
file.write("Hello from Python 2\n")
file.write("Hello from Python 3\n")
file.close()

# Read entire content from file
file = open("demo.txt", mode = "r")

entireContent = file.read()
file.close()

print(f"Read file content:\n{entireContent}")

# Read each line from file including "new lines"
print("\nReading each line:")
file = open("demo.txt", mode = "r")

for line in file.readlines():
  print(line)

file.close()

# Read each line from file excluding "new lines"
print("\nReading each line:")
file = open("demo.txt", mode = "r")

for line in file.readlines():
  print(line[: -1])

file.close()

# Use "with" to avoid having to call "close"
print("\nWith...")

with open("demo.txt", mode = "r") as file:
  line = file.readline()

  while line:
    print(line)
    line = file.readline()

print("\nDone!")
 