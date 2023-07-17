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
  display: inline-block;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  border: 0px;
}

.primary {
  color: #ffffff;
  background-color: #eb6a33;
}

.secondary {
  color: #eb6a33;
  background-color: #ffffff;
  border: 2px solid #eb6a33;
}

button:hover {
  background-color: #ff8433;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>
