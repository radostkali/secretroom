<template>
  <div class="chat-wrapper">
    <div class="chat-box">
      <div class="message-area">
        <div class="writing-line">
          <div class="writing-block" :class="writingHe ? 'writing' : ''">
            <p class="writing-message">User is typing...</p>
          </div>
        </div>
        <div v-for="(message, i) in messages" :key="i" class="message-line">
          <div class="message-block"
            :class="(message.user === user) ? 'my-message' :
              (message.user === 0) ? ('sys-message-' + message.color) : 'not-my-message'">
            <v-avatar class="avatar" v-if="(message.user !== user && message.user !== 0)" color="#369dd8" size="24">
              <v-icon small color="#FFFFF2">mdi-account</v-icon>
            </v-avatar>
            <p class="message">
              {{message.message}}
            </p>
            <v-icon class="delivered" small v-if="(message.user === user && !deliveredUUIDs.includes(message.id))">mdi-check</v-icon>
            <v-icon class="delivered" small v-if="(message.user === user && deliveredUUIDs.includes(message.id))">mdi-check-all</v-icon>
          </div>
        </div>
      </div>
    </div>
    <div class="text-box">
      <v-textarea
        no-resize
        auto-grow
        rows="1"
        :disabled="disable"
        placeholder="Write a message..."
        v-model="messageText"
        @keypress.enter.prevent="sendMessage"
        append-icon="mdi-send"
        @click:append="sendMessage">
      </v-textarea>
    </div>
    <div class="action-btns">
      <new-room class="action-btn">New room</new-room>
      <v-btn class="action-btn" text @click="leave(false)">Leave room</v-btn>
    </div>
  </div>
</template>

<script>
import NewRoom from './NewRoom'
import { mapGetters } from 'vuex'
import * as openpgp from '../../static/openpgp/openpgp.min.js'

const newMessageSound = new Audio('../../static/sounds/just-like-that.mp3')

export default {
  props: ['url'],
  components: { NewRoom },
  data () {
    return {
      messages: [],
      joined: false,
      messageText: '',
      deliveredUUIDs: [],
      encryptedMessage: null,
      disable: true,
      writingMe: false,
      writingHe: false
    }
  },
  sockets: {
    room (data) {
      let state = data.state
      // User connect to room
      if (state === 'connected') {
        let _pubkey = (this.user === 1) ? data.pubkey_2 : data.pubkey_1
        if (_pubkey === '') {
          this.messages.push({
            message: 'Waiting for second user...',
            user: 0,
            color: 'default'
          })
          this.messages.push({
            message: 'Send him this link: ' + this.url,
            user: 0,
            color: 'default'
          })
        } else {
          this.$store.dispatch('SET_PUBKEY', _pubkey)
          this.messages.push({
            message: 'Second user here. Let\'s chat...',
            user: 0,
            color: 'success'
          })
          this.disable = false
        }
      // User diconnect
      } else if (state === 'disconnected') {
        this.messages.push({
          message: 'Second user has left the room...',
          user: 0,
          color: 'end'
        })
        this.$store.dispatch('DELETE_PUBKEY')
        this.disable = true
      // User reconnect
      } else if (state === 'reconnecting') {
        this.messages.push({
          message: 'Second user is trying to reconnect...',
          user: 0,
          color: 'default'
        })
        this.disable = true
      // User writing
      } else if (state === 'writing') {
        if (data.user !== this.user) {
          this.writingHe = data.status === 1
        }
      // New message
      } else if (state === 'message') {
        if (data.user === this.user) {
          this.deliveredUUIDs.push(data.id)
        } else {
          let p = this.decryptMessage(data.message, this)
          p.then((decrypted) => {
            let msg = {
              message: decrypted,
              user: data.user
            }
            let el = this.$el.getElementsByClassName('chat-box')[0]
            let scroll = false
            if ((el.scrollTop + el.offsetHeight) > (el.scrollHeight - 50)) {
              scroll = true
            }
            this.messages.push(msg)
            newMessageSound.play()
            this.$nextTick(function () {
              el.scrollTop = (scroll) ? el.scrollHeight : el.scrollTop
            })
          })
        }
      }
    }
  },
  methods: {
    join (roomId) {
      this.$socket.emit('join', {room: roomId, user: this.user})
    },
    leave (soft) {
      this.messages = []
      if (soft) {
        this.$socket.emit('leave', {command: 'reconnect'})
      }
      if (!soft) {
        this.$store.dispatch('DELETE_KEYS')
        this.$store.dispatch('DELETE_USER')
        this.$store.dispatch('DELETE_PUBKEY')
        this.$socket.disconnect()
        this.$router.push({name: 'main'})
      }
    },
    sendMessage () {
      if (this._pubkey && this.messageText !== '') {
        this.disable = true
        let p = this.encryptMessage(this.messageText, this)
        p.then((encrypted) => {
          let uuid = this.$uuid.v4()
          let data = {
            encrypted: encrypted,
            user: this.user,
            id: uuid
          }
          this.messages.push({
            message: this.messageText,
            user: this.user,
            id: uuid
          })
          this.messageText = ''
          this.$nextTick(function () {
            let el = this.$el.getElementsByClassName('chat-box')[0]
            el.scrollTop = el.scrollHeight
          })
          this.$socket.emit('message', data)
          this.disable = false
          this.$nextTick(function () {
            let el = this.$el.getElementsByTagName('textarea')[0]
            el.focus()
          })
        })
      } else {
        console.log('Waiting for second user')
      }
    },
    encryptMessage: async (message, self) => {
      const privKeyObj = (await openpgp.key.readArmored(self.keys.privkey)).keys[0]
      await privKeyObj.decrypt(self.keys.passphrase)
      const options = {
        message: openpgp.message.fromText(message),
        publicKeys: (await openpgp.key.readArmored(self._pubkey)).keys,
        privateKeys: [privKeyObj],
        compression: openpgp.enums.compression.zip
      }
      let encrypted = openpgp.encrypt(options).then(ciphertext => {
        return ciphertext.data
      })
        .then(encrypted => {
          return encrypted
        })
      return encrypted
    },
    decryptMessage: async (encrypted, self) => {
      const privKeyObj = (await openpgp.key.readArmored(self.keys.privkey)).keys[0]
      await privKeyObj.decrypt(self.keys.passphrase)
      const options = {
        message: await openpgp.message.readArmored(encrypted),
        publicKeys: (await openpgp.key.readArmored(self._pubkey)).keys,
        privateKeys: [privKeyObj],
        compression: openpgp.enums.compression.zip
      }
      let decrypted = openpgp.decrypt(options).then(plaintext => {
        return plaintext.data
      })
        .then(decrypted => {
          return decrypted
        })
      return decrypted
    }
  },
  watch: {
    _pubkey (val) {
      if (val === '' || val === null) {
        this.disable = true
      }
    },
    messageText (val) {
      if (val === '' && this.writingMe === true) {
        this.writingMe = false
        this.$socket.emit('writing', {status: 0})
      } else if (val !== '' && this.writingMe === false) {
        this.writingMe = true
        this.$socket.emit('writing', {status: 1})
      }
    }
  },
  created () {
    if (this._pubkey === '' || this._pubkey === null) {
      this.disable = true
    } else {
      this.disable = false
    }
  },
  computed: {
    ...mapGetters({
      user: 'USER',
      keys: 'KEYS',
      _pubkey: '_PUBKEY'
    })
  }
}
</script>

