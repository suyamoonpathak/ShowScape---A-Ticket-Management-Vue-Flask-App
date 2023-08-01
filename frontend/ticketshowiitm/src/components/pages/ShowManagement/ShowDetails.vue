<template>
  <div class="full-page">
    <div class="show-details-page">
      <CustomHeading1>Show Details</CustomHeading1>
      <div class="wrapper">
        <div class="show-image">
          <div class="availability-overlay">
            <span
              class="availability-text success"
              v-if="show.available_seats > 0"
            >
              {{ show.available_seats }} Tickets Available
            </span>
            <span class="availability-text danger" v-else>
              No Tickets Available
            </span>
          </div>
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
            ><i class="far fa-calendar-alt" style="color: #ff5252"></i>
            {{ formatDate(show.date) }}</CustomParagraph
          >
          <CustomParagraph class="detail"
            ><i class="far fa-clock" style="color: #ff5252"></i>
            {{ formatTime(show.start_time) }}</CustomParagraph
          >
          <CustomParagraph class="detail">
            <i class="fas fa-map-marker-alt" style="color: #ff5252"></i>
            {{ theater.name }}, {{ theater.place }}
          </CustomParagraph>
          <div class="btn-group">
            <CustomAppButton secondary @click="goToTrailer" class="btn"
              >Watch Trailer</CustomAppButton
            >
          </div>
          <hr class="hr-bottom" />
          <CustomParagraph class="detail price"
            >${{ show.ticket_price }}</CustomParagraph
          >
          <div class="ticket-wrapper-div">
            <div
              class="ticket-input"
              v-if="userRole === 'client' && show.available_seats > 0"
            >
              <CustomAppButton
                secondary
                @click="decreaseTickets"
                class="arrow-btn"
              >
                <i class="fa-solid fa-arrow-down"></i>
              </CustomAppButton>
              <div class="number-of-tickets">{{ this.numberOfTickets }}</div>
              <i class="fa-solid fa-ticket fa-2xl" style="color: #ff5656"></i>
              <CustomAppButton
                @click="increaseTickets"
                class="arrow-btn"
                :disabled="numberOfTickets >= show.available_seats"
              >
                <i class="fa-solid fa-arrow-up fa-beat-fade"></i>
              </CustomAppButton>
            </div>
            <div class="btn-group">
              <CustomAppButton
                class="btn"
                v-if="userRole === 'client' && show.available_seats > 0"
                @click="submit"
                >Grab Tickets</CustomAppButton
              >
              <CustomParagraph
                class="houseful"
                v-if="userRole === 'client' && show.available_seats <= 0"
                >Houseful!
                <i class="fa-solid fa-face-sad-tear" style="color: #ff5252"></i
              ></CustomParagraph>
            </div>
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
      numberOfTickets: 1,
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
      }
    },
    getUserRole() {
      const accessToken = localStorage.getItem("access_token");
      const jwtPayload = decodeJwtToken(accessToken);
      this.userRole = jwtPayload.role;
    },
    getUserId() {
      const accessToken = localStorage.getItem("access_token");
      const jwtPayload = decodeJwtToken(accessToken);
      return jwtPayload.user_id;
    },
    getPosterImageUrl(posterFilename) {
      const imagePath = "./../../../../../../backend/static/images/";
      console.log(`${imagePath}${posterFilename}`);
      return `${imagePath}${posterFilename}`;
    },
    decreaseTickets() {
      if (this.numberOfTickets > 1) {
        this.numberOfTickets--;
      }
    },
    increaseTickets() {
      if (this.numberOfTickets < this.show.available_seats) {
        this.numberOfTickets++;
      }
    },
    async submit() {
    if (this.numberOfTickets < 1 || this.numberOfTickets > this.show.available_seats) {
      alert("Invalid number of tickets.");
      return;
    }

    const userId = this.getUserId(); // Replace this with the actual function to get the logged-in user's ID
    const showId = this.show.id;
    const numTickets = this.numberOfTickets;

    try {
      // Create a booking entry in the database
      await axios.post("http://localhost:5000/api/bookings", {
        user_id: userId,
        show_id: showId,
        num_tickets: numTickets,
      });
      this.$router.push('/booking-success');

    } catch (error) {
      console.error("Error creating booking:", error);
      this.$router.push('/booking-failed');
    }
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
  position: relative;
  display: inline-block;
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
  margin-top: 10px;
  margin-bottom: 10px;
}
.hr-bottom {
  margin-bottom: 10px;
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

.houseful {
  text-align: center;
  margin-top: 30px;
  color: #ff5252;
  font-size: 30px;
  font-weight: bolder;
}

.btn {
  margin-top: 5px;
}

.ticket-input {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 5px;
}

.ticket-input-box {
  width: 60px;
  text-align: center;
  margin: 0 10px;
}

.arrow-btn {
  padding: 5px 10px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.number-of-tickets {
  font-size: 30px;
  font-weight: bold;
  color: #ff5252;
  margin: 0px 15px;
}

.fa-ticket {
  margin-right: 15px;
  margin-top: 2px;
}

.availability-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 40%;
  height: 10%;
  background-color: rgba(
    0,
    0,
    0,
    0.7
  ); /* Change the background color as desired */
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: white;
  border-bottom-right-radius: 5px;
}

.availability-text {
  padding: 10px;
  text-align: center;
}

.danger {
  color: red;
}

.success {
  color: #5bfc5b;
}
</style>
