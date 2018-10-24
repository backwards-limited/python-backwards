from datetime import datetime
from random import random
from math import ceil

print("Random number between 0 and 1")
print(random())

print("Random number between 1 and 10")
print(ceil(random() * 10))

print("Unique combination of date time and randomw")
print(f"{round(random() * (10 ** 16))}-{int(datetime.now().strftime('%s')) * 1000}")
