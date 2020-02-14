<template>
  <div class="content">
    <div class="header">
      <h1 class="room-title">Room {{ $route.params.roomId }}</h1>
      <div class="btn-panel">
        <v-btn title="Copy link" x-small text
          v-clipboard:copy="url"
          v-clipboard:success="onCopy">
          <v-icon small :color="(copied) ? 'success' : ''">mdi-content-copy</v-icon>
        </v-btn>
        <my-keys v-if="connected">
          <v-btn title="Public keys" x-small text :disabled="keys === {}">
            <v-icon small>mdi-key-variant</v-icon>
          </v-btn>
        </my-keys>
        <v-btn v-if="connected" title="Reconnect" x-small text @click="reconnect">
          <v-icon small>mdi-refresh</v-icon>
        </v-btn>
      </div>
    </div>
    <p v-if="!error && !connected">
      <v-progress-circular :value="progress"></v-progress-circular>
      <span>{{ progressText }}</span>
    </p>
    <div class="error-block" v-if="error">
      <p class="error-msg">Can't enter this room!</p>
      <new-room>Create new room</new-room>
    </div>
    <chat :class="connected ? '' : 'invisible'" ref="chat" :url="url"></chat>
  </div>
</template>

<script>
import axios from 'axios'
import openpgp from '../../static/openpgp/openpgp.min.js'
import { mapGetters } from 'vuex'
import NewRoom from './NewRoom'
import MyKeys from './MyKeys'
import Chat from './Chat'

openpgp.initWorker({ path: '/static/openpgp/openpgp.worker.min.js' })

const urlCheckRoom = '/api/check_room'
const urlSendPubkey = '/api/send_pubkey'
const urlVerifyPubkey = '/api/verify_pubkey'

export default {
  components: { NewRoom, MyKeys, Chat },
  data () {
    return {
      progress: 0,
      progressText: '',
      error: false,
      connected: false,
      copied: false
    }
  },
  methods: {
    checkRoom () {
      this.error = false
      this.connected = false
      this.progressText = 'Checking room'
      this.progress = 1
      axios.get(urlCheckRoom, {
        params: {
          room_id: this.roomId
        }
      })
        .then(response => {
          let status = response.data.status
          if (status === 'error') {
            this.$router.push({name: 'notFound'})
          } else if (status === 'success') {
            this.progress = 30
            this.$store.dispatch('SET_USER', response.data.user)
            this.generateKeyPair()
          } else if (status === 'reconnected') {
            if (this.keys !== {}) {
              this.progress = 30
              this.$store.dispatch('SET_USER', response.data.user)
              this.verifyPubkey()
            } else {
              this.error = true
            }
          }
        })
    },
    generateKeyPair () {
      this.progressText = 'Generating keys'
      const options = {
        userIds: [{ name: 'User_' + this.roomId, email: 'jon@example.com' }],
        numBits: 4096,
        passphrase: Math.random().toString(36).substr(2, 8) + this.roomId
      }
      let self = this
      openpgp.generateKey(options).then(function (key) {
        let keys = {
          privkey: key.privateKeyArmored,
          pubkey: key.publicKeyArmored,
          revocationSignature: key.revocationSignature,
          passphrase: options.passphrase
        }
        self.$store.dispatch('SET_KEYS', keys)
        self.progress = 70
        self.sendPubkey()
      })
    },
    sendPubkey () {
      this.progressText = 'Sending public key to server'
      axios.post(urlSendPubkey, {
        pubkey: this.keys.pubkey
      })
        .then(response => {
          let status = response.data.status
          if (status === 'success') {
            this.connected = true
            this.$refs.chat.messages = []
            this.progress = 100
          } else if (status === 'error') {
            this.error = true
          }
        })
    },
    deleteKeys () {
      let options = { key: openpgp.key.readArmored(this.keys.privkey).keys[0] }
      let self = this
      openpgp.revokeKey(options).then(function (key) {
        self.$store.dispatch('DELETE_KEYS')
      })
    },
    verifyPubkey () {
      this.progressText = 'Trying to reconnect'
      axios.post(urlVerifyPubkey, {
        pubkey: this.keys.pubkey
      })
        .then(response => {
          let status = response.data.status
          if (status === 'success') {
            this.connected = true
            this.progress = 100
          } else if (status === 'error') {
            this.generateKeyPair()
          }
        })
    },
    reconnect () {
      this.$refs.chat.leave(true)
      this.checkRoom()
    },
    onCopy () {
      this.copied = true
      let self = this
      setTimeout(function () {
        self.copied = false
      }, 3000)
    }
  },
  created () {
    this.checkRoom()
    this.$socket.connect()
  },
  computed: {
    roomId: function () {
      return this.$route.params.roomId
    },
    url: function () {
      return window.location.origin + '/' + this.$route.params.roomId
    },
    ...mapGetters({
      keys: 'KEYS'
    })
  },
  watch: {
    $route (to, from) {
      this.checkRoom()
    },
    connected (val) {
      if (val) {
        this.$refs.chat.join(this.roomId)
      }
    }
  }
}
</script>

<style scoped>
.content {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.header {
  margin-top: 5rem;
  margin-bottom: 3rem;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}

@media screen and (max-width: 600px) {
  .header {
    margin-top: 1rem;
    margin-bottom: 1rem;
  }

  .room-title {
    font-size: 1.2rem;
  }
}

.btn-panel {
  display: flex;
  justify-content: center;
  align-items: center;
}

.small-btn {
  height: 3rem;
  width: 3rem;
}

.invisible {
  display: none !important;
}

.room-title {
  margin-right: 0.5rem;
}

.error-block {
  margin-top: 3rem;
  display: flex;
  flex-direction: column;
}

.error-msg {
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}
</style>
