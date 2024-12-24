from dotenv import load_dotenv
import requests
import os
import json

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

r = requests.post(url + "/wealthsimple/login", data = data)
aToken = r.cookies.get('ws-access-token')

res = requests.get(url + "/wealthsimple/refresh", headers={"ws-access-token" : aToken})
f = open("test/output.json", "w")
f.write(json.dumps(res.json(), indent=4))
f.close()
