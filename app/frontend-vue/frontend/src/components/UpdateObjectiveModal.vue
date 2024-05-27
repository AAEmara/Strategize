<template>
  <div class="edit">

    <!-- START - Update Objective Modal - START -->
    <div class="modal fade" tabindex="-1" :id="modalId">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Your Objective</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

          </div>

          <!-- Modal Form -->

          <div class="modal-body">

            <!-- START - Updating/Editing Objective Form - START -->
            <form action="#" @submit.prevent="onUpdate" method="put">
              <!-- Update Objective Name for Objective Component to Create -->
              <div class="mb-3">
                <label for="objective-name" class="form-label">
                  Name
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="objective-name"
                  placeholder="Your Objective Name"
                  v-model="ObjectiveName"
                >
              </div>

              <!-- Update Objective Start Date for Objective Component to Create -->
              <div class="mb-3">
                <label for="objective-start" class="form-label">
                  Start Date
                </label>
                <input
                  type="date"
                  class="form-control form-control-lg"
                  id="objective-start"
                  placeholder="Pick Objective's Start Date"
                  v-model="ObjectiveStart"
                >
              </div>

              <!-- Update Objective End Date for Objective Component to Create -->
              <div class="mb-3">
                <label for="objective-end" class="form-label">
                  Start End
                </label>
                <input
                  type="date"
                  class="form-control form-control-lg"
                  id="objective-end"
                  placeholder="Pick Objective's End Date"
                  v-model="ObjectiveEnd"
                >
              </div>

              <!-- Update Objective's Goal for Objective Component to Create -->
              <div class="mb-3">
                <label for="objective-goal" class="form-label">
                  Objective's Goal
                </label>
                <select
                  class="form-select form-select-sm"
                  id="objective-goal"
                  v-model="objectiveGoalId"
                >
                  <option disabled :value="CurrentGoal.id" selected>{{ UpdateGoal.name }}</option>
                  <option v-for="goal in GoalsData" :key="goal.id" :value="goal.id">{{ goal.name }}</option>
                </select>
              </div>

              <!-- Update Objective's KPI Type for Objective Component to Create -->
              <div class="mb-3">
                <label for="objective-kpi-type" class="form-label">
                  KPI Type
                </label>
                <select
                  class="form-select form-select-sm"
                  id="objective-kpi-type"
                  v-model="KpiId"
                >
                  <option disabled :value="objectiveData.kpi_id" selected>{{ CurrentKpi.name }}</option>
                  <option v-for="kpi in this.KpisData" :key="kpi.id" :value="kpi.id">{{ kpi.name }}</option>
                </select>
              </div>

              <!-- Update Objective's KPI Value for Objective Component to Create -->
              <div class="mb-3">
                <!-- This form should be splitted into KPI Target and KPI Actual -->
                <label for="objective-kpi-value" class="form-label">
                  KPI Target Value
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="objective-kpi-value"
                  placeholder="Your Objective's KPI Value"
                  v-model="KpiValue"
                >
              </div>
            </form>
            <!-- END - Update/Edit Objective Form - END -->

          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >Close</button>
            <button
              type="button"
              class="btn btn-primary"
              @click="onUpdate"
            >Save Changes</button>
          </div>

        </div>
      </div>
    </div>
    <!-- END - Update Objective Modal - END -->

  </div>

</template>

<script>
import axios from 'axios'
export default {
  name: 'UpdateObjective',
  props: {
    StrategyId: String,
    DirectionId: Number,
    GoalId: Number,
    ObjectiveId: Number,
    updateObjectiveData: Object,
    modalId: String,
    GoalsData: Array,
    CurrentGoal: Object,
    KpisData: Object
  },
  data () {
    return {
      objectiveData: { ...this.updateObjectiveData },
      objectiveGoalId: null,
      KpiId: null,
      ObjectiveName: null,
      ObjectiveStart: null,
      ObjectiveEnd: null,
      KpiValue: null,
      CurrentKpi: {},
      UpdateGoal: { ...this.CurrentGoal },
      UpdateGoalId: { ...this.CurrentGoal.id }
    }
  },
  methods: {
    onUpdate () {
      this.objectiveData.name = this.ObjectiveName
      this.objectiveData.start_date = this.ObjectiveStart
      this.objectiveData.end_date = this.ObjectiveEnd
      this.objectiveData.kpi_id = this.KpidId
      this.objectiveData.kpi_value = this.KpiValue
      this.objectiveData.goal_id = this.objectiveGoalId
      const path = `http://localhost:5000/api/v1/strategies/${this.StrategyId}/directions/${this.DirectionId}/goals/${this.GoalId}/objectives/${this.objectiveData.id}`
      axios
        .put(path, this.objectiveData)
        .then(response => {
          console.log(this.UpdateGoal)
          this.UpdateGoal = response.data
          this.UpdateGoalId = response.data.goal_id
          this.$emit('objective-updated', { message: 'Success' })
        })
        .catch(error => console.log(error))
    },
    getKpi () {
      const path = `http://localhost:5000/api/v1/strategies/${this.StrategyId}/kpis/${this.objectiveData.kpi_id}`
      axios
        .get(path)
        .then(response => {
          this.CurrentKpi = response.data
          console.log(this.CurrentKpi)
        })
    }
  },
  computed: {
    formattedStartDate () {
      const startDate = new Date(this.objectiveData.start_date)
      const formattedDate = startDate.toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
      return formattedDate
    }
  },
  created () {
    this.getKpi()
  }
}
</script>

<style scoped>
</style>
