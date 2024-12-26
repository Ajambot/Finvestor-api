from dotenv import load_dotenv
import requests
import os

load_dotenv()

url = "http://localhost:8000"

s = requests.session()
r = s.post(url + "/accounts/login", data = { "username": "test", "password": "test"})

headers = {
    "X-CSRFToken": s.cookies.get("csrftoken")
}

print(r.json())
print(s.cookies.get_dict())

email = os.getenv("EMAIL") 
password = os.getenv("PASSWORD")
otp = input("OTP: ")
data = {
    "email": email,
    "password": password,
    "otp": otp
}

r = s.post(url + "/wealthsimple/login", data = data, headers=headers, cookies=s.cookies.get_dict())
print(r.json())
r = s.post(url + "/wealthsimple/refresh", headers=headers, cookies=s.cookies.get_dict())
print(r.json())
r = s.get(url + "/positions", headers=headers, cookies=s.cookies.get_dict())
print(r.json())
