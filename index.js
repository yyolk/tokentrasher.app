require('dotenv').config()
const {XummSdk} = require('xumm-sdk')
const Sdk = new XummSdk(process.env.XUMM_API_KEY, process.env.XUMM_API_SECRET)

const main = async () => {
  const appInfo = await Sdk.ping()
  console.log(appInfo.application.name)

  const request = {
    "TransactionType": "Payment",
    "Destination": "rwietsevLFg8XSmG3bEZzFein1g8RBqWDZ",
    "Amount": "31337",
    "Memos": [
      {
        "Memo": {
          "MemoData": "F09F988E20596F7520726F636B21"
        }
      }
    ]
  }

  const payload = await Sdk.payload.create(request, true)
  console.log(payload)
}

main()
