<template>
  <div class='container'>
    <b-form @submit="onSubmit">
      <h1 class='text-center'>Flight Info</h1>
      <div class='row'>
        <div class='col'>
          <b-form-group label='Airline' label-for='airline' >
            <b-form-select 
              :options= 'airlines' 
              v-model='form.airline' 
              id='airline'
              required
            ></b-form-select>
          </b-form-group>
        </div>
        <div class='col'>
          <b-form-group label="Flight Number:" label-for="flightNumber">
            <b-form-input
              id="flightNumber"
              v-model="form.flightNumber"
              placeholder="Enter flight number"
              required
            ></b-form-input>
          </b-form-group>
        </div>
        <div class='col'>
          <b-form-group label='Departure Date' label-for='date' >
            <b-form-select 
              :options= 'dates' 
              v-model='form.date' 
              id='date'
              required
            ></b-form-select>
          </b-form-group>
        </div>
      </div>
      <h1 class='text-center'>SMS Info</h1>
      <div class='row'>
        <div class='col'>
          <b-form-group label="U.S. Cell Number:" label-for="cell">
            <b-form-input
              id="cell"
              v-model="form.cell"
              placeholder="xxx-xxx-xxxx"
              required
            ></b-form-input>
          </b-form-group>
        </div>
        <div class='col'>
          <b-form-group label='Carrier' label-for='carrier' >
            <b-form-select 
            :options= 'carriers' 
            v-model='form.carrier' 
            id='carrier'
            required
          ></b-form-select>
          </b-form-group>
        </div>
      </div>
      <button type="submit" class="btn btn-block btn-primary">Submit</button>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios'

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
      },
      carriers: [
        'Verizon',
      ],
      airlines: [
        'Frontier',
        'Delta',
        'American',
      ],
      dates: [
        '10/10/22',
        '10/12/22',
        '10/14/22'
      ]
    }
  },
  methods: {
    getFormStartData() {
      const path = 'http://localhost:5000/form';
      axios.get(path)
      .then((res) => {
        this.carriers = res.data.carriers;
        this.dates = res.data.dates
        this.airlines = res.data.airlines
      })
      .catch((err)=> {
        console.error(err)
      })
    },
    onSubmit() {
      event.preventDefault();
      alert(JSON.stringify(this.form))
    }
  },
  created() {
    this.getFormStartData()
  }
}
</script>