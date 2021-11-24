require('dotenv').config()
const crypto = require('crypto')


const xAppToken = process.env.X_APP_TOKEN
const myXummAppSecret =  process.env.XUMM_API_SECRET
const myXummDeviceId = process.env.XUMM_DEVICE_ID

const data = `${xAppToken}.${myXummAppSecret}.${myXummDeviceId}`
const hash = crypto
  .createHash('sha1')
  .update(data.toUpperCase())
  .digest('hex')

console.log(data, hash)
