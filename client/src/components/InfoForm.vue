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
          message: ('Success! You will now receive alerts and updates for this flight. Expect a confirmation SMS shortly.')
        },
        duplicate: {
          show: false,
          message: 'Tracking alerts for this flight are already registered to this cell.'
        },
        missing: {
          show: false,
          message: 'Could not find any flights matching the given details.'
        },
        invalidCell: {
          show: false,
          message: ('Please enter a valid U.S. cell number in the following format: xxx-xxx-xxxx.')
        }
      },
      form: {
        airline: '',
        flight_number: '',
        date: '',
        cell: '',
      },
      airlines: [{ text: 'Select One', value: null },],
      dates: [{ text: 'Select One', value: null },]
    }
  },
  methods: {
    getFormStartData() {
      const path = 'http://localhost:5000/form';
      axios.get(path)
      .then((res) => {
        this.airlines.push(...res.data.airlines);
        this.dates.push(...res.data.dates);
      })
      .catch((err)=> {
        console.error(err)
      })
    },
    onSubmit() {
      event.preventDefault()
      for (alert in this.alerts) {
        this.alerts[alert].show = false
      }
      const path = 'http://localhost:5000/register-new';
      axios.post(path, this.form)
        .then(response => this.conditionalFormReset(response))
        .then(response => this.alerts[response.data].show = true)
        .catch(error => {
          this.errorMessage = error.message;
          console.error("There was an error!", error.data);
        });
    },
    conditionalFormReset(response) {
      if (response.data == 'success') {
        this.form.airline = { text: 'Select One', value: null }
        this.form.date = { text: 'Select One', value: null }
        this.form.cell = '';
        this.form.flight_number = '';
      };
      console.log(response.data)
      return Promise.resolve(response)
    },
  },
  created() {
    this.getFormStartData()
  }
}
</script>