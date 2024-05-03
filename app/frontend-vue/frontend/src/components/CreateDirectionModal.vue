<template>
  <div class="create">

    <!-- START - Strategic Direction Modal - START -->
    <div  class="modal fade" tabindex="-1" id="create-direction-modal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create Your Strategic Direction</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

          </div>

          <!-- Modal Form -->

          <div class="modal-body">

            <!-- START - Strategic Direction Form - START -->
            <form action="#" @submit.prevent="onSubmit" method="post">
              <!-- Enter Direction Name for Direction Component to Create -->
              <div class="mb-3">
                <label for="direction-name" class="form-label">
                  Name
                </label>
                <input
                  type="text"
                  class="form-control form-control-lg"
                  id="direction-name"
                  placeholder="Your Strategic Direction Name"
                  v-model="name"
                >
              </div>

              <!-- Enter Direction Definition for Direction Component to Create -->
              <div class="mb-3">
                <label for="direction-definition" class="form-label">
                  Definition
                </label>
                <textarea
                  class="form-control form-control-sm"
                  id="direction-definition"
                  rows="3"
                  placeholder="Define your strategic theme (direction) so it could resemble a purpose."
                  v-model="definition"
                ></textarea>
              </div>

              <!-- Enter Direction Result for Direction Component to Create -->
              <div class="mb-3">
                <label for="direction-result" class="form-label">
                  Result
                </label>
                <textarea
                  class="form-control form-control-sm"
                  id="direction-result"
                  rows="3"
                  placeholder="This where your direction leads you to, think about what result/s you want from this direction."
                  v-model="result"
                ></textarea>
              </div>
            </form>
            <!-- END - Strategic Direction Form - END -->

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
    <!-- END - Strategic Direction Modal - END -->

  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'CreateDirection',
  props: {
    postPath: String
  },
  data () {
    return {
      name: '',
      definition: '',
      result: ''
    }
  },
  methods: {
    initForm () {
      this.name = ''
      this.definition = ''
      this.result = ''
    },
    onSubmit () {
      if (this.name === '' || this.result === '') {
        alert('Missing Name or Result Input. Please fill atleast both fields.')
        return
      }
      const directionData = {
        name: this.name,
        definition: this.definition,
        result: this.result
      }
      axios
        .post(this.postPath, directionData)
        .then(response => {
          this.$emit('direction-created', { message: 'Success' })
        })
      this.initForm()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
