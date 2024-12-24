import promptSync from "prompt-sync";
import dotenv from "dotenv";
import fs from "fs";

dotenv.config();
const email = process.env.EMAIL;
const password = process.env.PASSWORD;
let access_token:string | undefined | null  = process.env.ACCESS_TOKEN;
let refresh_token:string | undefined | null  = process.env.REFRESH_TOKEN;
let expiry:string | undefined | null  = process.env.EXPIRY;
const baseUrl = "https://trade-service.wealthsimple.com";
const prompt = promptSync();

async function main() {
    if (access_token == "") {
        console.log("authenticating");
        await authenticate();
    }

    const curTime = Math.floor(Date.now() / 1000);
    if (curTime > Number(expiry)) {
        console.log("refreshing");
        await refresh(refresh_token);
    }

    console.log("testing");
    await testQuery();
}

main();

function updateEnvVariable(key: string, value: string | null) {
  if (value===null) {
    throw Error("Value is undefined");
  }
  let envFileContent = fs.readFileSync("./.env", "utf8");

  const regex = new RegExp(`^${key}=.*`, "m");

  if (envFileContent.match(regex)) {
    envFileContent = envFileContent.replace(regex, `${key}=${value}`);
  } else {
    envFileContent += `\n${key}=${value}`;
  }

  fs.writeFileSync("./.env", envFileContent, "utf8");

  console.log(`${key} updated successfully in .env file!`);
}

async function testQuery() {
  let response = await fetch(baseUrl + "/account/list", {
    method: "GET",
    headers: {
      Authorization: "Bearer " + access_token,
      "Content-Type": "application/json",
    },
  });
  console.log(JSON.stringify(await response.json(), null, 4));

  response = await fetch(baseUrl + "/account/positions", {
    method: "GET",
    headers: {
      Authorization: "Bearer " + access_token,
      "Content-Type": "application/json",
    },
  });
  fs.writeFileSync("./output.txt", JSON.stringify(await response.json(), null, 4), "utf8");
}

async function authenticate() {
  const otp = prompt("OTP: ");
  const response = await fetch(baseUrl + "/auth/login", {
    method: "POST",
    body: JSON.stringify({ email: email, password: password, otp: otp }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  access_token = response.headers.get("x-access-token");
  refresh_token = response.headers.get("x-refresh-token");
  expiry = response.headers.get("x-access-token-expires");
  updateEnvVariable("ACCESS_TOKEN", access_token);
  updateEnvVariable("REFRESH_TOKEN", refresh_token);
  updateEnvVariable("EXPIRY", expiry);
}

async function refresh(refresh_token: string | undefined | null) {
  if(refresh_token==null){
    throw Error("refresh_token is not defined");
  }
  const response = await fetch(baseUrl + "/auth/refresh", {
    method: "POST",
    body: JSON.stringify({ refresh_token: refresh_token }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  console.log(await response.text());
  console.log(...response.headers);
  access_token = response.headers.get("x-access-token");
  refresh_token = response.headers.get("x-refresh-token");
  expiry = response.headers.get("x-access-token-expires");
  updateEnvVariable("ACCESS_TOKEN", access_token);
  updateEnvVariable("REFRESH_TOKEN", refresh_token);
  updateEnvVariable("EXPIRY", expiry);
}