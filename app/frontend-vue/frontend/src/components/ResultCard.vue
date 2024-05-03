<template>
  <div class="card">
    <div class="card-header">
      {{ this.resultCardData.name }} Expected Results
    </div>
    <div class="card-body">
      <p class="card-text">{{ this.resultCardData.result }}</p>
      <button type="button" class="btn btn-outline-dark btn-sm" data-bs-toggle="modal" :data-bs-target="'#update-direction-modal-' + this.resultCardData.id" >
        Edit Result
      </button>

    </div>
  </div>
</template>

<script>
export default {
  name: 'ResultCard',
  props: {
    resultCardData: Object
  }
}
</script>

<style scoped>
.card {
  width: 500px;
  margin-right: 10px;
}
</style>
