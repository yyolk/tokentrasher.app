<template>
  <div class="wizard">
    <ul>
      <li 
        v-for="(step, index) in steps"
        :class="getStepClass(index)"
        :key="index"
      >
        <div>
          {{ $t(`wizard.step_${index}.header`) }}
        </div>
        <div>
          {{ $t(`wizard.step_${index}.body`) }}
        </div>
        <div>
          <div v-if="trustlines.length > 0 && index === 1">
            <ul>
              <li v-for="(trustline, index) in trustlines" :key="index">
                <a @click="burnSelect(trustline)" :key="index">
                {{ trustline.currency }}.<small>{{ ellipAccount(trustline.account) }}</small>
                {{ trustline.balance }}
                </a>
              </li>
            </ul>
          </div>
          <a @click="next()" v-if="index === activeIndex">
          {{ $t(`wizard.step_${index}.button`) }}
          </a>
        </div>
      </li>
    </ul>
    {{ accountTrustLines }}
    <h5 v-if="burnIssuer">{{ burnIssuer }} : {{ burnCurrency }} : {{ burnAmount }}</h5>
    <a v-if="finished" @click=close()>
      {{ $t('wizard.success') }}
    </a>
  </div>
</template>


<script>
import axios from 'redaxios'

// axios.defaults.headers.common['Authorization'] = this.state.token
// axios.defaults.headers.common['x-api-key'] = this.apiKey 

// const txnCallback = function(that, command) {
//   return new Promise((resolve, reject) => {
//     console.log("state is", this.state)
//     const socket = new WebSocket(this.getWebSocketUrl(this.state.nodetype))
//     socket.onopen = event => {
//       event
//       socket.send(JSON.stringify(command))
//     }
//     socket.onmessage = msg => {
//       const data = JSON.parse(msg.data)
//       if (data.error) {
//         reject(this.$t(`wizard.error.${data.error}`))
//       }
//       if (data.id == 666) {
//         resolve(data)
//         socket.close()
//       }
//     }
//     socket.onclose = msg => {
//       reject(msg)
//     }
//     socket.onerror = e => {
//       reject(e)
//     }
//   })
// }

const txnPromiseFactory = (command, webSocketUrl, $t) => {
    return new Promise((resolve, reject) => {
      const socket = new WebSocket(webSocketUrl)
      socket.onopen = () => {
        socket.send(JSON.stringify(command))
      }
      socket.onmessage = msg => {
        const data = JSON.parse(msg.data)
        if (data.error) {
          reject($t(`wizard.error.${data.error}`))
        }
        if (data.id == command.id) {
          resolve(data)
          socket.close()
        }
      }
      socket.onclose = msg => {
        reject(msg)
      }
      socket.onerror = e => {
        reject(e)
      }
    })
}


