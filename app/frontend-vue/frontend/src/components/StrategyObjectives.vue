<template>
  <div class="navbar">
    <StrategyNav :strategiesObject="strategies"/>
  </div>

  <div class="sidebar">
    <SideBar/>
  </div>

  <div class="main-container">
    <div class="direction-header d-flex flex-row justify-content-center align-items-center flex-wrap mb-3">
      <img class="direction-nav" src="../assets/left-arrow-black.png" @click="navigate(-1)">
      <h1 class="mx-5" v-if="directions.length">{{ directions[currentIndex].name }}</h1>
      <img class="direction-nav" src="../assets/right-arrow-black.png" @click="navigate(1)">
    </div>
    <div class="d-flex flex-row justify-content-center flex-wrap">
      <div class="goal-container d-flex flex-row justify-content-center text-center">
        <div v-for="goal in goals" :key="goal.id">
          <ObjectiveGoalCard
            :goalObject="goal"
          />
          <!-- Create Objective Modal -->
          <!-- TODO: This should be inside the main-container under the direction selected -->
          <CreateObjective
            @objective-created="handleCreateObjective"
            :StrategyId="strategyId"
            :DirectionId="goal.direction_id"
            :GoalId="goal.id"
            :KpisData="kpis"
            :modalId="'create-objective-modal-' + goal.id"
          />
          <div class="objective-container" v-for="objective in objectives" :key="objective.id">
            <ObjectiveCard
              v-if="goal.id == objective.goal_id"
              @objective-deleted="handleDeleteObjective"
              :ObjectiveObject="objective"
              :StrategyId="strategyId"
              :DirectionId="goal.direction_id"
              :cardId="'delete-objective-card-' + objective.id"
            />
            <UpdateObjective
              @objective-updated="handleUpdateObjective"
              :StrategyId="strategyId"
              :DirectionId="goal.direction_id"
              :GoalsData="goals"
              :CurrentGoal="goal"
              :GoalId="objective.goal_id"
              :updateObjectiveData="objective"
              :KpisData="kpis"
              :modalId="'update-objective-modal-' + objective.id"
            />

          </div>
        </div>
      </div>
    </div>
    <div class="kpi-header d-flex flex-column align-items-center">
      <h1 class="mt-3 mb-2">KPIs</h1>
      <div>
        <a
          type="button"
          href="#"
          class="btn btn-primary btn-lg mb-3"
          data-bs-toggle="modal"
          :data-bs-target="'#create-kpi-modal'"
          @click="toggleModal"
        >
          Create KPI
        </a>
      </div>
    </div>
    <div class="d-flex flex-row justify-content-center flex-wrap me-5">
      <KpiTable
        @kpi-deleted="handleDeleteKpi"
        @kpi-updated="handleUpdateKpi"
        :KpisData="kpis"
        :StrategyId="strategyId"
        :DatatypeData="this.datatypes"
      />
      <CreateKpi
        @kpi-created="handleCreateKpi"
        :StrategyId="strategyId"
        :datatypeData="datatypes"
        :modalId="'create-kpi-modal'"
      />
    </div>
  </div>

</template>

<script>
import SideBar from './StrategySidebar.vue'
import StrategyNav from './StrategyNav.vue'
import CreateObjective from './CreateObjectiveModal.vue'
import ObjectiveGoalCard from './ObjectiveGoalCard'
import ObjectiveCard from './ObjectiveCard.vue'
import KpiTable from './KpiTable.vue'
import UpdateObjective from './UpdateObjectiveModal.vue'
import CreateKpi from './CreateKpiModal.vue'
import axios from 'axios'
export default {
  name: 'Objectives',
  components: {
    StrategyNav,
    SideBar,
    CreateObjective,
    ObjectiveGoalCard,
    ObjectiveCard,
    KpiTable,
    UpdateObjective,
    CreateKpi
  },
  data () {
    return {
      currentIndex: 0,
      strategies: null,
      strategyId: null,
      directions: [],
      goals: [],
      objectives: [],
      kpis: null,
      datatypes: [],
      showModal: true
    }
  },
  watch: {
    currentIndex (newVal, oldVal) {
      this.getGoals()
    }
  },
  methods: {
    toggleModal () {
      this.showModal = !this.showModal
    },
    getStrategies () {
      const path = 'http://localhost:5000/api/v1/strategies'
      // fetching strategies list to get the first strategy.
      // TODO: Turn the code to recieve the id of the triggered strategy only, once you finish user auth.
      axios
        .get(path)
        .then(response => {
          this.strategies = response.data[0]
          this.strategyId = response.data[0].id
          this.getPerspectives()
          this.getDirections()
        })
    },
    getPerspectives () {
      const path = 'http://localhost:5000/api/v1/perspectives'
      axios
        .get(path)
        .then(response => {
          this.perspectives = response.data
        })
    },
    getDirections () {
      const path = 'http://localhost:5000/api/v1/strategies/'.concat(this.strategyId)
        .concat('/directions/')
      axios
        .get(path)
        .then(response => {
          this.directions = response.data
          this.getGoals()
        })
    },
    getGoals () {
      if (this.directions.length > 0 && this.currentIndex >= 0 && this.currentIndex < this.directions.length) {
        const currentDirection = this.directions[this.currentIndex]
        const path = `http://localhost:5000/api/v1/strategies/${this.strategyId}/directions/${currentDirection.id}/goals`
        axios
          .get(path)
          .then(response => {
            this.goals = response.data
            this.getObjectives()
            this.getKpis()
          })
      }
    },
    getObjectives () {
      // Create an array of promises for each goal's objectives
      const objectivesPromises = this.goals.map(goal => {
        const path = `http://localhost:5000/api/v1/strategies/${this.strategyId}/directions/${this.directions[this.currentIndex].id}/goals/${goal.id}/objectives`
        return axios.get(path)
      })

      // Use Promise.all to wait for all API calls to finish
      Promise.all(objectivesPromises)
        .then(responses => {
          // Combine the objectives from all responses into one array
          this.objectives = responses.flatMap(response => response.data)
        })
        .catch(error => {
          // Handle errors here
          console.error('Error fetching objectives:', error)
        })
    },
    navigate (step) {
      this.currentIndex += step
      // Looping back to the start or the end if out of bounds.
      if (this.currentIndex >= this.directions.length) {
        this.currentIndex = 0
      } else if (this.currentIndex < 0) {
        this.currentIndex = this.directions.length - 1
      }
    },
    getKpis () {
      const path = `http://localhost:5000/api/v1/strategies/${this.strategyId}/kpis`
      axios
        .get(path)
        .then(response => {
          this.kpis = response.data
          this.getDatatypes()
        })
    },
    getDatatypes () {
      const path = 'http://localhost:5000/api/v1/datatypes'
      axios
        .get(path)
        .then(response => {
          this.datatypes = response.data
        })
    },
    handleCreateObjective () {
      this.getStrategies()
    },
    handleUpdateObjective () {
      this.getStrategies()
    },
    handleDeleteObjective () {
      this.getStrategies()
    },
    handleCreateKpi () {
      this.getStrategies()
    },
    handleDeleteKpi () {
      this.getStrategies()
    },
    handleUpdateKpi () {
      this.getStrategies()
    }
  },
  created () {
    this.getStrategies()
  },
  mounted () {
    document.title = 'Strategize - Objectives'
  }
}
</script>

<style scoped>
.main-container {
  margin-left: calc(4.5rem + 50px);
}

.direction-header .kpi-header {
  align-items: center;
}
.direction-nav {
  width: 30px;
  height: 30px;
  cursor: pointer;
}
</style>
