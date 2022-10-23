import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    categories: [],
    serverhost: 'http://www.morangames.xyz:3090',
    // serverhost: 'http://127.0.0.1:3090',
    token: '',
  },
  getters: {
  },
  mutations: {
    setCategories(state, categories) {
      state.categories = JSON.parse(JSON.stringify(categories))
    },
    setToken(state, token) {
      state.token = token
    },
  },
  actions: {
  },
  modules: {
  }
})
