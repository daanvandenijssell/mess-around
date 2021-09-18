import requests

# import sys

# print(sys.executable)

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "Helloworld/kipmetfriet")

print(response.json())
