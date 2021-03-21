import os


print(os.path.realpath(__file__))

scriptPath = os.path.dirname(os.path.realpath(__file__))
print(scriptPath)