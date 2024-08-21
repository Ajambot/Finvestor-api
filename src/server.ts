import promptSync from "prompt-sync"
import dotenv from "dotenv"

dotenv.config()

const email = process.env.EMAIL
const password = process.env.PASSWORD
const baseUrl = "https://trade-service.wealthsimple.com"
const prompt = promptSync();

async function test() {
    const otp = prompt("OTP: ")
    const response = await fetch(baseUrl+"/auth/login", {
        method: "POST",
        body: JSON.stringify({email: email, password: password, otp: otp}),
        headers: {
            "Content-Type": "application/json"
        }
    })
    console.log(await response.json());
    console.log(...response.headers)
}

test();