<template>
  <div class="full-page">
  <div class="edit-show-page">
    <CustomHeading1 class="heading">Edit Show</CustomHeading1>

    <form @submit.prevent="submit">
      <CustomInputText
        label="Name"
        type="text"
        placeholder="Enter updated name"
        :value="name"
        @update:value="name = $event"
      />
      <CustomInputText
        label="Rating"
        type="number"
        placeholder="Enter updated rating"
        :value="rating"
        @update:value="rating = $event"
      />
      <CustomInputText
        label="Tags"
        type="text"
        placeholder="Enter updated tags"
        :value="tags"
        @update:value="tags = $event"
      />
      <CustomInputText
        label="Ticket Price"
        type="number"
        placeholder="Enter updated ticket price"
        :value="ticketPrice"
        @update:value="ticketPrice = $event"
      />
      <CustomInputText
        label="Start Time"
        type="time"
        placeholder="Enter udated starting time of the show"
        :value="startTime"
        required="true"
        @update:value="startTime = $event"
      />
      <CustomInputText
        label="End Time"
        type="time"
        placeholder="Enter updated ending time of the show"
        :value="endTime"
        required="true"
        @update:value="endTime = $event"
      />
      <CustomInputText
        label="Date"
        type="date"
        placeholder="Enter updated date of the show"
        :value="date"
        required="true"
        @update:value="date = $event"
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
import {formatTime} from "./../../../../utils/formatTimeUtils"
import { formatDate } from "./../../../../utils/formatDateUtils"
import { decodeJwtToken } from "./../../../../utils/jwtUtils";

export default {
  name: "EditShow",
  data() {
    return {
      showId: this.$route.params.showid,
      theatre_id: this.$route.params.theaterid,
      name: "",
      rating: null,
      tags: "",
      ticketPrice: null,
      startTime: null,
      endTime: null,
      date:null,
      user_id:null,
    };
  },
  components: {
    CustomHeading1,
    CustomInputText,
    CustomAppButton,
  },
  mounted() {
    // Fetch the show details from the backend API based on the route parameter 'id'
    this.fetchShowDetails();
    this.getUserId();
  },
  methods: {
    async fetchShowDetails() {
      console.log(this.showId,this.theatre_id);
      // Make an API call to fetch the show details based on 'showId'
      // Replace the URL with your backend API endpoint for fetching show details
      await axios
        .get(`http://localhost:5000/api/shows/${this.showId}`)
        .then((response) => {
          this.name = response.data.name;
          this.rating=response.data.rating;
          this.tags=response.data.tags;
          this.ticketPrice=response.data.ticket_price;
          this.startTime=formatTime(response.data.start_time);
          this.endTime=formatTime(response.data.end_time);
          this.date=formatDate(response.data.date);
        })
        .catch((error) => {
          console.error("Error fetching show details:", error);
        });
    },
    submit() {
      const updatedShow = {
        name: this.name,
        rating: this.rating,
        tags: this.tags,
        ticket_price: this.ticketPrice,
        theatre_id: this.theatre_id,
        start_time:this.startTime,
        end_time:this.endTime,
        date:this.date,
        user_id:this.user_id
      };
      // Make an API call to update the show details based on 'showId'
      // Replace the URL with your backend API endpoint for updating show details
      axios
        .put(`http://localhost:5000/api/shows/${this.showId}`, updatedShow)
        .then((response) => {
          console.log("Show updated successfully:", response.data);
          // Redirect back to the show details page after successful update
          this.$router.push("/AdminHome");
        })
        .catch((error) => {
          console.error("Error updating show:", error);
          // Show error message to the user if needed
        });
    },
    formatTime,formatDate,
    getUserId(){
        const accessToken = localStorage.getItem("access_token");
        const jwtPayload = decodeJwtToken(accessToken);
        this.user_id = jwtPayload.admin_id;
        console.log(this.user_id);
        }
  },
};
</script>

<style scoped>
/* Add styles for the edit show page if needed */
.edit-show-page {
  display: block;
  width: 50%;
}

.full-page{
  display: flex;
  justify-content: center;
  padding-top: 5%;
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
</style>
