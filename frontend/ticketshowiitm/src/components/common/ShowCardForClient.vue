<template>
  <div class="show-card">
    <div class="poster-div" @mouseover="zoomIn" @mouseleave="zoomOut">
      <img
        v-if="show.poster"
        :src="require(`./../../../../../backend/static/images/${show.poster}`)"
        alt="Poster Image"
        class="poster"
        @click="showDetails(show.id)"
      />
    </div>
    <div class="details">
      <div class="inner-details">
        <p class="name" @click="showDetails(show.id)">{{ getFirstThreeWordsWithEllipsis(show.name) }}</p>
        <star-rating
          v-model:rating="localRating"
          :read-only="true"
          :increment="0.01"
          active-color="#ff5252"
          :show-rating="false"
          :star-size="20"
          class="stars"
        ></star-rating>
        <CustomTags
          :tagString="getFirstThreeTags(show.tags)"
          class="tags"
          center
        ></CustomTags>
        <CustomParagraph class="available-seats" v-if="available_seats > 0"
          >({{ available_seats }} tickets available)</CustomParagraph
        >
        <CustomParagraph class="houseful" v-else
          >Houseful!
          <i class="fa-solid fa-face-sad-tear" style="color: #ff5252"></i>
        </CustomParagraph>
      </div>
    </div>
  </div>
</template>

<script>
import StarRating from "vue-star-rating";
import CustomTags from "./CustomTags.vue";
import CustomParagraph from "./CustomParagraph.vue";
import {getFirstThreeTags} from "./../../../utils/getFirstThreeTagsUtils"
import {getFirstThreeWordsWithEllipsis} from "./../../../utils/getFirstThreeWordsWithEllipsisUtils"

export default {
  props: {
    show: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      localRating: this.show.rating, // Initialize the local data property with show.rating
      isZoomed: false,
      available_seats: this.show.available_seats,
    };
  },
  components: {
    StarRating,
    CustomTags,
    CustomParagraph,
  },
  methods: {
    zoomIn() {
      this.isZoomed = true;
    },
    zoomOut() {
      this.isZoomed = false;
    },
    showDetails(showId) {
      // Redirect to ShowDetails page for the selected show
      this.$router.push(`/show/${showId}`);
    }, getFirstThreeTags, getFirstThreeWordsWithEllipsis
  },
};
</script>

<style scoped>
.show-card {
  height: 505px;
  width: 250px;
  padding: 0 15px 0 15px;
  margin-bottom: 50px;
}

.poster {
  height: 100%;
  width: 100%;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.poster-div:hover img {
  transform: scale(
    1.05
  ); /* Increase the scale value to zoom in (e.g., 1.1 for 10% zoom) */
}

.details {
  background-color: #001232;
  padding: 0 20px;
  margin-top: -4px;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}

p {
  margin: 0;
}

.name {
  padding: 15px 0;
  font-size: 20px;
  color: white;
  font-weight: bold;
  border-bottom: #476697 dashed 0.5px;
  cursor: pointer;
}

.tags {
  margin-bottom: 3px;
}

.name:hover {
  color: #ff5252;
}

.available-seats {
  color: #6fdf67;
}

.inner-details {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stars {
  margin: 10px 0px;
}

.houseful {
  color: #ff5252;
}
</style>
