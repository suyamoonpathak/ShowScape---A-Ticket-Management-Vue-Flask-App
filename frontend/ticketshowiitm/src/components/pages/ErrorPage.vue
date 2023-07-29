<template>
  <div class="error-page">
    <div class="wrapper">
      <img src="./../../assets/error404.png" />
      <CustomAppButton class="btn" @click="goBack">Go back</CustomAppButton>
    </div>
  </div>
</template>

<script>
import CustomAppButton from "../common/CustomAppButton.vue";
export default {
  name: "ErrorPage",
  components: {
    CustomAppButton,
  },
  methods:{
    goBack(){
        this.$router.go(-1);
    }
  }
};
</script>

<style scoped>

img {
  padding-top: 100px;
  width: 600px;
  height: 550px;
}

.error-page {
  display: flex;
  justify-content: center;
  background-color: #001232 !important;
  width: 100%;
  height: 100vh;
}

.wrapper{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.btn{
    margin-top: 70px;
}
</style>
