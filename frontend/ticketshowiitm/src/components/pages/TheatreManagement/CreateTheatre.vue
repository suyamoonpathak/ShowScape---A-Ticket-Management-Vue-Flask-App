<template>
  <div class="create-theatre-page">
    <CustomHeading1 class="heading">Create Theatre</CustomHeading1>
    <form @submit.prevent="submit">
      <CustomInputText
        label="Name"
        type="text"
        placeholder="Enter theatre name"
        :value="name"
        required="true"
        @update:value="name = $event"
      />
      <CustomInputText
        label="Place"
        type="text"
        placeholder="Enter theatre place"
        :value="place"
        required="true"
        @update:value="place = $event"
      />
      <CustomInputText
        label="Capacity"
        type="number"
        placeholder="Enter theatre capacity"
        :value="capacity"
        required="true"
        @update:value="capacity = $event"
      />
      <div class="btn">
        <CustomAppButton type="submit">Save Changes</CustomAppButton>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { decodeJwtToken } from "../../../../utils/jwtUtils";
import CustomHeading1 from "../../common/CustomHeading1.vue";
import CustomInputText from "../../common/CustomTextInput.vue";
import CustomAppButton from "../../common/CustomAppButton.vue";

export default {
  name: "EditTheatre",
  data() {
    return {
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
  methods: {
    submit() {
      if (!this.name || !this.place || !this.capacity) {
        alert("Enter all the fields");
      } else {
        const accessToken = localStorage.getItem("access_token");
        const jwtPayload = decodeJwtToken(accessToken);
        const admin_id = jwtPayload.admin_id;
        const newTheatre = {
          name: this.name,
          place: this.place,
          capacity: this.capacity,
          admin_id: admin_id,
        };
        // Make an API call to update the theatre details based on 'theatreId'
        // Replace the URL with your backend API endpoint for updating theatre details
        axios
          .post("https://showscape-backend.onrender.com/api/theatres", newTheatre)
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
.create-theatre-page {
  display: block;
  padding: 10% 20%;
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
  .create-theatre-page {
    padding: 10% 0px;
  }
}
</style>
