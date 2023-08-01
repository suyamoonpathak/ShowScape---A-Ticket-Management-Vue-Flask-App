<template>
  <div class="client-home-page">
    <Navbar :userRole="'client'" />
    <div class="all-shows-list">
      <AllShows />
    </div>
  </div>
</template>
<script>
import Navbar from "../common/NavBar.vue";
import AllShows from "./ShowManagement/AllShows.vue";

export default {
  name: "ClientHome",
  data() {
    return {};
  },
  components: {
    Navbar,
    AllShows,
  },
};
</script>

<style>
h1 {
  color: white;
}
.client-home-page {
  display: block;
}

.all-shows-list {
  margin-top: 2%;
}
</style>
