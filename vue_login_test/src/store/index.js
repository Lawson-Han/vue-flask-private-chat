import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // userMuted: false
  },
  mutations: {
    mute (state, username) {
      // state.userMuted = true
      console.log(username)
      localStorage.setItem(username + '_muted', '1')
    },
    unmute (state, username) {
      // state.userMuted = false
      localStorage.setItem(username + '_muted', '0')
    }
  }
})
