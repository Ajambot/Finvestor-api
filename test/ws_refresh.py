import requests
from dotenv import load_dotenv
import os

load_dotenv()

s = requests.session()
csrf = s.cookies.get("csrftoken")
headers = {"X-CSRFToken": csrf}

email = os.getenv("EMAIL")
pwrd = os.getenv("PASSWORD")
otp = input("OTP: ")

r = s.post("http://localhost:8000/wealthsimple/login", {"email": email, "password": pwrd, "otp": otp}, headers=headers)
print(s.headers)
r = s.post("http://localhost:8000/wealthsimple/token/refresh", headers=headers, cookies=s.cookies.get_dict())
print(r.json(), r.status_code)
