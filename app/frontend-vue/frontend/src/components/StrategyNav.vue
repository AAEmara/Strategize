<template>
  <nav class="navbar navbar-dark bg-dark fixed-top" aria-label="First navbar example">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Strategize</a>
      <h6 v-if="strategiesObject" class="text-white">
        {{ strategyName }} - Last Updated: {{ formattedDateTime }}
      </h6>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample01" aria-controls="navbarsExample01" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarsExample01">
        <ul class="navbar-nav me-auto mb-2">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="https://aaemara.github.io/Strategize/">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/general_strategy">General Strategy</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/objectives">Objectives</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'StrategyNav',
  props: {
    strategiesObject: Object
  },
  computed: {
    formattedDateTime () {
      const date = new Date(this.strategiesObject.update_date + 'Z')

      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      })
    },
    strategyName () {
      const strategyName = this.strategiesObject.name
      return strategyName
    }
  },
  mounted () {
  }
}
</script>

<style scoped>
</style>
