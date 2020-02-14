import Vue from 'vue'
import App from './App'
import router from './router'
import vuetify from '@/plugins/vuetify'
import {store} from './store'
import VueSocketIO from 'vue-socket.io'
import VueClipboard from 'vue-clipboard2'
import UUID from 'vue-uuid'

Vue.use(UUID)
Vue.use(VueClipboard)
Vue.use(new VueSocketIO({
  debug: false,
  options: { autoConnect: false },
  // connection: 'http://localhost:5000'
  connection: 'https://' + location.host
}))
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  vuetify,
  render: h => h(App)
})
