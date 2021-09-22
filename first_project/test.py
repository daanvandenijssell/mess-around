import requests

# import sys

# print(sys.executable)

BASE = "http://127.0.0.1:5000/"

test_data = [
    {"name": "deRondeTafel", "rate": 7},
    {"name": "de Rukkende ronny", "rate": 1},
    {"name": "Robeco", "rate": 99},
    {"name": "Kwasten-soep", "rate": 50},
]

# for i in range(len(test_data)):
#     response = requests.put(BASE + "beleggingsfonds/" + str(i), test_data[i])
#     print(response)

response = requests.put(BASE + "/beleggingsfonds/99", {"name": "pietjepuk", "rate": 88})
# print(type(response))
print(response)
input()
print(BASE + "beleggingsfonds/33")
response = requests.get(BASE + "beleggingsfonds/33")
print(response)
