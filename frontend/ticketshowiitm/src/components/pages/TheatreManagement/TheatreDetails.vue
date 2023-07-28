<template>
  <div class="theatre-details-page">
    <div v-if="theatre">
      <h1>{{ theatre.name }}</h1>
      <p><strong>Place:</strong> {{ theatre.place }}</p>
      <p><strong>Capacity:</strong> {{ theatre.capacity }}</p>
      <router-link :to="{ name: 'EditTheatre', params: { id: theatre.id } }">Edit</router-link>
    </div>
    <div v-else>
      <!-- Optional: You can show a loading message or a fallback content if data is not available yet -->
      Loading theatre details...
    </div>
  </div>
</template>
  
  <script>
  import axios from "axios";
  export default {
    name: "TheatreDetails",
    data() {
      return {
        theatre: null,
      };
    },
    mounted() {
      // Fetch the theatre details from the backend API based on the route parameter 'id'
      this.fetchTheatreDetails();
    },
    watch: {
      $route: "fetchTheatreDetails",
    },
    methods: {
      fetchTheatreDetails() {
        const theatreId = this.$route.params.id;
        // Make an API call to fetch the theatre details based on 'theatreId'
        // Replace the URL with your backend API endpoint for fetching theatre details
        axios.get(`http://localhost:5000/api/theatres/${theatreId}`)
          .then((response) => {
            this.theatre = response.data;
          })
          .catch((error) => {
            console.error("Error fetching theatre details:", error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add styles for the theatre details page if needed */
  </style>
  