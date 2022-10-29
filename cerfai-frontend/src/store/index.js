import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    categories: [],
    // serverhost: 'http://tag.52dcr.cn:3090', 
    serverhost: 'http://127.0.0.1:3090',
    // serverhost: 'http://tmp.kromiose.top:3090', 

    token: '',
  },
  getters: {
  },
  mutations: {
    setCategories(state, categoriesList) {
      let sortedCategories = { l1: [], l2: {} }
      categoriesList.forEach(element => {
        if (element.level == 1) {
          element.id = parseInt(parseInt(element.id) / 100);
          sortedCategories.l1.push(element);
        } else {
          element.id = parseInt(element.id)
          let parentId = parseInt(element.id / 100)
          
          if (sortedCategories.l2[parentId] === undefined)
            sortedCategories.l2[parentId] = [];
          sortedCategories.l2[parentId].push(element);
        }
      });
      state.categories = sortedCategories
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
