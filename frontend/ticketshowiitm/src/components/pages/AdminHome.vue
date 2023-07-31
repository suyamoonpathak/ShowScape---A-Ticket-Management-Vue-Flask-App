<template>
  <div class="admin-home-page">
    <Navbar :userRole="'admin'" class="nav" />
    <TheatresListForAdmin class="theatres"></TheatresListForAdmin>
  </div>
</template>
<script>
import Navbar from "../common/NavBar.vue";
import TheatresListForAdmin from "./TheatreManagement/TheatresListForAdmin.vue";
export default {
  name: "AdminHome",
  data() {
    return {};
  },
  components: {
    Navbar,
    TheatresListForAdmin,
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
.admin-home-page {
  display: block;
}
</style>
