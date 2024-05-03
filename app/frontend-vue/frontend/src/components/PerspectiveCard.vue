<template>
  <h1>Hello World</h1>
  <div class="card-group">
    <div class="card">
      <img src="../assets/directions-icon.png" class="card-img-top" alt="Learning and Growth">
      <div class="card-body">
        <h5 class="card-title">Card title</h5>
        <p class="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PerspectiveCard',
  data () {
  }
}
</script>

<style scoped>
img {
  width: 300px;
}
.card {
 max-width: 300px;
}
</style>
