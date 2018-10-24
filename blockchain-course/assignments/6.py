from json import dumps as to_json
from json import loads as from_json
from pickle import dumps as pickle
from pickle import loads as unpickle
from textwrap import dedent as strip_margin

def ask():
  return input(strip_margin("""
    Give me input or
    - 'q' to quit
    - 'r' to view file
    - 'rj' to view JSON file
    - 'rp' to view Pickle file
    - 'wj' to write JSON to file
    - 'wp' to write Pickle to file
    """
  ))

def main(request):
  file_name = "6.out"
  request = request.lower()

  if request != "q":
    try:
      if request == "r":
        with open(file_name, "r") as file:
          print(file.read())
      elif request == "rj":
        with open(file_name, "r") as file:
          print(from_json(file.read()))
      elif request == "rp":
        with open(file_name, "rb") as file:
          print(unpickle(file.read()))
      elif request == "wj":
        with open(file_name, "wt") as file:
          file.write(to_json([input(": ")]))
      elif request == "wp":
        with open(file_name, "wb") as file:
          file.write(pickle(input(": ")))
      else:
        with open(file_name, "w") as file:
          file.write(request)
    
    except FileNotFoundError:
      print("No existing file to load")
    
    main(ask())

main(ask())
