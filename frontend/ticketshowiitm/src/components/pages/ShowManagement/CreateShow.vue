<template>
  <div class="full-page">
  <div class="create-show">
    <CustomHeading1 class="heading">Create Show</CustomHeading1>
    <form @submit.prevent="submitForm">
      <CustomInputText
        label="Name"
        type="text"
        placeholder="Enter show name"
        :value="name"
        required="true"
        @update:value="name = $event"
      />
      <CustomInputText
        label="Rating"
        type="number"
        placeholder="Enter show rating"
        :value="rating"
        required="true"
        pattern="^(?:[0-5](?:\.[0-9]*)?|5(?:\.0*)?)$"
        @update:value="rating = $event"
      />
      <CustomInputText
        label="Tags"
        type="string"
        placeholder="Enter show tags separated by comma"
        :value="tags"
        required="true"
        @update:value="tags = $event"
      />
      <CustomInputText
        label="Ticket Price"
        type="number"
        placeholder="Enter ticket price of the show"
        :value="ticketPrice"
        required="true"
        @update:value="ticketPrice = $event"
      />
      <CustomInputText
        label="Start Time"
        type="time"
        placeholder="Enter starting time of the show"
        :value="startTime"
        required="true"
        @update:value="startTime = $event"
      />
      <CustomInputText
        label="End Time"
        type="time"
        placeholder="Enter ending time of the show"
        :value="endTime"
        required="true"
        @update:value="endTime = $event"
      />
      <CustomInputText
        label="Date"
        type="date"
        placeholder="Enter the date of the show"
        :value="date"
        required="true"
        @update:value="date = $event"
      />
      <div class="btn">
      <CustomAppButton type="submit">Create</CustomAppButton>
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
import { decodeJwtToken } from "./../../../../utils/jwtUtils";

export default {
  name: "CreateShow",
  data() {
    return {
      name: "",
      rating: "",
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
    this.getUserId();
  },
  methods: {
    submitForm() {
      const theatreId = this.$route.params.id;
      console.log(theatreId);
      const newShow = {
        name: this.name,
        rating: this.rating,
        tags: this.tags,
        ticket_price: this.ticketPrice,
        theatre_id: theatreId,
        start_time:this.startTime,
        end_time:this.endTime,
        date:this.date,
        user_id:this.user_id
      };
      console.log(newShow);
      // Make API call to create a new show
      axios.post("http://localhost:5000/api/shows", newShow)
        .then((response) => {
          console.log("Show created successfully:", response.data);
          // Redirect to the ShowList page after successful creation
          this.$router.push("/AdminHome");
        })
        .catch((error) => {
          console.error("Error creating show:", error);
        });
    },
    getUserId(){
        const accessToken = localStorage.getItem("access_token");
        const jwtPayload = decodeJwtToken(accessToken);
        this.user_id = jwtPayload.admin_id;
        console.log(this.user_id);
        }
  },
};
</script>

<style>
.create-show {
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