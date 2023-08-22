<template>
  <div class="show-banner-for-search" @click="redirectToShowDetails">
    <div class="poster-img-div">
      <img
        v-if="show.poster"
        :src="getImageUrl(show.poster)"
        alt="Poster Image"
        class="poster"
        @click="showDetails(show.id)"
      />
    </div>
    <div class="details">
      <div class="desc">
        <CustomHeading1 class="heading">{{ getFirstThreeWordsWithEllipsis(show.name) }}</CustomHeading1>
        <CustomTags :tagString="getFirstThreeTags(show.tags)" class="tags"></CustomTags>
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
        <p><i class="fas fa-map-marker-alt" style="color: #ff5252"></i> {{ show.theatre_name }}, {{ show.theatre_place }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import CustomHeading1 from './CustomHeading1.vue';
import CustomTags from './CustomTags.vue';
import StarRating from "vue-star-rating";
import { getFirstThreeTags } from './../../../utils/getFirstThreeTagsUtils';
import { getFirstThreeWordsWithEllipsis } from './../../../utils/getFirstThreeWordsWithEllipsisUtils';
import { getImageUrl } from "./../../../utils/getImage";

export default {
  props: {
    show: {
      type: Object,
      required: true,
    },
  },
  data(){
    return {
      localRating:this.show.rating
    }
  },
  components:{
    CustomHeading1,CustomTags,StarRating
  },
  methods:{
    redirectToShowDetails(){
      this.$router.push(`/show/${this.show.id}`)
    },getFirstThreeTags,getFirstThreeWordsWithEllipsis,getImageUrl
  }
};
</script>

<style scoped>
/* Add styling for the show banner */
p {
  color: white;
}

.show-banner-for-search {
  width: 700px;
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

.rating{
  display: flex;
  align-items: center;
}

.place{
  display: flex;
  align-items: center;
}

.desc{
  display: flex;
  flex-direction: column;
  align-items: baseline;
}

.heading{
  margin: 15px 0px;
  padding-top: 10px;
}

.tags{
  margin-top: -10px;
}

@media (max-width: 768px) {

    .heading, .tags, p{
      margin: 0;
      padding: 0;
      font-size: 20px;
    }

    .show-banner-for-search{
      width: 350px;
    }

    .details{
      flex-direction: column;
      margin-left: 5%;
    }

    p{
      font-size: 14px;
    }

  }

</style>
