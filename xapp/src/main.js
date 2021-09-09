import { createApp } from 'vue'
import App from './App.vue'

// createApp(App).mount('#app')
const app = createApp(App)

import { createI18n } from 'vue-i18n'

import { languages, defaultLocale } from './locale/index.js'
const messages = Object.assign(languages)

const i18n = createI18n({
  locale: defaultLocale,
  fallbackLocale: 'en',
  messages
})

app.use(i18n)


const urlParams = new URLSearchParams(window.location.search)
const token = urlParams.get('xAppToken') || process.env?.VUE_APP_NAME
// const theme = urlParams.get('xAppStyle') || 'LIGHT'


app.config.globalProperties.token = token
app.config.globalProperties.endpoint = process.env?.VUE_APP_API_ENDPOINT || ''
app.config.globalProperties.apiKey = process.env?.VUE_APP_XAPP_KEY || ''

app.mount('#app')
