<template>
  <div class="card text-bg-dark mb-3" style="max-width: 18rem;" :id="cardId">
    <div class="card-header">Objective</div>
    <div class="card-body">
      <h5 class="card-title">{{ this.ObjectiveObject.name }}</h5>
      <p>Start Date: {{ formatDate(this.ObjectiveObject.start_date) }}</p>
      <p>End Date: {{ formatDate(this.ObjectiveObject.end_date) }}</p>
      <p>{{ kpiName }}: {{ this.ObjectiveObject.kpi_value }}</p>
    </div>
    <div class="card-footer">
      <button
        @click="onDelete"
        type="button"
        class="btn btn-danger me-2"
        data-bs-toggle="card"
        :data-bs-target="'#delete-objective-card-' + this.ObjectiveObject.id"
      >
        Delete
      </button>
      <button
        type="button"
        class="btn btn-light"
        data-bs-toggle="modal"
        :data-bs-target="'#update-objective-modal-' + this.ObjectiveObject.id"
      >
        Edit
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ObjectiveCard',
  props: {
    cardId: String,
    ObjectiveObject: Object,
    StrategyId: String,
    DirectionId: Number
  },
  data () {
    return {
      kpiName: ''
    }
  },
  methods: {
    getKpiName () {
      const path = `http://localhost:5000/api/v1/strategies/${this.StrategyId}/kpis/${this.ObjectiveObject.kpi_id}`
      axios
        .get(path)
        .then(response => {
          this.kpiName = response.data.name
        })
    },
    formatDate (dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    onDelete () {
      const path = `http://localhost:5000/api/v1/strategies/${this.StrategyId}/directions/${this.DirectionId}/goals/${this.ObjectiveObject.goal_id}/objectives/${this.ObjectiveObject.id}`
      axios
        .delete(path)
        .then(response => {
          this.$emit('objective-deleted', { message: 'Success' })
        })
        .catch(error => console.log(error))
    }
  },
  created () {
    this.getKpiName()
  }
}
</script>
