<template>
  <div class="full-page">
    <div class="edit-show-page">
      <CustomHeading1 class="heading">Edit Show</CustomHeading1>

      <div>
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
        <CustomInputText
          label="Trailer URL"
          type="url"
          placeholder="Enter updated trailer URL"
          :value="trailer_url"
          @update:value="trailer_url = $event"
        />
        <div class="poster-wrapper">
          <CustomInputText
            :type="'file'"
            :label="'Upload Poster'"
            :inputId="'poster'"
            @change="onFileChange"
            accept="image/*"
            style="display: none"
          />
          <CustomAppButton
            @click="openFileInput"
            secondary
            class="upload-poster-btn"
          >
            Edit Poster
          </CustomAppButton>
          <div v-if="posterDisplay" class="poster-img-div">
            <img :src="posterDisplay" alt="Poster Preview" class="image-preview" />
          </div>
        </div>
        <div class="btn">
          <CustomAppButton @click="submit">Save Changes</CustomAppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CustomHeading1 from "../../common/CustomHeading1.vue";
import CustomInputText from "../../common/CustomTextInput.vue";
import CustomAppButton from "../../common/CustomAppButton.vue";
import { formatTime } from "./../../../../utils/formatTimeUtils";
import { formatDate } from "./../../../../utils/formatDateUtils";
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
      date: null,
      user_id: null,
      trailer_url: "",
      posterDisplay: null,
      posterApi: null,
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
      // Make an API call to fetch the show details based on 'showId'
      // Replace the URL with your backend API endpoint for fetching show details
      await axios
        .get(`http://localhost:5000/api/shows/${this.showId}`)
        .then((response) => {
          this.name = response.data.name;
          this.rating = response.data.rating;
          this.tags = response.data.tags;
          this.ticketPrice = response.data.ticket_price;
          this.startTime = formatTime(response.data.start_time);
          this.endTime = formatTime(response.data.end_time);
          this.date = formatDate(response.data.date);
          this.trailer_url = response.data.trailer_url;
          this.posterDisplay = require(`./../../../../../../backend/static/images/${response.data.poster}`);
          
        })
        .catch((error) => {
          console.error("Error fetching show details:", error);
        });
    },
    submit() {
      const theatreId = this.$route.params.theaterid;

      const formData = new FormData();
      formData.append("name", this.name);
      formData.append("rating", this.rating);
      formData.append("tags", this.tags);
      formData.append("ticket_price", this.ticketPrice);
      formData.append("theatre_id", theatreId);
      formData.append("start_time", this.startTime);
      formData.append("end_time", this.endTime);
      formData.append("date", this.date);
      formData.append("user_id", this.user_id);
      formData.append("trailer_url", this.trailer_url);

      var posterFile = null;
      if(this.posterApi){
        posterFile = new File([this.posterApi], "poster.jpg", {
          type: this.posterApi.type,
        });
      }
      formData.append("poster", posterFile);


      // Make API call to create a new show
      axios
        .put(`http://localhost:5000/api/shows/${this.showId}`, formData, {
          headers: {
            "Content-Type": "multipart/form-data", // Set the content type to handle file upload
          },
        })
        .then((response) => {
          console.log("Show created successfully:", response.data);
          // Redirect to the ShowList page after successful creation
          this.$router.push("/AdminHome");
        })
        .catch((error) => {
          console.error("Error creating show:", error);
        });
    },

    formatTime,
    formatDate,
    getUserId() {
      const accessToken = localStorage.getItem("access_token");
      const jwtPayload = decodeJwtToken(accessToken);
      this.user_id = jwtPayload.admin_id;
    },
    openFileInput() {
      // When the button is clicked, trigger the click event of the file input
      document.getElementById("poster").click();
    },
    onFileChange(event) {
      const selectedFile = event.target.files[0];
      this.posterDisplay = URL.createObjectURL(selectedFile);
      this.posterApi = selectedFile;
    },
  },
};
</script>

<style scoped>
/* Add styles for the edit show page if needed */
.edit-show-page {
  display: block;
  width: 50%;
}

.full-page {
  display: flex;
  justify-content: center;
  padding-top: 2%;
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

.image-preview {
  width: 80px;
  height: 120px;
  margin-right: 100px;
}

.poster-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-poster-btn {
  margin-left: 10%;
}
</style>
