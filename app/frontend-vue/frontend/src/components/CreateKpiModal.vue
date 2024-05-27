<template>
  <div class="create-kpi">

    <!-- START - KPI Modal - START -->
    <div  class="modal fade" tabindex="-1" :id="modalId">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create KPI</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

          </div>

          <!-- Modal Form -->

          <div class="modal-body" style="text-align: left;">

            <!-- START - KPI Form - START -->
            <form action="#" @submit.prevent="onSubmit" method="post">

              <!-- Enter KPI's Name for KPI Component to Create -->
              <div class="mb-3">
                <label for="kpi-name" class="form-label">
                  Name
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="kpi-name"
                  placeholder="Your KPI's Name"
                  v-model="name"
                >
              </div>

              <!-- Choose KPI's Data Type for KPI Component to Create -->
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
            <!-- END - KPI Form - END -->

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
    <!-- START - KPI Modal - START -->

  </div>

</template>

<script>
import axios from 'axios'
export default {
  name: 'CreateKpi',
  props: {
    StrategyId: String,
    datatypeData: Array,
    modalId: String
  },
  data () {
    return {
      name: null,
      datatypeId: null,
      kpiDefinition: null,
      postKpiPath: ''

    }
  },
  methods: {
    initForm () {
      this.name = null
      this.datatypeId = null
      this.kpiDefinition = null
    },
    closeModal () {
      this.$emit('close')
    },
    onSubmit () {
      if (this.name === '' || this.name === null) {
        alert('Missing KPI Name. Please fill Name field.')
        return
      } else if (this.datatypeId === null) {
        alert('Missing Data Type. Please Choose a Data Type.')
      } else if (this.kpiDefinition === null) {
        alert('Missing KPI Definition. Please fill KPI Definition field.')
      }

      const kpiData = {
        name: this.name,
        definition: this.kpiDefinition,
        datatype_id: this.datatypeId
      }

      this.postKpiPath = `http://localhost:5000/api/v1/strategies/${this.StrategyId}/kpis`
      axios
        .post(this.postKpiPath, kpiData)
        .then(response => {
          this.$emit('kpi-created', { message: 'Success' })
        })
        .catch(error => {
          console.log(error)
          console.log(this.postKpiPath)
        })
      this.initForm()
    }
  }
}
</script>

<style scoped>
</style>
