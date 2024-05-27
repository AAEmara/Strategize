<template>
  <div class="card text-center mb-3 me-5" style="width: 18rem; height: 15rem;">
    <div class="card-body">
      <h5 class="card-title">{{ this.goalObject.name }}</h5>
      <p class="card-text">{{ this.goalObject.note }}</p>
    </div>
    <div class="card-footer">
      <a
        href="#"
        class="btn btn-primary"
        data-bs-toggle="modal"
        :data-bs-target="'#create-objective-modal-' + this.goalObject.id"
        @click="toggleModal"
      >
        Create Objective
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ObjectiveGoalCard',
  components: {
  },
  props: {
    goalObject: Object
  },
  data () {
    return {
      showModal: true
    }
  },
  methods: {
    handleModalClose () {
      this.showModal = false
    },
    toggleModal () {
      this.showModal = !this.showModal
    }
  }
}
</script>
