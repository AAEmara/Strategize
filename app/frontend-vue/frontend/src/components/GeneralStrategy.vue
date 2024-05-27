<template>

  <div class="navbar">
    <StrategyNav
      :strategiesObject="strategies[0]"
    />
  </div>

  <div class="sidebar">
    <SideBar/>
  </div>

  <div class="main-container">
    <!-- Create Direction Modal -->
    <CreateDirection
      @direction-created="handleCreateDirection"
      :postPath="postDirectionPath"
    />

    <!-- Create Learning and Growth Goal Modal -->
    <CreateLearningGrowth
      @lg-goal-created="handleUpdateDirection"
      :directionsData="directions"
      :strategyId="strategyId"
    />

    <!-- Create Productivity and Processes Goal Modal -->
    <CreateProductivityProcesses
      @pp-goal-created="handleUpdateDirection"
      :ppDirectionsData="directions"
      :ppStrategyId="strategyId"
    />

    <!-- Create Networking and Relationships Goal Modal -->
    <CreateNetworkingRelationships
      @nr-goal-created="handleUpdateDirection"
      :nrDirectionsData="directions"
      :nrStrategyId="strategyId"
    />

    <!-- Create Financial Goal Modal -->
    <CreateFinancial
      @f-goal-created="handleUpdateDirection"
      :fDirectionsData="directions"
      :fStrategyId="strategyId"
    />

    <!-- This should be the strategy page, so only one strategy accessible as desired from user -->
    <!-- TODO: There should be a dashboard page where the user sees all the strategies available to select -->
    <h1 class="mt-2 mb-3">Strategic Directions</h1>

    <div class="d-flex flex-row justify-content-center flex-wrap">
      <div v-for="direction in directions" :key="direction.id" class="d-flex align-items-stretch ml-3">
        <DirectionCard
          class="direction-card me-3"
          @direction-deleted="handleDeleteDirection"
          :directionData="direction"
          :cardId="'delete-direction-card-' + direction.id"
        />
        <UpdateDirection @direction-updated="handleUpdateDirection" :updateDirectionData="direction" :modalId="'update-direction-modal-' + direction.id"/>
      </div>
    </div>

    <div class="results-container">
      <ResultCard v-for="direction in directions" :key="direction.id" :resultCardData="direction"/>
    </div>

    <!-- PERSPECTIVES & GOALS -->

    <h1 class="mt-5 mb-3">Strategic Perspectives</h1>
    <div class="perspectives d-flex flex-row justify-content-between me-5">
      <div class="card" style="width: 18rem;" v-for="perspective in perspectives" :key="perspective.id">
        <div class="card-body">
          <h5 class="card-title">{{ perspective.name }}</h5>
          <p
            v-if="perspective.name == 'Learning and Growth'"
            class="card-text"
          >
            Focuses on intangible assets, emphasizing the internal skills, knowledge, and capabilities
            necessary to support value-creating processes.
          </p>
          <p
            v-else-if="perspective.name == 'Productivity and Processes'"
            class="card-text"
          >
            Focuses on critical operations that must excel at to meet financial and
            networking &amp; relationships goals, emphasizing the optimization of key processes to
            enhace productivity and performance.
          </p>
          <p
            v-else-if="perspective.name == 'Networking and Relationships'"
            class="card-text"
          >
            Focuses on building and maintaining a robust network and connections, emphasizing the cultivation
            of relationships that are mutually benficial and align with strategic goals.
          </p>
          <p
            v-else-if="perspective.name == 'Financial'"
            class="card-text"
          >
            Focuses on setting financial goals that aligns with the broader strategy, where it includes
            goals related to profitability, budgeting and other aspects that helps achieving the strategy.
          </p>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item" v-for="goal in PerspectiveGoals(perspective.id)" :key="goal.id">
            {{ goal.name }}
            <br>
            <span class="badge rounded-pill text-bg-dark me-1">#DIR{{ goal.direction_id }}</span>
            <span class="badge rounded-pill text-bg-warning">#GOAL{{ goal.id }}</span>
          </li>
        </ul>
        <div class="card-body">
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import CreateDirection from './CreateDirectionModal.vue'
import CreateLearningGrowth from './CreateLGGoalModal.vue'
import CreateProductivityProcesses from './CreatePPGoalModal.vue'
import CreateNetworkingRelationships from './CreateNRGoalModal.vue'
import CreateFinancial from './CreateFGoalModal.vue'
import DirectionCard from './DirectionCard.vue'
import UpdateDirection from './UpdateDirectionModal.vue'
import ResultCard from './ResultCard.vue'
import SideBar from './StrategySidebar.vue'
import StrategyNav from './StrategyNav.vue'
import axios from 'axios'
export default {
  name: 'Strategy',
  components: {
    CreateDirection,
    CreateLearningGrowth,
    CreateProductivityProcesses,
    CreateNetworkingRelationships,
    CreateFinancial,
    UpdateDirection,
    DirectionCard,
    ResultCard,
    SideBar,
    StrategyNav
  },
  data () {
    return {
      title: 'Hello World',
      strategies: [],
      perspectives: null,
      strategyId: '',
      directions: [],
      goals: [],
      postDirectionPath: '',
      updateDirectionData: null
    }
  },
  methods: {
    getStrategies () {
      const path = 'http://localhost:5000/api/v1/strategies'
      // fetching strategies list to get the first strategy.
      // TODO: Turn the code to recieve the id of the triggered strategy only, once you finish user auth.
      axios
        .get(path)
        .then(response => {
          this.strategies = response.data
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
      this.postDirectionPath = path
      axios
        .get(path)
        .then(response => {
          this.directions = response.data
          this.getGoals()
        })
    },
    getGoals () {
      // Create an array of promises for each direction's goals
      const goalsPromises = this.directions.map(direction => {
        const path = `http://localhost:5000/api/v1/strategies/${this.strategyId}/directions/${direction.id}/goals`
        return axios.get(path)
      })

      // Use Promise.all to wait for all API calls to finish
      Promise.all(goalsPromises)
        .then(responses => {
          // Combine the goals from all responses into one array
          this.goals = responses.flatMap(response => response.data)
        })
        .catch(error => {
          // Handle errors here
          console.error('Error fetching goals:', error)
        })
    },
    handleCreateDirection () {
      this.getStrategies()
    },
    handleUpdateDirection () {
      this.getStrategies()
    },
    handleDeleteDirection () {
      this.getStrategies()
    }
  },
  computed: {
    DirectionName () {
      let directionName = ''
      for (let i = 0; i < this.goals.length; i++) {
        for (let j = 0; j < this.directions.length; j++) {
          if (this.directions[j].id === this.goals[i].id) {
            directionName = this.directions[j].name
          }
        }
      }
      return directionName
    },
    PerspectiveGoals () {
      return (perspectiveId) => {
        return this.goals.filter(goal => goal.perspective_id === perspectiveId)
      }
    }
  },
  created () {
    this.getStrategies()
  },
  mounted () {
    document.title = 'Strategize - General Strategy'
  }
}
</script>

<style scoped>
h1 {
  text-align: center;
}
h2 {
  text-align: center;
  margin-bottom: 20px;
  margin-top: 20px;
}

.results-container {
  display: flex;
  justify-content: center;
  margin-right: 40px;
}

.direction-card {
  width: 350px;
}

.main-container {
  margin-left: calc(4.5rem + 50px);
}

.perspectives {
  margin-bottom: 20px;
}
</style>
