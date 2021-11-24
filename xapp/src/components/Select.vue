<template>
  <div @click.self="$emit('close')">
  Close?
  </div>
  <ul>
    <template v-for="(item, currency, index) in currencyObject" :key="index">
      <!-- <li @click="setCurrency(currency)" v-if="!filterCurrency(currency)"> -->
      <!-- <li @click="setTarget(item, currency)"> -->
      <!-- <li @click="$emit('selectedCurrency')"> -->
      <!-- <li @click=""> -->
      <!-- <li @click="$emit('update:currency', currency) ; $emit('update:issuer', issuer)" v-for="(line, issuer) in item" :key="issuer"> -->
      <!-- <li @click="setTarget(currency, issuer)" v-for="(line, issuer) in item" :key="issuer"> -->
      <template v-for="(line, issuer) in item" :key="issuer">
        <div style="padding:4px;background-color:red;margin:3px;" @click="setTarget(currency, issuer, line.balance)">
           <span>{{ $xapp.currencyCodeFormat(currency, 16) }}</span>
           <span>{{ issuer }} {{ line.balance }}</span>
        <!-- <ul> -->
        <!--   <li -->
        <!--     v-for="(line, index) in item" -->
        <!--     :key="index" -->
        <!--   > -->
        <!--     {{ line.account }} {{ line.balance }} -->
        <!--   </li> -->
        <!-- <span>{{ item[Object.keys(item)[0]] }} {{ index }}</span> -->
        <!-- </ul> -->
        </div>

      </template>
    </template>
  </ul>
  <!-- <h4>Isuuer: {{ issuer }}</h4> -->
  <!-- <h4>Currency {{ currency}}</h4> -->
</template>

<script>

export default {
  // props: [],
  // emits: ['selectedCurrency', 'close'],
  props: {
    currency: String,
    issuer: String,
    balance: Number,
  },
  emits: ['update:currency', 'update:issuer', 'update:balance'],
  // emits: ['selectedCurrency'],
  // data() {
  //   return {
  //     currency: '',
  //     issuer: '',
  //   }
  // },
  computed: {
    currencyObject() {
      return this.accountTrustLines
    },
    accountTrustLines() {
      const accData = this.$xapp.getAccountData()
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
    setTarget(currency, issuer, balance) {
      // console.log("you want me to set currency to", currency)
      // this.selectedCurrency = currency
      console.log("you want me to set target to", currency, issuer)
      // this.selectedCurrency = currency
      // this.selectedIssuer = issuer
      // this.currency = currency
      // this.issuer = issuer
      // console.log('this is', this.selectedIssuer, this.selectedCurrency)
      this.$emit('update:currency', currency)
      this.$emit('update:issuer', issuer)
      this.$emit('update:balance', balance)
      // this.$emit('selectedCurrency')
      console.log('this is', this.issuer, this.currency)
      // this.$emit('sselectedCurrencyelectedCurrency', this.data)
      // this.$emitter.emit('selectedCurrency')
    },
  },
}

</script>
