<template>
  <!-- <h1>This is client home page! Welcome client!</h1> -->
  <Navbar :userRole="'client'" />
</template>
<script>
import Navbar from "../common/NavBar.vue";
export default {
  name: "ClientHome",
  data() {
    return {};
  },
  components: {
    Navbar,
  },
};
</script>
