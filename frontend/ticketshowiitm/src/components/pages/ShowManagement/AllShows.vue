<template>
    <div class="all-shows-page">
      <h1 class="upcoming-shows">Upcoming Shows</h1>
        <span v-for="show in shows" :key="show.id">
          <ShowCardForClient :show="show"/>
        </span>
    </div>
  </template>
<script>
// Import Axios
import axios from 'axios';
import ShowCardForClient from './../../common/ShowCardForClient.vue'

export default {
  data() {
    return {
      shows: [], // To store the list of shows
    };
  },
  components:{
    ShowCardForClient
  },
  created() {
    // Fetch the list of shows when the component is created
    this.fetchShows();
  },
  methods: {
    fetchShows() {
      axios
        .get('http://localhost:5000/api/shows')
        .then((response) => {
          // Update the 'shows' data with the fetched shows from the backend
          this.shows = response.data;
        })   
        .catch((error) => {
          console.error('Error fetching shows:', error);
        });
    },
    viewShowDetails(showId){
        this.$router.push(`/show/${showId}`);
    }
  },
};
</script> 
<style>
span{
  display: inline-block;
}

.all-shows-page{
  margin-left: 50px;
}

.upcoming-shows{
  margin-left: 10px;
}

</style> 