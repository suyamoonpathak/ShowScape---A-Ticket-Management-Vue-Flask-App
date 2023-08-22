<template>
  <div class="full-page">
    <div class="edit-theatre-page">
      <CustomHeading1 class="heading">Edit Theatre</CustomHeading1>

      <form @submit.prevent="submit">
        <CustomInputText
          label="Name"
          type="text"
          placeholder="Enter updated name"
          :value="name"
          @update:value="name = $event"
        />
        <CustomInputText
          label="Place"
          type="text"
          placeholder="Enter updated place"
          :value="place"
          @update:value="place = $event"
        />
        <CustomInputText
          label="Capacity"
          type="number"
          placeholder="Enter updated capacity"
          :value="capacity"
          @update:value="capacity = $event"
        />
        <div class="btn">
          <CustomAppButton type="submit">Save Changes</CustomAppButton>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CustomHeading1 from "../../common/CustomHeading1.vue";
import CustomInputText from "../../common/CustomTextInput.vue";
import CustomAppButton from "../../common/CustomAppButton.vue";

export default {
  name: "EditTheatre",
  data() {
    return {
      theatreId: this.$route.params.id,
      name: "",
      place: "",
      capacity: "",
    };
  },
  components: {
    CustomHeading1,
    CustomInputText,
    CustomAppButton,
  },
  mounted() {
    // Fetch the theatre details from the backend API based on the route parameter 'id'
    this.fetchTheatreDetails();
  },
  methods: {
    async fetchTheatreDetails() {
      // Make an API call to fetch the theatre details based on 'theatreId'
      // Replace the URL with your backend API endpoint for fetching theatre details
      await axios
        .get(`https://showscape-backend.onrender.com/api/theatres/${this.theatreId}`)
        .then((response) => {
          this.name = response.data.name;
          this.place = response.data.place;
          this.capacity = response.data.capacity;
        })
        .catch((error) => {
          console.error("Error fetching theatre details:", error);
        });
    },
    submit() {
      if (!this.name || !this.place || !this.capacity) {
        alert("Enter all the fields");
      } else {
        const updatedTheatre = {
          name: this.name,
          place: this.place,
          capacity: this.capacity,
        };
        // Make an API call to update the theatre details based on 'theatreId'
        // Replace the URL with your backend API endpoint for updating theatre details
        axios
          .put(
            `https://showscape-backend.onrender.com/api/theatres/${this.theatreId}`,
            updatedTheatre
          )
          .then((response) => {
            console.log("Theatre updated successfully:", response.data);
            // Redirect back to the theatre details page after successful update
            this.$router.push("/AdminHome");
          })
          .catch((error) => {
            console.error("Error updating theatre:", error);
            // Show error message to the user if needed
          });
      }
    },
  },
};
</script>

<style scoped>
/* Add styles for the edit theatre page if needed */
.edit-theatre-page {
  display: block;
  width: 50%;
}

.full-page {
  display: flex;
  justify-content: center;
  padding-top: 10%;
}

.heading {
  text-align: center;
}

.btn {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .edit-theatre-page {
    width: 100%;
  }
}
</style>
