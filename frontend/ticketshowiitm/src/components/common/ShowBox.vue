<template>
    <div class="show-box">
      <div class="show-info">
        <router-link :to="{ name: 'ShowDetails', params: { id: show.id } }">
          <h3>{{ show.name }}</h3>
        </router-link>
        <p>From {{ formatTime(show.start_time) }} to {{ formatTime(show.end_time) }}</p>
        <p>({{ formatDate(show.date) }})</p>
      </div>
      <div class="show-actions">
        <CustomAppButton @click="editShow(theatre.id,show.id)" class="btn">Edit</CustomAppButton>
        <CustomAppButton @click="deleteShow(show.id)" secondary class="btn">Delete</CustomAppButton>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import CustomAppButton from './CustomAppButton.vue';
  import { formatDate } from './../../../utils/formatDateUtils';
  import { formatTime } from './../../../utils/formatTimeUtils';

  export default {
    props: {
      show: {
        type: Object,
        required: true,
      },
      theatre:{
        type:Object,
      },
    },
    components:{
        CustomAppButton
    },
    methods: {
      editShow(theatre_id,show_id) {
        console.log(theatre_id,show_id);
        this.$router.push({ name: 'EditShow', params: { showid: show_id, theaterid: theatre_id} });
        // Handle the logic to edit the selected show
        // You can use router.push() to navigate to the edit show page
        // or display a modal for editing the show details
      },
      deleteShow(showid) {
      if (confirm('Are you sure you want to delete this show?')) {
        // Make an API call to delete the theatre
        axios
          .delete(`http://localhost:5000/api/shows/${showid}`)
          .then((response) => {
            console.log('Theatre deleted successfully:', response.data);
            // After successful deletion, you may want to navigate back to the theatres list
            // You can use router.push() for that as well
            this.$router.push("/AdminHome");
          })
          .catch((error) => {
            console.error('Error deleting theatre:', error.response.data);
            alert('Failed to delete theatre. Please try again.');
          });
      }
    }, formatTime, formatDate
    },
    mounted() {
    // Call the method to log the passed dummy string after the component is mounted
    // console.log(this.theatre.id);
    },
  };
  </script>
  
  <style scoped>
  .show-box {
    background-color: #f0f0f0; /* Use a lighter shade of the theater card's background color */
    padding: 10px;
    border-radius: 10px;
    display: flex;
    flex-direction: column; /* Arrange the show name and buttons vertically */
    align-items: center; /* Center the content horizontally */
    margin-bottom: 10px;
    width: 200px;
    margin-right: 20px;
  }

  .show-info{
    text-align: center;
  }
  
  .show-actions {
    display: flex;
    justify-content: space-around;
    width: 100%;
  }

  .btn{
    height: 50%;
    width: 40%;
    font-size: 80%;
    padding: 10px;
  }
  </style>
  