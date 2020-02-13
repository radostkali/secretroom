import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    keys: {},
    user: null,
    _pubkey: null
  },
  getters: {
    KEYS: state => state.keys,
    USER: state => state.user,
    _PUBKEY: state => state._pubkey
  },
  mutations: {
    SET_KEYS: (state, keys) => {
      state.keys = keys
    },
    DELETE_KEYS: (state) => {
      state.keys = {}
    },
    SET_USER: (state, user) => {
      state.user = user
    },
    DELETE_USER: (state) => {
      state.user = {}
    },
    SET_PUBKEY: (state, _pubkey) => {
      state._pubkey = _pubkey
    },
    DELETE_PUBKEY: (state) => {
      state._pubkey = null
    }
  },
  actions: {
    SET_KEYS (context, keys) {
      context.commit('SET_KEYS', keys)
    },
    DELETE_KEYS (context) {
      context.commit('DELETE_KEYS')
    },
    SET_USER (context, user) {
      context.commit('SET_USER', user)
    },
    DELETE_USER (context) {
      context.commit('DELETE_KEYS')
    },
    SET_PUBKEY (context, _pubkey) {
      context.commit('SET_PUBKEY', _pubkey)
    },
    DELETE_PUBKEY (context) {
      context.commit('DELETE_PUBKEY')
    }
  }
})
