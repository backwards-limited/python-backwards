from vehicle import Vehicle

class Car (Vehicle):
  def blah():
    return "Global function"

  def brag(self):
    print("Look at my cool car")

car1 = Car()
print(car1)

car1.add_warning("warn")
print(car1)

car1._Vehicle__warnings.append("whoops")
print(car1)

print(Car.blah())