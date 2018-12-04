from json import dumps as to_json
from jsonmerge import merge

def fail(responseCode, message, json = {}):
  print(len(json))

  if len(json) == 0:
    return to_json({
      "error": {
        "message": message
      }
    }), responseCode
  else:
    j = {
      "error": {
        "message": message
      }
    }

    

    # j["error"]["data"] = json
    j["error"].update(json)

    return (j, responseCode) 

print(fail(201, "blah", {
  "data": {
    "foo": "bar"
  }
}))