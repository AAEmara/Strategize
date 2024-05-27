<template>
  <div class="edit">

    <!-- START - KPI Modal - START -->
    <div class="modal fade" tabindex="-1" :id="modalId">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit KPI</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

          </div>

          <!-- Modal Form -->

          <div class="modal-body">

            <!-- START - Updating/Editing KPI Form - START -->
            <form action="#" @submit.prevent="onUpdate" method="put">
              <!-- Update KPI Name for KPI Component to Create -->
              <div class="mb-3">
                <label for="kpi-name" class="form-label">
                  Name
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="kpi-name"
                  placeholder="Your KPI's Name"
                  v-model="kpiName"
                >
              </div>

              <!-- Update KPI's Data Type for KPI Component to Create -->
              <div class="mb-3">
                <label for="kpi-datatype" class="form-label">
                  Data Type
                </label>
                <select
                  class="form-select form-select-sm"
                  id="kpi-datatype"
                  v-model="datatypeId"
                >
                  <option disabled value="" selected>Select a Data Type</option>
                  <option
                    v-for="datatype in datatypeData"
                    :key="datatype.id"
                    :value="datatype.id"
                  >
                    {{ datatype.name }}
                  </option>
                </select>
              </div>

              <!-- Enter KPI's Definition for KPI Component to Create -->
              <div class="mb-3">
                <!-- This form should be splitted into KPI Target and KPI Actual -->
                <label for="kpi-definition" class="form-label">
                  KPI Value
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="kpi-definition"
                  placeholder="Your KPI's Definition"
                  v-model="kpiDefinition"
                >
              </div>

            </form>
            <!-- END - Update/Edit KPI Form - END -->

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
    <!-- END - Update KPI Modal - END -->

  </div>

</template>

<script>
import axios from 'axios'
export default {
  name: 'UpdateKpi',
  props: {
    StrategyId: String,
    KpiId: Number,
    updateKpiData: Object,
    modalId: String,
    DatatypeData: Array
  },
  data () {
    return {
      kpiData: { ...this.updateKpiData },
      datatypeData: { ...this.DatatypeData },
      kpiName: null,
      kpiDefinition: null,
      datatypeId: null
    }
  },
  methods: {
    onUpdate () {
      this.kpiData.name = this.kpiName
      this.kpiData.datatype_id = this.datatypeId
      this.kpiData.definition = this.kpiDefinition

      const path = `http://localhost:5000/api/v1/strategies/${this.StrategyId}/kpis/${this.KpiId}`
      axios
        .put(path, this.kpiData)
        .then(response => {
          this.$emit('kpi-updated', { message: 'Success' })
        })
        .catch(error => console.log(error))
    }
  }
}
</script>

<style scoped>
</style>
