<template>
  <div class="create-objective">

    <!-- START - Objective Modal - START -->
    <div  class="modal fade" tabindex="-1" :id="modalId">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create Your Objective</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

          </div>

          <!-- Modal Form -->

          <div class="modal-body" style="text-align: left;">

            <!-- START - Objective Form - START -->
            <form action="#" @submit.prevent="onSubmit" method="post">

              <!-- Enter Objective's Name for Objective Component to Create -->
              <div class="mb-3">
                <label for="objective-name" class="form-label">
                  Name
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="objective-name"
                  placeholder="Your Objective's Name"
                  v-model="name"
                >
              </div>

              <!-- Choose Objective's Start Date for Objective Component to Create -->
              <div class="mb-3">
                <label for="objective-start" class="form-label">
                  Start Date
                </label>
                <input
                  type="date"
                  class="form-control form-control-lg"
                  id="objective-start"
                  placeholder="Pick Objective's Start Date"
                  v-model="startDate"
                >
              </div>

              <!-- Choose Objective's End Date for Objective Component to Create -->
              <div class="mb-3">
                <label for="objective-end" class="form-label">
                  End Date
                </label>
                <input
                  type="date"
                  class="form-control form-control-lg"
                  id="objective-end"
                  placeholder="Pick Objective's End Date"
                  v-model="endDate"
                >
              </div>

              <!-- Choose Objective's KPI Type for Objective Component to Create -->
              <div class="mb-3">
                <label for="objective-kpi-type" class="form-label">
                  KPI Type
                </label>
                <select
                  class="form-select form-select-sm"
                  id="objective-kpi-type"
                  v-model="kpiId"
                >
                  <option disabled value="" selected>Select a KPI Type</option>
                  <option v-for="kpi in KpisData" :key="kpi.id" :value="kpi.id">{{ kpi.name }}</option>
                </select>
              </div>

              <!-- Enter Objective's KPI Value for Objective Component to Create -->
              <div class="mb-3">
                <!-- This form should be splitted into KPI Target and KPI Actual -->
                <label for="objective-kpi-value" class="form-label">
                  KPI Value
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="objective-kpi-value"
                  placeholder="Your Objective's KPI Value"
                  v-model="kpiValue"
                >
              </div>

            </form>
            <!-- END - Objective Form - END -->

          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
              @click="closeModal"
            >Close</button>
            <button
              type="button"
              class="btn btn-primary"
              @click="onSubmit"
            >Create</button>
          </div>

        </div>
      </div>
    </div>
    <!-- START - Objective Modal - START -->

  </div>

</template>

<script>
import axios from 'axios'
export default {
  name: 'CreateObjective',
  props: {
    StrategyId: String,
    DirectionId: Number,
    GoalId: Number,
    KpisData: Array,
    GoalObject: Object,
    modalId: String
  },
  data () {
    return {
      name: null,
      startDate: null,
      endDate: null,
      kpiId: null,
      kpiValue: null,
      goalId: this.GoalId,
      postObjectivePath: ''

    }
  },
  methods: {
    initForm () {
      this.name = null
      this.startDate = null
      this.endDate = null
      this.kpiId = null
      this.kpiValue = null
      this.goalId = this.GoalId
    },
    closeModal () {
      this.$emit('close')
    },
    onSubmit () {
      if (this.name === '' || this.name === null) {
        alert('Missing Objective Name. Please fill Name field.')
        return
      } else if (this.startDate === null) {
        alert('Missing Start Date. Please Choose a Start Date.')
      } else if (this.endDate === null) {
        alert('Missing End Date. Please Choose an End Date.')
      } else if (this.kpiId === null) {
        alert('Missing KPI Type. Please Choose a KPI Type.')
      } else if (this.kpiValue === null) {
        alert('Missing KPI Value. Please Choose a KPI Value.')
      }

      const objectiveData = {
        name: this.name,
        start_date: this.startDate,
        end_date: this.endDate,
        kpi_id: this.kpiId,
        kpi_value: this.kpiValue,
        goal_id: this.goalId
      }
      this.postObjectivePath = `http://localhost:5000/api/v1/strategies/${this.StrategyId}/directions/${this.DirectionId}/goals/${this.GoalId}/objectives`
      axios
        .post(this.postObjectivePath, objectiveData)
        .then(response => {
          this.$emit('objective-created', { message: 'Success' })
        })
        .catch(error => {
          console.log(error)
          console.log(this.postObjectivePath)
        })
      this.initForm()
    }
  }
}
</script>

<style scoped>
</style>
