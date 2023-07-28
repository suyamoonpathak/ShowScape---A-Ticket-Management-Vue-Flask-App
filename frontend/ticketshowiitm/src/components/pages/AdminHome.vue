<template>
  <div class="admin-home-page">
  <Navbar :userRole="'admin'" class="nav"/>
  <h1>Hi! Welcome to your dashboard</h1>
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
    Navbar,TheatresListForAdmin
  },
};
</script>
<style>
body{
  background-color: #001232;
}
.admin-home-page{
  display: block;
}
</style>
