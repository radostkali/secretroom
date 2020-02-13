<template>
  <v-btn outlined @click="createRoom">
    <v-icon>mdi-shield-key-outline</v-icon>
    <slot></slot>
  </v-btn>
</template>

<script>
import axios from 'axios'

const urlCreateRoom = '/api/create_room'

export default {
  data () {
    return {
      roomId: null
    }
  },
  methods: {
    createRoom () {
      this.$socket.emit('leave', {command: 'leave'})
      this.$store.dispatch('DELETE_KEYS')
      this.$store.dispatch('DELETE_USER')
      this.$store.dispatch('DELETE_PUBKEY')
      this.$router.push({name: 'main'})
      axios.post(urlCreateRoom)
        .then(response => {
          this.roomId = response.data.room_id
          this.$router.push({name: 'room', params: {'roomId': this.roomId}})
        })
    }
  }
}
</script>
