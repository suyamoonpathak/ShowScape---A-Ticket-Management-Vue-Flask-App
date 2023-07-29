<template>
  <div class="theatres-page">
    <CustomHeading1 class="welcomeText"
      >Hi {{ username }}! Welcome to your dashboard.</CustomHeading1
    >
    <div v-if="theatres.length === 0">
      <CustomHeading1 class="empty">No theatres found.</CustomHeading1>
    </div>
    <div v-else>
      <div class="theatresMessage">
        <CustomHeading1 class="theatresText"
          >Here are your theatres:</CustomHeading1
        >
      </div>
      <ul>
        <li v-for="theatre in theatres" :key="theatre.id">
          <div class="theatre-card">
            <div class="theatre-header">
              <h1>
                {{ theatre.name }} | {{ theatre.place }} |
                {{ theatre.capacity }} Seats
              </h1>
              <div class="actions">
                <!-- "+" button to add shows -->
                <CustomAppButton
                  class="add-show-btn"
                  @click="addShowToTheatre(theatre.id)"
                >
                  Add Show
                </CustomAppButton>
                <!-- Edit and delete buttons -->
                <CustomAppButton
                  class="edit-btn"
                  @click="editTheatre(theatre.id)"
                  secondary
                >
                  Edit
                </CustomAppButton>
                <CustomAppButton
                  class="delete-btn"
                  @click="deleteTheatre(theatre.id)"
                  secondary
                >
                  Delete
                </CustomAppButton>
              </div>
            </div>
            <div class="show-list">
              <div v-if="showExistsForTheatre(theatre.id)">
                <!-- Render the ShowBox components for this theater -->
                <div v-for="group of shows" :key="group" class="showboxes">
                  <div v-for="show in group" :key="show.id">
                    <span v-if="show.length != 0 && show.theatre_id == theatre.id">
                      <ShowBox :show="show" :theatre="theatre" />
                    </span>
                  </div>
                </div>
              </div>
              <div v-else>
                <!-- Message when no shows are scheduled for this theater -->
                <p>No shows created.</p>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <CustomAppButton class="add-theatre-btn create-btn" @click="addNewTheatre"
      >Add Theatre
    </CustomAppButton>
  </div>
</template>

<script>
import axios from "axios";
import CustomAppButton from "../../common/CustomAppButton.vue";
import CustomHeading1 from "../../common/CustomHeading1.vue";
import ShowBox from "@/components/common/ShowBox.vue";
import { decodeJwtToken } from "../../../../utils/jwtUtils";

export default {
  name: "TheatresListForAdmin",
  data() {
    return {
      theatres: [],
      shows: [],
      username: "",
    };
  },
  components: {
    CustomAppButton,
    CustomHeading1,
    ShowBox,
  },
  mounted() {
    // Fetch the list of theatres from the backend API
    this.fetchTheatres();
  },
  methods: {
    fetchTheatres() {
      const accessToken = localStorage.getItem("access_token");
      const jwtPayload = decodeJwtToken(accessToken);
      const admin_id = jwtPayload.admin_id;
      this.username = jwtPayload.username;
      // Make an API call to fetch the list of theatres
      // Replace the URL with your backend API endpoint for fetching theatres
      axios
        .get(`http://localhost:5000/api/theatres/admin/${admin_id}`)
        .then((response) => {
          this.theatres = response.data;
          this.theatres.forEach((theatre) => {
            axios
              .get(`http://localhost:5000/api/shows/theatre/${theatre.id}`)
              .then((response) => {
                this.shows.push(response.data);
              })
              .catch((error) => {
                console.error("Error getting shows:", error);
              });
          });
        })
        .catch((error) => {
          console.error("Error fetching theatres:", error);
        });
    },
    addShowToTheatre(theatreId) {
      this.$router.push({ name: "CreateShow", params: { id: theatreId } });
      // Handle the logic to add a show for the selected theatre
      // You can use router.push() to navigate to the add show page
      // or display a modal for adding the show details
    },
    editTheatre(theatreId) {
      console.log(theatreId);
      this.$router.push({ name: "EditTheatre", params: { id: theatreId } });
    },
    deleteTheatre(theatreId) {
      if (confirm("Are you sure you want to delete this theatre?")) {
        // Make an API call to delete the theatre
        axios
          .delete(`http://localhost:5000/api/theatres/${theatreId}`)
          .then((response) => {
            console.log("Theatre deleted successfully:", response.data);
            // After successful deletion, you may want to navigate back to the theatres list
            // You can use router.push() for that as well
            this.theatres = this.theatres.filter(
              (theatre) => theatre.id !== theatreId
            );
            this.$router.push("/AdminHome");
          })
          .catch((error) => {
            console.error("Error deleting theatre:", error.response.data);
            alert("Failed to delete theatre. Please try again.");
          });
      }
    },
    addNewTheatre() {
      this.$router.push({ name: "CreateTheatre" });
    },
    showExistsForTheatre(theatreId) {
      // Check if there are shows associated with the given theater ID
      return this.shows.some((group) => {
        return group.some((show) => show.length !== 0 && show.theatre_id === theatreId);
      });
    },
  },
};
</script>

<style scoped>
/* Add styles for the theatres page */
.theatres-page {
  background:transparent;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

ul {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  padding: 0;
  justify-content: center;
}

h1 {
  color: #001232;
}

li {
  width: 50%; /* Half-screen on laptops */
  min-width: 100%; /* Full-screen on PCs */
  margin: 10px;
}

.theatre-card {
  /* Add styles for the card container */
  background-color: white;
  color: black; /* Set text color to black or another visible color */
  padding: 20px;
  margin: 10px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.empty {
  margin-top: 15%;
  color: white;
  text-align: center;
}

.theatre-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcomeText {
  text-align: center;
}

.theatresMessage {
  display: block;
  justify-content: left;
  margin-bottom: -30px;
  margin-left: 15px;
}

.theatresText {
  color: #ff5252;
}

.theatre-header h3 {
  margin: 0;
  color: black;
}

.showboxes {
  display: flex;
}

.actions {
  display: flex;
  align-items: center;
}

.add-show-btn,
.edit-btn,
.delete-btn {
  margin-left: 10px;
}

.add-show-btn i {
  font-size: 14px;
}

.show-list {
  margin-top: 10px;
  color: black;
}

.show-list ul {
  padding-left: 20px;
  list-style: disc;
}

.show-list li {
  margin-bottom: 5px;
}

.add-theatre-btn {
  /* Add styles for the circular add button to add a theatre */
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 10px auto;
}

.create-btn {
  /* Add styles for the create button at the bottom */
  margin-top: 20px;
}
</style>
