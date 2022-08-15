<template>
  <div class='container'>
    <form @submit="onSubmit">
      <h1 class='text-center'>Flight Info</h1>
      <div class='row'>
        <div class='col'>
          <div class="form-group">
            <label for="airline">Airline</label>
            <select v-model='form.airline' type="email" class="form-control" id="airline">
              <option>Frontier</option>
              <option>Frontier</option>
              <option>Frontier</option>
            </select>
          </div>
        </div>
        <div class='col'>
          <div class="form-group">
            <label for="flightNumber">Flight Number</label>
            <input v-model='form.flightNumber' type="text" class="form-control" id="flightNumber" placeholder="Enter Flight Number">
          </div>
        </div>
        <div class='col'>
          <div class="form-group">
            <label for="date">Departure Date</label>
            <select v-model = 'form.date' class="form-control" id="date">
              <option>10/10/2022</option>
              <option>10/11/2022</option>
              <option>10/12/2022</option>
            </select>
          </div>
        </div>
      </div>
      <h1 class='text-center'>SMS Info</h1>
      <div class='row'>
        <div class='col'>
          <div class="form-group">
            <label for="cell">U.S. Cell Number</label>
            <input v-model='form.cell' type="tel" class="form-control" id="cell" placeholder="xxx-xxx-xxxx">
          </div>
        </div>
        <div class='col'>
          <div class="form-group">
            <label for="carrier">Carrier</label>
            <select v-model = 'form.carrier' class="form-control" id="carrier">
              <option>T-Mobile</option>
              <option>Verizon</option>
              <option>Sprint</option>
            </select>
          </div>
        </div>
      </div>
      <button type="submit" class="btn btn-block btn-primary">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'InfoForm',
  data() {
    return {
      form: {
        airline: '',
        flightNumber: '',
        date: '',
        cell: '',
        carrier: '',
      }
      

    }
  },
  methods: {
    onSubmit() {
      alert(this.form)
    }
  },
}
</script>