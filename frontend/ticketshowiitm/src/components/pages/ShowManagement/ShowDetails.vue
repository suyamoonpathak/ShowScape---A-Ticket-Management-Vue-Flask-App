<template>
  <div class="full-page">
    <div class="show-details-page">
      <CustomHeading1>Show Details</CustomHeading1>
      <div class="wrapper">
        <div class="show-image">
          <img src="./../../../assets/poster.jpg">
        </div>
        <div style="color:white" class="show-details">
          <CustomHeading1>{{ show.name }}</CustomHeading1>
          <CustomParagraph class="detail duration">{{calculateDuration(show.start_time,show.end_time)}}</CustomParagraph>
          <CustomTags :tagString="show.tags" class="tags"></CustomTags>
          <p><star-rating v-model:rating="show.rating" :read-only="true" :increment="0.01" active-color="#ff5252" :show-rating="false" :star-size="30"></star-rating></p>
          <hr class="hr-top">
          <CustomParagraph class="detail">Release Date: {{ formatDate(show.date) }}</CustomParagraph>
          <CustomParagraph class="detail">Airing at {{ formatTime(show.start_time) }}</CustomParagraph>
          <hr class="hr-bottom">
          <CustomParagraph class="detail price">${{ show.ticket_price }}</CustomParagraph>
          <div class="btn-group">
            <CustomAppButton secondary @click="goToTrailer" class="btn">Watch Trailer</CustomAppButton>
            <CustomAppButton class="btn" v-if="userRole === 'client'">Grab Tickets</CustomAppButton>
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
  import CustomTags from "./../../common/CustomTags.vue"
  import CustomAppButton from "./../../common/CustomAppButton.vue"
  import StarRating from 'vue-star-rating'
  import {formatTime} from "./../../../../utils/formatTimeUtils"
  import { formatDate } from "./../../../../utils/formatDateUtils"
  import { formatCSV } from "./../../../../utils/formatCSVUtils"
  import { calculateDuration } from "./../../../../utils/timeDifferenceUtils"
  import { decodeJwtToken } from "./../../../../utils/jwtUtils";
  
  export default {
    name: "ShowDetails",
    data() {
      return {
        show: {},
        userRole:null,
      };
    },
    components:{
      CustomHeading1,StarRating,CustomParagraph,CustomTags,CustomAppButton
    },
    mounted() {
      this.getShowDetails();
      this.getUserRole();
    },
    methods: {
      getShowDetails() {
        // Get the show ID from the route params
        const showId = this.$route.params.id;
  
        // Make API call to get show details by ID
        axios.get(`http://localhost:5000/api/shows/${showId}`)
          .then((response) => {
            this.show = response.data;
          })
          .catch((error) => {
            console.error("Error getting show details:", error);
          });
      },
      formatTime,formatDate,formatCSV,calculateDuration,
      goToTrailer(){
        window.open('https://www.youtube.com', '_blank');
      },
      getUserRole(){
        const accessToken = localStorage.getItem("access_token");
        const jwtPayload = decodeJwtToken(accessToken);
        this.userRole = jwtPayload.role;
        }
    },
  };
  </script>
  
  <style scoped>
.show-details-page{
  display: block;
}

img{
  height: 600px;
}

.wrapper{
  display: flex;
}

.show-image{
  margin-right: 5%;
}

.detail{
  font-size: 20px;
  margin-bottom: 5px;
}

.duration{
  margin-top: -20px;
  margin-bottom: 20px;
  font-size: 16px;
  color: #ff5252;
}

.tags{
  margin-left: -7px;
  margin-bottom: 10px;
}

.hr-top{
  margin-top: 40px;
  margin-bottom: 15px;
}
.hr-bottom{
  margin-bottom: 40px;
  margin-top: 15px;
}

.btn{
  display: block;
}
.btn-group{
display: flex;
flex-direction: column;
justify-content: center;
}

.price{
  font-size: 40px;
  text-align: center;
}
.full-page{
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top:5%
}

.show-details{
  width: 300px;
}


  </style>
  