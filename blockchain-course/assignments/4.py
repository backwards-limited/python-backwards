def func(f, *args):
  return f(args)

def fToRun(*args):
  if len(args[0]) > 0:
    return "hi there from fToRun"
  else:
    return f"hi there from fToRun with given args: {args}"
    
print(f"fToRun no parameters: {func(fToRun)}")
print(f"fToRun with parameters: {func(fToRun, 'yo')}")

print(f"Anonymous: {func(lambda *args: f'hi there {args}', 'anonymous args')}")
