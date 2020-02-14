<template>
  <div class="content">
    <div class="main-block">
      <v-container>
        <v-row align="center" justify-space-between>
          <v-col xs12 fill-height >
            <h1 class="main-title">Fast encrypted<br>one on one chatting.</h1>
            <p class="main-text">Private end-to-end GPG encrypted chatting<br>in one click.</p>
            <new-room ref="newroom">Create room</new-room>
          </v-col>
          <v-col xs12>
            <v-img class="image" contain src="/static/img/rush-12.png"></v-img>
          </v-col>
        </v-row>
      </v-container>
    </div>
    <div class="text-block">
      <v-stepper>
        <v-stepper-header>
          <v-stepper-step
            @click="$refs.newroom.createRoom()"
            style="cursor: pointer"
            step="1" complete complete-icon="mdi-shield-key-outline">Create room</v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step step="2" complete complete-icon="mdi-link-variant">Share link</v-stepper-step>
          <v-divider></v-divider>
          <v-stepper-step step="3" complete complete-icon="mdi-chat-outline">Chat</v-stepper-step>
        </v-stepper-header>
      </v-stepper>
    </div>
    <div class="info-container">
      <v-container>
        <v-row justify="center">
          <v-col xs12>
            <div class="info-block">
              <v-img class="info-image" contain src="/static/img/client-side.png"></v-img>
              <h2 class="info-title">Client-side encryption</h2>
              <p class="info-text">All messages are encrypted on the client side<br>
                with a uniq key pair generated for every new room.</p>
            </div>
          </v-col>
          <v-col xs12>
            <div class="info-block">
              <v-img class="info-image" contain src="/static/img/pgp.png"></v-img>
              <h2 class="info-title">PGP</h2>
              <p class="info-text">SECRET ROOM uses the JavaScript implementation of the OpenPGP protocol
                <a href="https://github.com/openpgpjs/openpgpjs">OpenPGP.js</a></p>
            </div>
          </v-col>
        </v-row>
        <v-row class="mt-9" justify="center">
          <v-col xs12>
            <div class="info-block">
              <v-img class="info-image" contain src="/static/img/no-storing.png"></v-img>
              <h2 class="info-title">No server storage</h2>
              <p class="info-text">Messages are not stored in any database.<br>
                The application uses <a href="https://redis.io/">Radis</a> only to exchange public keys.</p>
            </div>
          </v-col>
          <v-col xs12>
            <div class="info-block">
              <v-img class="info-image" contain src="/static/img/open-source.png"></v-img>
              <h2 class="info-title">Open source</h2>
              <p class="info-text">SECRET ROOM is an open source application.<br>
                Find code on <a href="https://github.com/radostkali/secretroom">GitHub</a></p>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </div>
    <p class="source">Images from icons8.com and absurd.design</p>
  </div>
</template>

<script>
import NewRoom from './NewRoom'

export default {
  components: { NewRoom },
  data () {
    return {
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

.main-block {
  display: flex;
  justify-content: center;
}

.image {
  width: 23rem;
}

.main-title {
  font-weight: 500;
  margin-bottom: 1rem;
}

.main-text {
  color: #b3b3b3;
}

.text-block {
  margin-top: 7rem;
  width: 70%;
}

.info-container {
  margin-top: 7rem;
}

.info-block {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}

.info-image {
  width: 21rem;
}

.info-title {
  font-weight: 500;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.info-text {
  font-size: 1.1rem;
  color: #b3b3b3;
}

.source {
  opacity: 0.3;
  margin-top: 7rem;
}

</style>
