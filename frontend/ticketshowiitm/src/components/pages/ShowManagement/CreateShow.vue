<template>
  <div class="full-page">
    <div class="create-show">
      <CustomHeading1 class="heading">Create Show</CustomHeading1>
      <div class="form">
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
        <CustomInputText
          label="Trailer URL"
          type="url"
          placeholder="Enter url for the trailer"
          :value="trailer_url"
          required="true"
          @update:value="trailer_url = $event"
        />
        <div class="poster-wrapper">
          >
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
            >Upload Poster</CustomAppButton
          >
          <div v-if="posterDisplay" class="poster-img-div">
            <img
              :src="posterDisplay"
              alt="Poster Preview"
              class="image-preview"
            />
          </div>
        </div>
        <div class="btn">
          <CustomAppButton @click="submitForm">Create Show</CustomAppButton>
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
      date: null,
      user_id: null,
      trailer_url: null,
      posterDisplay: null,
      posterApi: null,
      posterURL: null,
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
      if (this.posterApi) {
        posterFile = new File([this.posterApi], "poster.jpg", {
          type: this.posterApi.type,
        });
      }
      formData.append("poster", posterFile);
      // formData.append("poster",this.poster);

      // Make API call to create a new show
      axios
        .post("http://localhost:5000/api/shows", formData, {
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

<style>
.create-show {
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

.image-preview {
  margin-top: 10px;
  max-width: 300px; /* Adjust the size of the preview image */
}

.btn {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.image-preview {
  width: 80px;
  height: 120px;
  margin-left: 425px;
}

.poster-wrapper {
  display: flex;
  align-items: center;
}

.upload-poster-btn {
  margin-left: 10%;
}

@media (max-width: 768px) {
  .create-show {
    width: 100%;
  }

  .image-preview {
    margin: 0px;
  }

  .form{
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .upload-poster-btn{
    margin: 0;
    margin-right: 15px;
  }

  .full-page{
    padding-bottom: 20px;
  }
}
</style>