<style scoped>
.chat-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chat-box {
  min-height: 3rem;
  max-height: 23rem;
  background: #ebebeb71;
  overflow: auto;
}

.chat-box, .text-box {
  width: 80%;
  max-width: 53rem;
}

.text-box {
  margin-bottom: 1rem;
}

@media screen and (max-width: 600px) {
  .chat-box {
    width: 100%;
    max-height: 70vh;
    height: 70vh;
  }
  .text-box {
    width: 95%;
  }
}

.message-area {
  padding: 1rem;
  padding-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  position: relative;
}

.message-line {
  width: 100%;
  margin-bottom: 0.5rem;
}

.avatar {
  float: left;
  margin-right: 0.5rem;
}

.message-block {
  border-radius: 1rem;
  padding: 0.5rem 1.5rem;
  width: fit-content;
  max-width: 90%;
  display: flex;
  align-items: flex-end;
}

.my-message {
  float: right;
  background: #87c1e2;
  padding-right: 0.5rem;
}

.delivered {
  margin-left: 0.5rem;
}

.not-my-message {
  background: #FFFFF2;
  padding-left: 0.5rem;
  float: left;
}

.sys-message-default {
  background: #a0d6ce;
}

.sys-message-success {
  background: #9ee4a9;
}

.sys-message-end {
  background: #f18c85;
}

.message {
  margin: 0;
  width: 100%;
  color: black;
  text-align: left;
  word-wrap: break-word;
}

.action-btns {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.action-btn {
  margin: 0 0.5rem;
}

.writing-line {
  position: absolute;
  height: 2.5rem;
  bottom: 0;
  left: 50%;
  transform: translate(-50%, 0);
  overflow: hidden;
}

.writing-block {
  border-radius: 0.7rem;
  background: #ffffff;
  transition: 0.3s all ease-out;
  padding: 0.3rem 0.5rem;
  transform: translate(0, 100%);
  opacity: 0;
}

.writing.writing-block {
  transform: translate(0, 0);
  opacity: 1;
}

.writing-message {
  font-size: 0.8rem;
  margin: 0;
}
</style>
