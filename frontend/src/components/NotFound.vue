<template>
  <div class="content">
    <v-img class="image" contain src="/static/img/fogg-page-not-found-1.png"></v-img>
    <p class="title">404 - Page Not Found</p>
    <router-link :to="'/'" class="link">Go main</router-link>
    <br>
    <p class="source">Image from icons8.com</p>
  </div>
</template>

<style scoped>
  .content {
    height: 50%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    z-index: 1;
  }

  .title {
    font-size: 3rem;
  }

  .link {
    color: #215D9E;
  }

  .image {
    width: 40%;
  }

  .source {
    opacity: 0.3;
    margin-top: 7rem;
  }
</style>
