<template>
  <div class="full-page">
    <div class="show-details-page">
      <CustomHeading1>Show Details</CustomHeading1>
      <div class="wrapper">
        <div class="show-image">
          <!-- Bind the src attribute to the correct URL of the poster image -->
          <img
            v-if="show.poster"
            :src="
              require(`./../../../../../../backend/static/images/${show.poster}`)
            "
            alt="Poster Image"
            class="poster"
          />
        </div>
        <div style="color: white" class="show-details">
          <CustomHeading1>{{ show.name }}</CustomHeading1>
          <CustomParagraph class="detail duration">{{
            calculateDuration(show.start_time, show.end_time)
          }}</CustomParagraph>
          <CustomTags :tagString="show.tags" class="tags"></CustomTags>
          <p>
            <star-rating
              v-model:rating="show.rating"
              :read-only="true"
              :increment="0.01"
              active-color="#ff5252"
              :show-rating="false"
              :star-size="30"
            ></star-rating>
          </p>
          <hr class="hr-top" />
          <CustomParagraph class="detail"
            ><i class="far fa-calendar-alt" style="color: #ff5252;"></i> {{ formatDate(show.date) }}</CustomParagraph
          >
          <CustomParagraph class="detail"
            ><i class="far fa-clock" style="color: #ff5252;"></i> {{ formatTime(show.start_time) }}</CustomParagraph
          >
          <CustomParagraph class="detail">
            <i class="fas fa-map-marker-alt" style="color: #ff5252"></i>
            {{ theater.name }}, {{ theater.place }}
          </CustomParagraph>
          <hr class="hr-bottom" />
          <CustomParagraph class="detail price"
            >${{ show.ticket_price }}</CustomParagraph
          >
          <div class="btn-group">
            <CustomAppButton secondary @click="goToTrailer" class="btn"
              >Watch Trailer</CustomAppButton
            >
            <CustomAppButton class="btn" v-if="userRole === 'client' && show.available_seats>0"
              >Grab Tickets</CustomAppButton
            >
            <CustomParagraph class="houseful" v-if="userRole === 'client' && show.available_seats<=0"
              >Houseful! <i class="fa-solid fa-face-sad-tear" style="color: #ff5252;"></i></CustomParagraph
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CustomHeading1 from "./../../common/CustomHeading1.vue";
import CustomParagraph from "./../../common/CustomParagraph.vue";
import CustomTags from "./../../common/CustomTags.vue";
import CustomAppButton from "./../../common/CustomAppButton.vue";
import StarRating from "vue-star-rating";
import { formatTime } from "./../../../../utils/formatTimeUtils";
import { formatDate } from "./../../../../utils/formatDateUtils";
import { formatCSV } from "./../../../../utils/formatCSVUtils";
import { calculateDuration } from "./../../../../utils/timeDifferenceUtils";
import { decodeJwtToken } from "./../../../../utils/jwtUtils";

export default {
  name: "ShowDetails",
  data() {
    return {
      show: {},
      userRole: null,
      theater: {},
    };
  },
  components: {
    CustomHeading1,
    StarRating,
    CustomParagraph,
    CustomTags,
    CustomAppButton,
  },
  mounted() {
    this.getShowDetails();
    this.getUserRole();
  },
  methods: {
    async getShowDetails() {
      const showId = this.$route.params.id;

      try {
        // Fetch show details
        const showResponse = await axios.get(
          `http://localhost:5000/api/shows/${showId}`
        );
        this.show = showResponse.data;

        // Fetch theater details using the theater_id from the show object
        const theaterResponse = await axios.get(
          `http://localhost:5000/api/theatres/${this.show.theatre_id}`
        );
        this.theater = theaterResponse.data;

        console.log(this.show);
        console.log(this.theater);
      } catch (error) {
        console.error("Error getting show and theater details:", error);
      }
    },
    formatTime,
    formatDate,
    formatCSV,
    calculateDuration,
    goToTrailer() {
      const trailerUrl = this.show.trailer_url;
      if (trailerUrl) {
        window.open(trailerUrl, "_blank");
      } else {
        console.log("Trailer URL not available.");
        // Show an error message or handle the case where the trailer URL is not available
      }
    },
    getUserRole() {
      const accessToken = localStorage.getItem("access_token");
      const jwtPayload = decodeJwtToken(accessToken);
      this.userRole = jwtPayload.role;
    },
    getPosterImageUrl(posterFilename) {
      // Replace this path with the actual path to your images

      const imagePath = "./../../../../../../backend/static/images/";
      console.log(`${imagePath}${posterFilename}`);
      return `${imagePath}${posterFilename}`;
    },
  },
};
</script>

<style scoped>
.show-details-page {
  display: block;
}

img {
  height: 600px;
}

.wrapper {
  display: flex;
}

.show-image {
  margin-right: 5%;
}

.detail {
  font-size: 20px;
  margin-bottom: 5px;
}

.duration {
  margin-top: -20px;
  margin-bottom: 20px;
  font-size: 16px;
  color: #ff5252;
}

.tags {
  margin-bottom: 10px;
}

.hr-top {
  margin-top: 20px;
  margin-bottom: 15px;
}
.hr-bottom {
  margin-bottom: 20px;
  margin-top: 15px;
}

.btn-group {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.price {
  font-size: 40px;
  text-align: center;
}
.full-page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 5%;
}

.show-details {
  width: 300px;
}

.poster {
  width: 400px;
  height: 600px;
}

.houseful{
  text-align: center;
  margin-top: 30px;
  color:#ff5252;
  font-size: 30px;
  font-weight: bolder;
}
</style>
