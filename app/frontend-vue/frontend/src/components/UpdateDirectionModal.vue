<template>
  <div class="edit">

    <!-- START - Update Strategic Direction Modal - START -->
    <div class="modal fade" tabindex="-1" :id="modalId">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Your Strategic Direction</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

          </div>

          <!-- Modal Form -->

          <div class="modal-body">

            <!-- START - Updating/Editing Strategic Direction Form - START -->
            <form action="#" @submit.prevent="onSave" method="put">
              <!-- Update Direction Name for Direction Component to Create -->
              <div class="mb-3">
                <label for="direction-name" class="form-label">
                  Name
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="direction-name"
                  placeholder="Your Strategic Direction Name"
                  v-model="directionData.name"
                >
              </div>

              <!-- Update Direction Definition for Direction Component to Create -->
              <div class="mb-3">
                <label for="direction-definition" class="form-label">
                  Definition
                </label>
                <textarea
                  class="form-control form-control-sm"
                  id="direction-definition"
                  rows="3"
                  placeholder="Define your strategic theme (direction) so it could resemble a purpose."
                  v-model="directionData.definition"
                ></textarea>
              </div>

              <!-- Update Direction Result for Direction Component to Create -->
              <div class="mb-3">
                <label for="direction-result" class="form-label">
                  Result
                </label>
                <textarea
                  class="form-control form-control-sm"
                  id="direction-result"
                  rows="3"
                  placeholder="This where your direction leads you to, think about what result/s you want from this direction."
                  v-model="directionData.result"
                ></textarea>
              </div>
            </form>
            <!-- END - Update/Edit Strategic Direction Form - END -->

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
    <!-- END - Update Strategic Direction Modal - END -->

  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UpdateDirection',
  props: {
    updateDirectionData: Object,
    modalId: String
  },
  data () {
    return {
      directionData: { ...this.updateDirectionData }
    }
  },
  methods: {
    onUpdate () {
      const path = `http://localhost:5000/api/v1/strategies/${this.directionData.strategy_id}/directions/${this.directionData.id}`
      if (this.directionData.name === '' || this.directionData.result === '') {
        alert('Missing Name or Result Input. Please fill atleast both fields.')
        return
      }
      axios
        .put(path, this.directionData)
        .then(response => {
          this.$emit('direction-updated', { message: 'Success' })
        })
        .catch(error => console.log(error))
    }
  }
}
</script>
