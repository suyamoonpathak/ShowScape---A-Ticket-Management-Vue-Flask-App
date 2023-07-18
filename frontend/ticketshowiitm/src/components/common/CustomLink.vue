<template>
  <a :href="to" class="custom-link">
    <slot></slot>
  </a>
</template>

<script>
export default {
  props: {
    to: {
      type: String,
    }
  },
};
</script>

<style scoped>
.custom-link {
  color: #ff5252;
  text-decoration: none;
  /* Additional styles for the link */
}
</style>
