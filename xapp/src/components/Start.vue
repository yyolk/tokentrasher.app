<template>

<h1>uhh</h1>
<a v-if="ready" @click.prevent="next()" >
{{ $t( 'start.button' ) }}
</a>
</template>


<script>
import axios from 'redaxios'


export default {
  //components..
  data() {
    return {
      ott: Object,
      busy: true,
      ready: false,
      data: '',
      error: ''
    }
  },
  async mounted() {
    await this.getTokenData()
  },
  methods: {
    async getTokenData() {
      try {
        const res = await axios({
          method: 'get',
          url: `${this.endpoint}/xapp/ott/${this.token}`,
          headers: { 'x-api-key': this.apiKey }
        })
        this.data = res.data
        this.ready = true
        this.error = false
      } catch(e) {
        console.error(e)
        this.error = this.$t('start.error')
      }
      this.busy = false
    },
    next() {
      // window.history.pushState('this.data', 'state', '/non-existant')
      window.history.pushState('this.data', 'state', '/wizard')
      const popStateEvent = new PopStateEvent('popstate', { state: this.data })
      dispatchEvent(popStateEvent)
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
