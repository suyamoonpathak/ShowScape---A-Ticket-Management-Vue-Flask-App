<template>
  <div class="custom-checkbox">
    <label>
      <input type="checkbox" :checked="value" @change="handleChange" />
      <span class="checkmark"></span>
      <span class="checkbox-label">
        <slot></slot>
      </span>
    </label>
  </div>
</template>

<script>
export default {
  name: "CustomCheckbox",
  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handleChange(event) {
      const isChecked = event.target.checked;
      this.$emit("input", isChecked);
    },
  },
};
</script>

<style>
/* Style the custom checkbox */
.custom-checkbox {
  display: flex;
  align-content: center;
  position: relative;
  padding-left: 5px;
  cursor: pointer;
  margin-left: 10%;
  color: rgba(255, 255, 255, 0.7);
}

/* Hide the default checkbox */
.custom-checkbox input {
  position: relative;
  opacity: 0;
  cursor: pointer;
}

/* Create a custom checkbox design */
.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 17px;
  width: 17px;
  margin-top: 2px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 50%;
}

/* When the checkbox is checked, add a blue background */
.custom-checkbox input:checked ~ .checkmark {
  background-color: #ff5252;
}

/* Create the checkmark/indicator (hidden when not checked) */
.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the checkmark when checked */
.custom-checkbox input:checked ~ .checkmark:after {
  display: block;
}

/* Style the checkmark/indicator */
.custom-checkbox .checkmark:after {
  left: 6px;
  top: 3px;
  width: 3px;
  height: 7px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
</style>
