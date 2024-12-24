import requests

r = requests.post("http://localhost:8000/accounts/login/", {"username": "test", "password": "test"})
r.raise_for_status()
print(r.json(), r.status_code)
