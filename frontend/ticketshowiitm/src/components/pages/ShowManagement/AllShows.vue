<template>
  <div>
    <div class="search">
      <SearchBar
        :shows="shows"
        @filteredShows="updateFilteredShows"
      ></SearchBar>
    </div>
    <div class="all-shows-page">
      <h1 class="upcoming-shows">Upcoming Shows</h1>
      <span v-for="show in shows" :key="show.id">
        <ShowCardForClient :show="show" />
      </span>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ShowCardForClient from "./../../common/ShowCardForClient.vue";
import SearchBar from "./../../common/SearchBar.vue";

export default {
  data() {
    return {
      shows: [], // To store the list of shows
      filteredShowsList: [], // To store the filtered shows
      showOverlay: false, // To control the overlay display
    };
  },
  components: {
    ShowCardForClient,
    SearchBar,
  },
  created() {
    // Fetch the list of shows when the component is created
    this.fetchShows();
  },
  methods: {
    fetchShows() {
      axios
        .get("http://localhost:5000/api/shows")
        .then((response) => {
          // Update the 'shows' data with the fetched shows from the backend
          this.shows = response.data;
        })
        .catch((error) => {
          console.error("Error fetching shows:", error);
        });
    },
    viewShowDetails(showId) {
      this.$router.push(`/show/${showId}`);
    },
    updateFilteredShows(filteredShows) {
      this.filteredShowsList = filteredShows;
      this.showOverlay = filteredShows.length > 0; // Set the overlay display based on filtered results
    },
  },
};
</script>
<style>
span {
  display: inline-block;
}

.upcoming-shows {
  margin-left: 10px;
}

.search {
  display: flex;
  justify-content: center;
  margin-top: 10%;
  margin-bottom: 3%;
  width: 100%;
}

.all-shows-page {
  margin: 0 5% 0 5%;
  
}

.search-overlay {
  position: absolute;
  top: 241px; /* Adjust this value to position the overlay correctly */
  margin-left: 28.6%;
  width: 42.6%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50px;
}

/* Style for the horizontal line between shows */
.horizontal-line {
  border: 0;
  height: 1px;
  background-color: #ccc;
  margin: 10px 0;
  color: white;
}

@media (max-width: 768px) {
  .all-shows-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
}

</style>
