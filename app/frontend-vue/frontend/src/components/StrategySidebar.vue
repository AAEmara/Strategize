<template>
  <div class="sidebar d-flex flex-column flex-shrink-0 bg-dark position-fixed" style="width: 4.5rem;">
    <a href="/" class="d-block p-3 link-dark text-decoration-none" title="Icon-only" data-bs-toggle="tooltip" data-bs-placement="right">
      <svg class="bi" width="40" height="32"><use xlink:href="#bootstrap"/></svg>
      <span class="visually-hidden">Icon-only</span>
    </a>
    <ul class="nav nav-pills nav-flush flex-column mb-auto text-center">
      <li class="nav-item">
        <a href="#" class="nav-link py-3 border-bottom" :class="{ 'active': isDirectionActive }" aria-current="page" title="Create Direction" data-bs-toggle="modal" data-bs-target="#create-direction-modal" @mouseover="isDirectionActive = true" @mouseleave="isDirectionActive = false" @click="toggleModal">
        <img src="../assets/directions-white.png" alt="Directions" width="24" height="24">
        </a>
      </li>
      <li>
        <a href="#" class="nav-link py-3 border-bottom" :class="{ 'active': isLearningGrowthActive }" aria-current="page" title="Create Learning and Growth Goal" data-bs-toggle="modal" data-bs-target="#create-learning-growth-modal" @mouseover="isLearningGrowthActive = true" @mouseleave="isLearningGrowthActive = false" @click="toggleModal">
        <img src="../assets/learning-and-growth.png" alt="Learning and Growth Goal" width="24" height="24">
        </a>
      </li>
      <li>
        <a href="#" class="nav-link py-3 border-bottom" :class="{ 'active': isProductivityProcessesActive }" title="Create Productivity and Processes Goal" data-bs-toggle="modal" data-bs-target="#create-productivity-processes-modal" @mouseover="isProductivityProcessesActive = true" @mouseleave="isProductivityProcessesActive = false" @click="toggleModal">
        <img src="../assets/productivity-and-processes-white.png" alt="Create Productivity and Processes Goal" width="24" height="24">
        </a>
      </li>
      <li>
        <a href="#" class="nav-link py-3 border-bottom" :class="{ 'active': isNetworkingRelationshipsActive }" title="Create Networking and Relationships Goal" data-bs-toggle="modal" data-bs-target="#create-networking-and-relationships-modal" @mouseover="isNetworkingRelationshipsActive = true" @mouseleave="isNetworkingRelationshipsActive = false" @click="toggleModal">
        <img src="../assets/networking-and-relationships-white.png" alt="Create Networking and Relationships Goal" width="24" height="24">
        </a>
      </li>
      <li>
        <a href="#" class="nav-link py-3 border-bottom" :class="{ 'active': isFinancialActive }" title="Create Financial Goal" data-bs-toggle="modal" data-bs-target="#create-financial-modal" @mouseover="isFinancialActive = true" @mouseleave="isFinancialActive = false" @click="toggleModal" >
        <img src="../assets/financial-white.png" alt="Create Financial Goal" width="24" height="24">
        </a>
      </li>
    </ul>
    <div class="dropdown border-top">
      <a href="#" class="d-flex align-items-center justify-content-center p-3 link-dark text-decoration-none dropdown-toggle" id="dropdownUser3" data-bs-toggle="dropdown" aria-expanded="false">
        <img src="https://github.com/mdo.png" alt="mdo" width="24" height="24" class="rounded-circle">
      </a>
      <ul class="dropdown-menu text-small shadow" aria-labelledby="dropdownUser3">
        <li><a class="dropdown-item" href="#">New project...</a></li>
        <li><a class="dropdown-item" href="#">Settings</a></li>
        <li><a class="dropdown-item" href="#">Profile</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="#">Sign out</a></li>
      </ul>
    </div>
  </div>

  <CreateDirection v-if="showModal" @close="toggleModal"/>
  <CreateLearningGrowth v-if="showModal" @close="toggleModal"/>
</template>

<script>
import CreateDirection from './CreateDirectionModal.vue'
import CreateLearningGrowth from './CreateLGGoalModal.vue'
export default {
  name: 'StrategySidebar',
  components: {
    CreateDirection,
    CreateLearningGrowth
  },
  data () {
    return {
      isDirectionActive: false,
      isLearningGrowthActive: false,
      isProductivityProcessesActive: false,
      isNetworkingRelationshipsActive: false,
      isFinancialActive: false
    }
  },
  methods: {
    toggleModal () {
      this.showModal = !this.showModal
    }
  }
}
</script>

<style scoped>
.sidebar {
  position: fixed; /* Fixed sidebar (stay in place on scroll) */
  left: 0;        /* Align to the left side of the viewport */
  top: 0;         /* Align to the top of the viewport */
  bottom: 0;      /* Stretch to the bottom of the viewport */
  height: calc(100vh -50px);  /* Set the height to 100% of the viewport height */
}</style>
