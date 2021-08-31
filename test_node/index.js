require('dotenv').config()
const {XummSdk} = require('xumm-sdk')
const Sdk = new XummSdk(process.env.XUMM_API_KEY, process.env.XUMM_API_SECRET)

const main = async () => {
  const appInfo = await Sdk.ping()
  // console.log(appInfo.application.name)

  // const request = {
  //   "TransactionType": "Payment",
  //   "Destination": "rwietsevLFg8XSmG3bEZzFein1g8RBqWDZ",
  //   "Amount": "31337",
  //   "Memos": [
  //     {
  //       "Memo": {
  //         "MemoData": "F09F988E20596F7520726F636B21"
  //       }
  //     }
  //   ]
  // }
  
  // const request = {
  //   "TransactionType": "TrustSet",
  //   // "Account": "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
  //   "LimitAmount": {
  //     "currency": "534F4C4F00000000000000000000000000000000",
  //     "value": "0",
  //     "issuer": "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz"
  //   }
  //
  // }
  //







  // const request = {
  //   "TransactionType": "TrustSet",
  //   "LimitAmount": {
  //     "currency": "YT1",
  //     "value": "100000",
  //     "issuer": "r9rLLez84biAyZFtVWHY2UfXGKvxEnvX6G"
  //   },
  //   "Flags": 131072
  // }
  // const request = {
  //   "TransactionType": "Payment",
  //   "Destination": "rDwsM7vLrWLasZrN9HmHEKqKbM5WtbJ3rQ",
  //   "Amount": {
  //     "currency": "YT1",
  //     "value": "100000",
  //     "issuer": "r9rLLez84biAyZFtVWHY2UfXGKvxEnvX6G"
  //   }
  // }
  // const request = {
  //   "TransactionType": "Payment",
  //   "Destination": "r9rLLez84biAyZFtVWHY2UfXGKvxEnvX6G",
  //   "Amount": {
  //     "currency": "YT1",
  //     "value": "100000",
  //     "issuer": "r9rLLez84biAyZFtVWHY2UfXGKvxEnvX6G"
  //   }
  // }
  // const request = {
  //   "TransactionType": "TrustSet",
  //   "LimitAmount": {
  //     "currency": "YT1",
  //     "value": "0",
  //     "issuer": "r9rLLez84biAyZFtVWHY2UfXGKvxEnvX6G"
  //   }
    const request = {
      "txjson": {
        "TransactionType": "SignIn"
      },
      "options": {
        "return_url": {
          "app": "https://tokentrasher.app",
          "web": "https://tokentrasher.app"
        }
      }
    }


  const payload = await Sdk.payload.create(request, true)
  console.log(payload)
}

main()
