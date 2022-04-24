def strtobool(str):
   if str.lower() == "true":
      return True
   elif str.lower() == "false":
      return False
   else:
      raise ValueError()