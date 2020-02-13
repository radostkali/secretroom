<template>
  <div>
    <div @click="dialog = true">
      <slot></slot>
    </div>
    <v-dialog v-model="dialog" persistent max-width="700">
      <v-card>
        <v-card-title><span>Cryptographic keys</span></v-card-title>
        <v-card-text style="text-align: left">
          <h3>My public key</h3>
          <br>
          <v-textarea
            outlined
            no-resize
            readonly
            max-height="300"
            v-model="keys.pubkey">
          </v-textarea>
          <h3>Second user public key</h3>
          <br>
          <v-textarea
            outlined
            no-resize
            readonly
            max-height="300"
            v-model="_pubkey">
          </v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      dialog: false
    }
  },
  computed: {
    ...mapGetters({
      _pubkey: '_PUBKEY',
      keys: 'KEYS'
    })
  }
}
</script>
