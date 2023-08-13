<template>
  <div class="theatre-summary-page">
    <Navbar :userRole="'admin'" class="nav" />
    <div class="graphs-div-wrapper">
      <div
        v-for="(theatreData, theatreName) in theatresData"
        :key="theatreName"
        class="graphs"
      >
        <SummaryGraph
          :capacityArray="theatreData.capacity_array"
          :revenueArray="theatreData.revenue_array"
          :theatreName="theatreName"
        />
      </div>
    </div>
  </div>
</template>
<script>
import Navbar from "../common/NavBar.vue";
import SummaryGraph from "../common/SummaryGraph.vue";
import { decodeJwtToken } from "./../../../utils/jwtUtils";
import axios from "axios";

export default {
  name: "TheatreSummary",
  data() {
    return {
      theatres: [],
      shows: [],
      theatresData: {}, // To store fetched theatre data
    };
  },
  components: {
    Navbar,
    SummaryGraph,
  },
  async mounted() {
    try {
      const accessToken = localStorage.getItem("access_token");
      const jwtPayload = decodeJwtToken(accessToken);
      const admin_id = jwtPayload.admin_id;
      const response = await axios.get(
        `http://localhost:5000/api/generate_arrays/${admin_id}`
      );
      this.theatresData = response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  },
};
</script>
<style>
body {
  background-color: #001232;
  background-image: url("./../../assets/bg2.jpg");
  background-repeat: no-repeat;
  background-size: cover;
}

.graphs {
  width: 50%;
}

.graphs-div-wrapper {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  margin-top: 2%;
}

@media (max-width: 768px) {
  .graphs {
    width: 95%;
  }

  .graphs-div-wrapper {
  margin-top: 5%;
}
}
</style>
