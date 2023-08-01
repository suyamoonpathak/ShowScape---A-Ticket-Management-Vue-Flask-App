<template>
    <div class="my-bookings">
      <CustomHeading1>My Bookings</CustomHeading1>
      <div v-if="bookings.length > 0">
        <div v-for="booking in bookings" :key="booking.id" class="booking-item">
          <BookingList :booking="booking" />
        </div>
      </div>
      <div v-else>
        <p class="no-bookings">You haven't made any bookings yet.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import CustomHeading1 from "@/components/common/CustomHeading1.vue";
  import BookingList from "@/components/common/BookingList.vue";
  import { decodeJwtToken } from "./../../../../utils/jwtUtils";
  
  export default {
    name: "MyBookings",
    data() {
      return {
        bookings: [], // Array to store the user's bookings
      };
    },
    components: {
      CustomHeading1, BookingList
    },
    mounted() {
      // Fetch the user's bookings when the component is mounted
      this.fetchUserBookings();
    },
    methods: {
      async fetchUserBookings() {
        const userId = this.getUserId(); // Replace this with the actual function to get the logged-in user's ID
  
        try {
          // Fetch the user's bookings using the API endpoint
          const response = await axios.get(`http://localhost:5000/api/users/${userId}/bookings`);
          this.bookings = response.data;
        } catch (error) {
          console.error("Error fetching user bookings:", error);
        }
      },
      getUserId() {
      const accessToken = localStorage.getItem("access_token");
      const jwtPayload = decodeJwtToken(accessToken);
      return jwtPayload.user_id;
    },
    },
  };
  </script>
  
  <style scoped>
  .my-bookings {
    margin-top: 20px;
    padding: 5% 10% 0 10%;
  }

  </style>
  