export default {
  // components: {},
  props: ['state'],
  data() {
    return {
      activeIndex: 0,
      // steps: new Array(4).fill(''),
      // steps: ['','','','','','',''],
      steps: ['', ''],
      busy: false,
      error: false,
      msg: '',
      account: '',
      trustlines: '',
      burnIssuer: '',
      burnCurrency: '',
      burnAmount: '',
      finished: false,
    }
  },
  async mounted() {
    await this.getTokenData()
    await this.subscribe()
    axios.defaults = { headers: { Authorization: this.state.token, 'x-api-key': this.apiKey } }
    this.busy = false
  },
  // computed: {
  //   trustlineMap() {
  //     this.trustlines...
  //   }
  // },
  computed: {
    accountTrustLines() {
      const accData = this.$xapp.getAccountData()
      console.log(this.$xapp.getAccountData())
      if (!accData) return {}
      const array = accData.lines
      const obj = {}

      if (Array.isArray(array) && array.length > 0) {
        array.forEach(line => {
          if (typeof obj[line.currency] === 'undefined') {
            obj[line.currency] = {
              [line.account]: line
            }
          } else {
            obj[line.currency][line.account] = line
          }
        })
      }
      return obj
    }
  },
  methods: {
    async setAccountData () {
      const account_info = await this.$rippled.send({
        command: 'account_info',
        account: this.$xapp.getAccount()
      })
      if (account_info.error === 'actNotFound') return this.$xapp.setAccountData(null)
      const account_lines = await this.$rippled.send({
        command: 'account_lines',
        account: this.$xapp.getAccount()
      })
      // if (account_lines.lines < 1) alert('no trustlines')
      const account_objects = await this.$rippled.send({
        command: 'account_objects',
        account: this.$xapp.getAccount()
      })
      const account_data = {
        account: this.$xapp.getAccount(),
        account_data: account_info.account_data,
        objects: account_objects.account_objects,
        lines: account_lines.lines
      }
      this.$xapp.setAccountData(account_data)
    },
    async getTokenData () {
      this.busy = true
      if (typeof window.ReactNativeWebView === 'undefined') {
        // set account for dev manually here
        // this.data = {
        //    account: 'r...',
        //    nodetype: 'MAINNET',
        //    // account: 'r...',
        //    // nodetype: 'TESTNET'
        // }
        // this.$xapp.setAccount(this.account)
        this.data = {
          account: 'rMtfWxk9ZLr5mHrRzJMnaE5x1fqN3oPdJ7',
          nodetype: 'TESTNET'
        }
        this.$xapp.setAccount(this.data.account)
      } else {
        try {
          this.data = await this.$xapp.getTokenData()
          this.$xapp.setAccount(this.data.account)
        } catch(e) {
          this.busy = false
          this.error = this.$t('xapp.error.get_ott_data')
          throw e
        }
      }
    },
    async subscribe() {
      this.busy = true
      try {
        const url = this.getWebSocketUrl(this.data.nodetype)
        //const ws = this.$rippled.connect(url, { NoUserAgent: true, MaxConnectTryCount: 5 })
        this.$rippled.connect(url, { NoUserAgent: true, MaxConnectTryCount: 5 })
        this.setAccountData()
        this.$rippled.send({
          command: 'subscribe',
          accounts: [this.data.account]
        })
        this.$rippled.on('transaction', tx => {
          this.setAccountData()
          this.$xapp.onTransaction(tx)
        })
        this.busy = false
        this.ready = true
        this.error = false
      } catch(e) {
        this.busy = false
        console.log(e)
        this.error = this.$t('xapp.error.subscribe_to_account')
        throw e
      }
    },
    ellipAccount(value) {
      return `${value.slice(0, 6)} ... ${value.slice(value.length-7, value.length)}`
    },
    close() {
      window.ReactNativeWebView.postMessage(JSON.stringify({
        command: 'close'
      }))
    },
    changeIndex(index) {
      if (this.activeIndex > index) this.activeIndex = index
    },
    getStepClass(index) {
      const obj = {
        current: this.activeIndex === index,
        complete: this.activeIndex > index,
        'prev-step': this.activeIndex === (index - 1),
        locked: this.activeIndex < index
      }
      return obj
    },
    openSignRequest(uuid) {
      if (typeof window.ReactNativeWebView === 'undefined') {
        // TODO if dev
        console.log('uuid:', uuid)
        // throw new Error(this.$t('wizard.error.reactNative'))
      } else {
        window.ReactNativeWebView.postMessage(JSON.stringify({
          command: 'openSignRequest',
          uuid: uuid
        }))
      }
    },
    isResolved() {
      return new Promise((resolve, reject) => {
        function message(event) {
          window.removeEventListener('message', message)
          document.removeEventListener('message', message)
          const data = JSON.parse(event.data)
          if(data.method !== 'payloadResolved') return reject('')
          if(data.reason === 'SIGNED') return resolve()
          else return reject('')
        }
        // iOS
        window.addEventListener('message', message)
        // Android
        document.addEventListener('message', message)
      })
    },
    getWebSocketUrl(nodetype) {
      switch (nodetype) {
        case 'MAINNET':
          return 'wss://xrpcluster.com'
        case 'TESTNET':
          return 'wss://testnet.xrpl-labs.com'
      }
      return 'wss://xrplcluster.com'
    },
    accountLines(account) {
      const command = {
        id: 666,
        command: 'account_lines',
        account,
        ledger_index: 'validated',
        limit: 10
      }
      const webSocketUrl = this.getWebSocketUrl(this.state.nodetype)
      const $t = this.$t
      return txnPromiseFactory(command, webSocketUrl, $t)
    },
    // accountInfo(account) {
    //   const command = {
    //     id: 666,
    //     command: 'account_objects',
    //     account: account,
    //     ledger_index: 'validated',
    //     deletion_blockers_only: true,
    //     limit: 10
    //   }
    //   return new Promise((resolve, reject) => {
    //     const socket = new WebSocket(this.getWebSocketUrl(this.state.nodetype))
    //     socket.onopen = event => {
    //       // event
    //       console.log('got event', event)
    //       socket.send(JSON.stringify(command))
    //     }
    //     socket.onmessage = msg => {
    //       const data = JSON.parse(msg.data)
    //       if (data.error) {
    //         reject(this.$t(`wizard.error.${data.error}`))
    //       }
    //       if (data.id == 666) {
    //         resolve(data)
    //         socket.close()
    //       }
    //     }
    //     socket.onclose = msg => {
    //       reject(msg)
    //     }
    //     socket.onerror = e => {
    //       reject(e)
    //     }
    //   })
    // },
    throwError(e) {
      this.error = true
      if (e === '') return
      if (e.status === 403) e = this.$t('wizard.error.403')
      if (e.status === 404) e = this.$t('wizard.error.404')
      this.msg = e
      console.log(e)
      // this.$swal(
      //   icon: 
      //
      // alert('error see console')
    },
    async next() {
      this.msg = ''
      this.busy = true
      this.error = false
      
      // const headers = 
      switch(this.activeIndex) {
        case 0:
          try {
            const payload = {
              user_token: this.token,
              txjson: {
                TransactionType: "SignIn"
              }
            }


            const res = await axios.post(`${this.endpoint}/payload`, payload)
            this.openSignRequest(res.data.uuid)
            await this.isResolved()

            const result = await axios.get(`${this.endpoint}/payload/${res.data.uuid}`)
            this.account = result.data.response.account

            console.log('account is', this.account)
            const test = await this.accountLines(this.account)
            //console.log(test)

            if (test.result.lines.length == 0) throw new Error(this.$t('wizard.error.noTrustLines'))
            this.trustlines = test.result.lines

          } catch(e) {
            this.throwError(e)
          }
          break
        case 1:
          // pick which token to trash here
          // a token to trash is a token with balances

          break
          //....
        case 2:
          break
          //....
        default:
          break
          //...
      }
      this.busy = false
      if (this.error) return null
      this.activeIndex ++
    },
    burnSelect(trustline) {
      this.burnIssuer = trustline.issuer
      this.burnCurrency = trustline.currency  
      this.burnAmount = trustline.amount
    },
  }
}

  

</script>
