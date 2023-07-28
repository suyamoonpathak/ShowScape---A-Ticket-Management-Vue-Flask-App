<template>
  <button :class="buttonClass">
    <slot></slot>
  </button>
</template>

<script>
export default {
  props: {
    primary: {
      type: Boolean,
      default: true,
    },
    secondary: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    buttonClass() {
      return {
        "button-primary": this.primary && !this.secondary,
        "button-secondary": this.secondary,
      };
    },
  },
};
</script>

<style scoped>
/* Remove the common button styles from the global button selector */
.button-primary {
  background-image: -webkit-linear-gradient(169deg, #5560ff 17%, #aa52a1 63%, #ff4343 100%);
  color: white;
}

.button-secondary {
  background-image: linear-gradient(169deg, #fff 17%, #f5f5f5 63%, #f9f9f9 100%); /* Light gradient background */
  color: #333; /* Dark text color */
  border: 2px solid #ccc; /* Lighter border */
}



button {
  font-family: 'Lato', sans-serif;
  -webkit-transition: all ease 0.3s;
  transition: all ease 0.3s;
  border-radius: 30px;
  width: auto;
  padding: 0 50px;
  height: 50px;
  text-transform: uppercase;
  font-size: medium;
  font-weight: bold;
  border: 0;
  cursor: pointer;
}

button:hover {
  box-shadow: 0px 10px 15px 0px rgba(59, 55, 188, 0.5);
}
</style>
