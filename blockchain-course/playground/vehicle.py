class Vehicle:
  def __init__(self, starting_top_speed = 100):
    self.top_speed = starting_top_speed
    self.__warnings = []  # Starts with __ is a convention to mark as "private"

  def __repr__(self):
    print("Repr...")
    return f"Top Speed: {self.top_speed}, Warnings: {self.__warnings}"

  def add_warning(self, warning_text):
    if len(warning_text) > 0:
      self.__warnings.append(warning_text)

  def warnings(self):
    return self.__warnings

  def drive(self):
    print(f"Driving, though not faster than {self.top_speed}")