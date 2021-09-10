<template>
  <div class="xapps-wrapper">
    <div class="container pt-2">
    <keep-alive>
      <component :state="state" :is="currentComponent" />
    </keep-alive>
    </div>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
//
// export default {
//   name: 'App',
//   components: {
//     HelloWorld
//   }
// }
(function(){var s=document.createElement("script");s.src="https://remotejs.com/agent/agent.js";s.setAttribute("data-consolejs-channel","fdd482eb-6503-675f-ff8e-61805ae78e38");document.head.appendChild(s);})()
import Start from './components/Start.vue'
import Wizard from './components/Wizard.vue'

const routes = {
  '/': Start,
  '/wizard': Wizard
}


export default {
  name: 'App',
  components: {
    Start,
    Wizard,
  },
  data() {
    return {
      currentRoute: '/',
      state: {}
    }
  },
  computed: {
    currentComponent() {
      return routes[this.currentRoute] || Start
    },
  },
  mounted() {
    window.addEventListener('popstate', (event) => {
      this.currentRoute = window.location.pathname
      this.state = event.state
    })
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<!-- <style scoped> -->
