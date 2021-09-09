<template>
  <div class="wizard">
    <ul>
      <li 
        v-for="(step, index) in steps"
        :class="getStepClass(index)"
        :key="index"
      >
        <div>
          {{ $t(`wizard.step_${index}.body`) }}
        </div>
        <div>
          {{ $t(`wizard.step_${index}.button`) }}
        </div>
      </li>
    </ul>
  </div>
</template>


<script>
import axios from 'redaxios'

export default {
  // components: {},
  props: ['state'],
  data() {
    return {
      activeIndex: 0,
      // steps: new Array(4).fill(''),
      steps: ['','','','','','',''],
      // steps: ,
      busy: false,
      error: false,
      msg: '',
      account: '',
      // trustline: '',
      // issuer: '',
      finished: false,
    }
  },
  mounted() {
    axios.defaults.headers.common['Authorization'] = this.state.token
    axios.defaults.headers.common['x-api-key'] = this.apiKey 
  },
  methods: {
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
      uuid
      alert('open sign request')
      // if (typeof
      //
    },
    isResolved() {
      return new Promise((resolve, reject) => {
        function message(event) {
          window.removeEventListener('message', message)
          document.removeEventListeneter('message', message)
          const data = JSON.parse(event.data)
          if(data.method !== 'payloadResolved') return reject('')
          if(data.reason === 'SIGNED') return resolve()
          else return reject('')
        }
        // iOS
        window.addEventListner('message', message)
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
    accountInfo(account) {
      const command = {
        id: 666,
        command: 'account_objects',
        account: account,
        ledger_index: 'validdated',
        deletion_blockers_only: true,
        limit: 10
      }
      return new Promise((resolve, reject) => {
        const socket = new WebSocket(this.getWebSocketUrl(this.state.nodetype))
        socket.onopen = event => {
          event
          socket.send(JSON.stringify(command))
        }
        socket.onmessage = msg => {
          const data = JSON.parse(msg.data)
          if (data.error) {
            // reject(this.$t(`wizard.error.${data.error}`))
            // reject(this.$t(`wizard.error.${data.error}`))
            reject()
          }
          if (data.id == 666) {
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
    },
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
      alert('error see console')
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

            // const res = await axios.post(`${this.endpoint}/payload`, payload, headers)
            const res = await axios.post(`${this.endpoint}/payload`, payload)
            this.openSignRequest(res.data.uuid)
            await this.isResolved()
            // const result = await axios.get(`${this.endpoint}/payload/${res.data.uuid}`, headers)
            const result = await axios.get(`${this.endpoint}/payload/${res.data.uuid}`)
            this.account = result.data.response.account

            // test for trustlines here?
            // throw err if there are any?
            // from account-merge:
            // if (test.result.account_objects.length >= 1) throw new Error(this.$t('wizard.error.hasObjects'))

          } catch(e) {
            this.throwError(e)
          }
          break
        case 1:
          break
          //....
        case 2:
          break
          //....
        default:
          break
          //...
      }
    },
  }
}

  

</script>
