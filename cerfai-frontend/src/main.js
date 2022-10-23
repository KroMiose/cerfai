import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// 导入 element-ui
import './plugins/element.js'

// 导入 axios
import axios from 'axios'
import VueAxios from 'vue-axios'
axios.defaults.withCredentials = true // 让axios请求携带cookie
Vue.prototype.$http = axios
Vue.use(VueAxios, axios)

// 导入 VueClipboard
import VueClipboard from 'vue-clipboard2'
Vue.use(VueClipboard)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
