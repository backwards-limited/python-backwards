import copy

persons = [
  {"name": "Bob", "age": 76, "hobbies": ["F1", "Golf"]},
  {"name": "Sue", "age": 22, "hobbies": ["Rugby", "Tennis"]},
  {"name": "Polly", "age": 18, "hobbies": ["F1", "Tennis"]}
]

print("-" * 50)

names = [p["name"] for p in persons]
print(f"Names of persons: {names}\n")

allOlderThan20 = all([p["age"] > 20 for p in persons])
print(f"All persons older than 20: {allOlderThan20}\n")

personsCopy = copy.deepcopy(persons)
personsCopy[0]["name"] = "Bobby"
print(f"Copy changed: {personsCopy}\n")
print(f"Original: {persons}\n")

bob, sue, polly = persons
print(f"Bob: {bob}")
print(f"Sue: {sue}")
print(f"Polly: {polly}")