<template>
  <div class="create-networking-relationships-goal">

    <!-- START - Networking and Relationships Perspective's Goal Modal - START -->
    <div  class="modal fade" tabindex="-1" id="create-networking-and-relationships-modal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create Your Networking and Relationships Goal</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

          </div>

          <!-- Modal Form -->

          <div class="modal-body">

            <!-- START - Networking and Relationships Goal Form - START -->
            <form action="#" @submit.prevent="onSubmit" method="post">

              <!-- Choose Goal's Direction for Networking and Relationships Goal Component to Create -->
              <div class="mb-3">
                <label for="goal-direction" class="form-label">
                  Direction
                </label>
                <select
                  class="form-select form-select-sm"
                  aria-label="Select Goal's Direction"
                  for="goal-direction"
                  v-model="directionId"
                >
                  <option disabled value="" selected>Select a direction</option>
                  <option v-for="direction in nrDirectionsData" :key="direction.id" :value="direction.id">{{ direction.name }}</option>
                </select>
              </div>

              <!-- Enter Goal Name for Networking and Relationships Goal Component to Create -->
              <div class="mb-3">
                <label for="goal-name" class="form-label">
                  Name
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="goal-name"
                  placeholder="Your Networking and Relationships Goal Name"
                  v-model="name"
                >
              </div>

              <!-- Enter Networking and Relationships Goal Note for Goal Component to Create -->
              <div class="mb-3">
                <label for="goal-definition" class="form-label">
                  Note
                </label>
                <textarea
                  class="form-control form-control-sm"
                  id="goal-definition"
                  rows="3"
                  placeholder="Put your notes specific to your networking and relationships goal."
                  v-model="note"
                ></textarea>
              </div>

            </form>
            <!-- END - Networking and Relationships Goal Form - END -->

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
              @click="onSubmit"
            >Create</button>
          </div>

        </div>
      </div>
    </div>
    <!-- START - Networking and Relationships Perspective's Goal Modal - START -->

  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'CreateNetworkingRelationships',
  props: {
    nrDirectionsData: Object,
    nrStrategyId: String
  },
  data () {
    return {
      name: '',
      note: '',
      directionId: '',
      postGoalPath: ''
    }
  },
  methods: {
    initForm () {
      this.name = ''
      this.note = ''
      this.directionId = null
    },
    onSubmit () {
      if (this.name === '' || this.directionId === null) {
        alert('Missing Goal Name or Didn\'t select Direciton. Please fill both fields.')
        return
      }
      const goalData = {
        name: this.name,
        note: this.note,
        perspective_id: 3
      }
      this.postGoalPath = `http://localhost:5000/api/v1/strategies/${this.nrStrategyId}/directions/${this.directionId}/goals`
      axios
        .post(this.postGoalPath, goalData)
        .then(response => {
          this.$emit('nr-goal-created', { message: 'Success' })
        })
        .catch(error => {
          console.log(error)
          console.log(this.postGoalPath)
        })
      this.initForm()
    }
  }

}
</script>
