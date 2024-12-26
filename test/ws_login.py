from dotenv import load_dotenv
import requests
import os

load_dotenv()

url = "http://localhost:8000"
email = os.getenv("EMAIL") 
password = os.getenv("PASSWORD")
otp = input("OTP: ")
data = {
    "email": email,
    "password": password,
    "otp": otp
}

s = requests.session()
csrf = s.cookies.get("csrftoken")
headers = {"X-CSRFToken": csrf}
r = s.post(url + "/wealthsimple/login", data = data, headers=headers)
print(r.json(), r.status_code)
print(s.cookies.get_dict())
res = s.post(url + "/wealthsimple/refresh", headers=headers, cookies=s.cookies.get_dict())
print(res.json())
res = s.get(url + "/positions", headers=headers, cookies=s.cookies.get_dict())
print(res.json())
