<template>
    <div class="show-list">
      <h1>Show List</h1>
      <div v-for="show in shows" :key="show.id" @click="showDetails(show.id)">
        {{ show.name }} - Rating: {{ show.rating }} - Price: {{ show.ticket_price }}
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "ShowListFromTheatre",
    data() {
      return {
        theatreId: this.$route.params.id,
        shows: [],
      };
    },
    mounted() {
      this.getShowsForTheatre();
    },
    methods: {
      getShowsForTheatre() {
        // Make API call to get all shows for a theatre
        axios.get(`http://localhost:5000/api/shows/theatre/${this.theatreId}`)
          .then((response) => {
            this.shows = response.data;
          })
          .catch((error) => {
            console.error("Error getting shows:", error);
          });
      },
      showDetails(showId) {
        // Redirect to ShowDetails page for the selected show
        this.$router.push(`/show/${showId}`);
      },
    },
  };
  </script>
  
  <style>
  /* Add your CSS styles here */
  </style>
  