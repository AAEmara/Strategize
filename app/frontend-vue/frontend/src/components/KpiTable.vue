<template>
  <table class="table table-dark table-hover text-center">
    <thead>
      <tr>
        <th class="table-header-name align-middle">KPI Name</th>
        <th class="table-header-def align-middle">Definition</th>
        <th class="table-header-buttons align-middle"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="kpi in this.KpisData" :key="kpi.id">
        <td class="align-middle">{{ kpi.name }}</td>
        <td class="align-middle">{{ kpi.definition }}</td>
        <td class="align-middle">
          <button
            type="button"
            class="btn btn-danger me-2"
            @click="onDelete(kpi.id)"
          >
            Delete
          </button>
          <button
            type="button"
            class="btn btn-light"
            data-bs-toggle="modal"
            :data-bs-target="'#update-kpi-modal-' + kpi.id"
          >
            Edit
          </button>
          <UpdateKpi
            @kpi-updated="handleUpdateKpi"
            :KpiId="kpi.id"
            :updateKpiData="kpi"
            :DatatypeData="this.DatatypeData"
            :StrategyId="this.StrategyId"
            :modalId="'update-kpi-modal-' + kpi.id"
          />
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import UpdateKpi from './UpdateKpiModal.vue'
import axios from 'axios'
export default {
  name: 'KpiTable',
  components: {
    UpdateKpi
  },
  props: {
    KpisData: Array,
    StrategyId: String,
    DatatypeData: Array
  },
  data () {
    return {
      kpiId: null
    }
  },
  methods: {
    onDelete (kpiId) {
      const path = `http://localhost:5000/api/v1/strategies/${this.StrategyId}/kpis/${kpiId}`
      axios
        .delete(path)
        .then(response => {
          this.$emit('kpi-deleted', { message: 'Success' })
        })
        .catch(error => console.log(error))
    },
    handleUpdateKpi () {
      this.$emit('kpi-updated', { message: 'Success' })
    }

  }
}
</script>

<style scoped>
.table-header-name {
  width: 20%;
}
.table-header-def {
  width: 60%;
}
.table-header-buttons {
  width: 20%;
}

</style>
