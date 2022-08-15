<template>
  <div>
      <!-- Bootstrap CSS -->
    <link rel="stylesheet" 
    href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/flatly/bootstrap.min.css" 
    integrity="sha384-qF/QmIAj5ZaYFAeQcrQ6bfVMAh4zZlrGwTPY7T/M+iTTLJqJBJjwwnsE5Y0mV7QK" 
    crossorigin="anonymous">
    <div class='container-fluid jumbotron bg-primary'>
      <h1 class='text-light text-center display-1'>Flight Tracker</h1>
      <h3 class='text-light text-center display-5'>Receive instant SMS alerts about flight changes </h3>
    </div>
    <info-form></info-form>
  </div>
</template>


<script>
import InfoForm from "@/components/InfoForm.vue"

export default {
  name: 'HomeView',
  components: {
    InfoForm
  },
  methods: {
    submit() {
    }
  },
}
</script>