<template>
  <div class="show-banner-for-search" @click="redirectToShowDetails">
    <div class="poster-img-div">
      <img
        v-if="booking.show.poster"
        :src="
          require(`./../../../../../backend/static/images/${booking.show.poster}`)
        "
        alt="Poster Image"
        class="poster"
        @click="redirectToShowDetails"
      />
    </div>
    <div class="details">
      <div class="desc">
        <CustomHeading1 class="heading">{{
          getFirstThreeWordsWithEllipsis(booking.show.name)
        }}</CustomHeading1
        >
        <CustomTags
          :tagString="getFirstThreeTags(booking.show.tags)"
          class="tags"
        ></CustomTags>
      </div>
      <div class="rating">
        <star-rating
          v-model:rating="localRating"
          :read-only="true"
          :increment="0.01"
          active-color="#ff5252"
          :show-rating="false"
          :star-size="20"
          class="stars"
        ></star-rating>
      </div>
      <div class="place">
        <p>
          <i class="fas fa-map-marker-alt" style="color: #ff5252"></i>
          {{ booking.theatre.name }}, {{ booking.theatre.place }}
        </p>
      </div>
      <div class="date">
        <p>
          <i class="far fa-calendar-alt" style="color: #ff5252"></i>
          {{ formatDate(booking.show.date) }} at
          {{ formatTime(booking.show.start_time) }}
        </p>
      </div>
      <div class="price">
        <p>
          <i class="fa-solid fa-money-check-dollar" style="color: #fa5656;"></i>
          ${{ booking.show.ticket_price }} x {{ booking.num_tickets }} = ${{
            totalPrice
          }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import CustomHeading1 from "./CustomHeading1.vue";
import CustomTags from "./CustomTags.vue";
import StarRating from "vue-star-rating";
import { formatDate } from "./../../../utils/formatDateUtils";
import { formatTime } from "./../../../utils/formatTimeUtils";
import { getFirstThreeTags } from "./../../../utils/getFirstThreeTagsUtils";
import { getFirstThreeWordsWithEllipsis } from "./../../../utils/getFirstThreeWordsWithEllipsisUtils";

export default {
  props: {
    booking: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      localRating: this.booking.show.rating,
      totalPrice:
        Math.round(
          this.booking.show.ticket_price * this.booking.num_tickets * 100
        ) / 100, //to round the number into two decimal points
    };
  },
  components: {
    CustomHeading1,
    CustomTags,
    StarRating,
  },
  methods: {
    redirectToShowDetails() {
      this.$router.push(`/show/${this.booking.show.id}`);
    },
    formatDate,
    formatTime,
    getFirstThreeTags,
    getFirstThreeWordsWithEllipsis,
  },
};
</script>

<style scoped>
/* Add styling for the show banner */
p {
  color: white;
}

.show-banner-for-search {
  width: 100%;
  height: 140px;
  background-color: #001232;
  margin: 10px 0px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  cursor: pointer;
  border-bottom: 1px dashed white;
}

.poster {
  width: 100px;
  height: 100%;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
}

.details {
  display: flex;
  width: 100%;
  justify-content: space-around;
}

.rating {
  display: flex;
  align-items: center;
}

.place {
  display: flex;
  align-items: center;
}

.date {
  display: flex;
  align-items: center;
}

.price {
  display: flex;
  align-items: center;
}

.desc {
  display: flex;
  flex-direction: column;
  align-items: left;
}

.heading {
  margin: 15px 0px;
  padding-top: 10px;
}

.tags {
  margin-top: -10px;
}

i{
  margin-right: 2px;
}

@media (max-width: 768px) {
  .tags, .rating{
    display: none;
  }
  .details{
    display: flex;
    flex-direction: column;
    padding-left: 5%;
    margin-top: -10px;
  }
  .heading,p,.desc {
    margin: 0;
    padding: 0;
  }

  .heading{
    text-align: left;
  }

}
</style>
