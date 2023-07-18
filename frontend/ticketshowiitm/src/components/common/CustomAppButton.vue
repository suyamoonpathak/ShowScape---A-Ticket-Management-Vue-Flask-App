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
        "button-primary": this.primary,
        "button-secondary": this.secondary,
      };
    },
  },
};
</script>
<style scoped>
button {
  background-image: -webkit-linear-gradient(169deg, #5560ff 17%, #aa52a1 63%, #ff4343 100%);
  font-family: 'Lato', sans-serif;
  -webkit-transition: all ease 0.3s;
  transition: all ease 0.3s;
  border-radius: 30px;
  width: auto;
  padding: 0 50px;
  height: 50px;
  text-transform: uppercase;
  margin: 10px auto;
  color:white;
  font-size: medium;
  font-weight: bold;
  border:0px;
  cursor: pointer;
}


button:hover {
  -webkit-box-shadow: 0px 10px 15px 0px rgba(59, 55, 188, 0.5);
  box-shadow: 0px 10px 15px 0px rgba(59, 55, 188, 0.5);
}
</style>


