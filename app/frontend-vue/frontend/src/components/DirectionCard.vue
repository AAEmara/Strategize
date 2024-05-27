<template>

  <!-- Strategic Direction Card -->
  <div class="card border-primary mb-3" style="max-width: 18rem;" :id="cardId">
    <div class="card-body text-primary">
      <h5 class="direction-card-name">
        <span class="badge rounded-pill text-bg-dark">#DIR{{ this.directionData.id }}</span>
        {{ this.directionData.name }}
      </h5>
      <hr>
      <p class="direction-card-definition">Definition: {{ this.directionData.definition }}</p>
  </div>
  <div class="card-footer border-primary">
    <button
      @click="onDelete"
      type="button"
      class="btn btn-outline-danger btn-sm"
      data-bs-toggle="card"
      :data-bs-target="'#delete-direction-card-' + this.directionData.id"
    >
      Delete
    </button>
    <button
      type="button"
      class="btn btn-outline-dark btn-sm"
      data-bs-toggle="modal"
      :data-bs-target="'#update-direction-modal-' + this.directionData.id"
    >
      Edit
    </button>

  </div>
</div>

</template>

<script>
import axios from 'axios'
export default {
  name: 'DirectionCard',
  props: {
    directionData: Object,
    cardId: String
  },
  data () {
  },
  methods: {
    onDelete () {
      const path = `http://localhost:5000/api/v1/strategies/${this.directionData.strategy_id}/directions/${this.directionData.id}`
      axios
        .delete(path)
        .then(response => {
          this.$emit('direction-deleted', { message: 'Success' })
        })
        .catch(error => console.log(error))
    }
  }
}
</script>
