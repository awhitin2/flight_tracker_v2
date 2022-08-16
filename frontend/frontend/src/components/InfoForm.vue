<template>
  <div class='container'>
    <b-form @submit="onSubmit">
      <b-alert v-model="alerts.success.show" variant="success" dismissible>
        {{alerts.success.message}}
      </b-alert>
      <b-alert v-model="alerts.duplicate.show" variant="info" dismissible>
        {{alerts.duplicate.message}}
      </b-alert>
      <h1 class='text-center'>Flight Info</h1>
      <b-alert v-model="alerts.missing.show" variant="danger" dismissible>
        {{alerts.missing.message}}
      </b-alert>
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
          <b-form-group label="Flight Number:" label-for="flight_number">
            <b-form-input
              id="flight_number"
              v-model="form.flight_number"
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
      <b-alert v-model="alerts.invalidCell.show" variant="danger" dismissible>
        {{alerts.invalidCell.message}}
      </b-alert>
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
      alerts: {
        success: {
          show: false,
          message: 'Flight tracking successfully registered!'
        },
        duplicate: {
          show: false,
          message: 'This cell number is already tracking this flight'
        },
        missing: {
          show: false,
          message: 'Could not find any flights matching the given details'
        },
        invalidCell: {
          show: false,
          message: ('Please enter a valid U.S. cell number \
                    in the following format: xxx-xxx-xxxx')
        }
      },
      form: {
        airline: '',
        flight_number: '',
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
      event.preventDefault()
      const path = 'http://localhost:5000/register-new';
      axios.post(path, this.form)
        .then(response => this.alerts[response.data].show = true)
        .catch(error => {
          this.errorMessage = error.message;
          console.error("There was an error!", error.data);
        });
    }
  },
  created() {
    this.getFormStartData()
  }
}
</script>