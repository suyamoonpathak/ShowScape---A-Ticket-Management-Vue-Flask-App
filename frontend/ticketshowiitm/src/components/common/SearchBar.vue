<template>
  <div>
    <input
      v-model="searchQuery"
      type="text"
      :placeholder="placeholderText"
      @focus="onInputFocus"
      @blur="onInputBlur"
      class="search-bar"
    />
    <div v-if="showOverlay" class="search-overlay">
      <div>
        <div v-for="show in filteredShows" :key="show.id">
          <ShowBannerForSearch :show="show" />
          <!-- Add other show details as needed -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ShowBannerForSearch from './ShowBannerForSearch.vue';

export default {
  data() {
    return {
      searchQuery: "",
      showOverlay: false, // To control the overlay display
      placeholderText: "🔍 Search shows, theatres, genres, or location",
    };
  },
  props: {
    shows: {
      type: Array,
      required: true,
    },
  },
  components:{
    ShowBannerForSearch
  },
  computed: {
    filteredShows() {
      // Filter the shows based on the search query
      const query = (this.searchQuery ?? "").toLowerCase().trim();
      if (!query) {
        return [];
      } else {
        // If there's a search query, filter the shows
        return this.shows.filter((show) => {
          // Perform nullish checks for each property before using toLowerCase()
          const name = show.name?.toLowerCase() ?? "";
          const theatreName = show.theatre_name?.toLowerCase() ?? "";
          const theatreLocation = show.theatre_place?.toLowerCase() ?? "";
          const tags = show.tags?.toLowerCase() ?? "";
          const rating = show.rating?.toString() ?? "";

          return (
            name.includes(query) ||
            theatreName.includes(query) ||
            theatreLocation.includes(query) ||
            tags.includes(query) ||
            rating.includes(query)
          );
        });
      }
    },
  },
  methods:{
    onInputFocus() {
      this.placeholderText = ""; // Clear the placeholder text on input focus
    },
    onInputBlur() {
      // Reset the placeholder text to its original value if the input is empty
      if (!this.searchQuery) {
        this.placeholderText = "🔍 Search shows, theatres, genres, or location";
      }
    },
  },
  watch: {
    filteredShows(newFilteredShows) {
      this.showOverlay = newFilteredShows.length > 0; // Set the overlay display based on filtered results
    },
  },
};
</script>

<style>
.search-bar {
  width: 800px;
  height: 50px;
  background: transparent;
  border: 2px solid rgb(190, 188, 188);
  border-radius: 50px;
  text-align: center;
  font-size: 20px;
  color: rgb(190, 188, 188);
}

.search-bar::placeholder {
  text-align: center;
  font-size: 20px;
  color: rgb(190, 188, 188);
}

.search-overlay {
  position: absolute;
  top: 60px; /* Adjust this value to position the overlay correctly */
  left: 0;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>
