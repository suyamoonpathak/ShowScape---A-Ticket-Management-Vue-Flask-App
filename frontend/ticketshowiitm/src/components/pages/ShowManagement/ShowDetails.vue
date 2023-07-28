<template>
    <div class="show-details">
      <h1>Show Details</h1>
      <div>
        <h2>{{ show.name }}</h2>
        <p>Rating: {{ show.rating }}</p>
        <p>Tags: {{ show.tags }}</p>
        <p>Ticket Price: {{ show.ticket_price }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "ShowDetails",
    data() {
      return {
        show: {},
      };
    },
    mounted() {
      this.getShowDetails();
    },
    methods: {
      getShowDetails() {
        // Get the show ID from the route params
        const showId = this.$route.params.id;
  
        // Make API call to get show details by ID
        axios.get(`http://localhost:5000/api/shows/${showId}`)
          .then((response) => {
            this.show = response.data;
          })
          .catch((error) => {
            console.error("Error getting show details:", error);
          });
      },
    },
  };
  </script>
  
  <style>
  /* Add your CSS styles here */
  </style>
  