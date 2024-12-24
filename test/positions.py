import requests
import json

url = "http://localhost:8000/positions"
r = requests.get(url)
print("Before POST:")
print(json.dumps(r.json()))

requests.post(url, data = {"account_id": "tfsa-1234", "symbol": "XBAL", "book_value": 120, "amount": 1, "user": 1})

print("After POST:")
r = requests.get(url)
print(json.dumps(r.json()))
