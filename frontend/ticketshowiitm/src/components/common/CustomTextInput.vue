<template>
  <div class="input-container">
    <label :for="inputId" class="input-label">{{ label }}</label
    ><br />
    <input
      :placeholder="placeholder"
      :type="type"
      :value="value"
      class="input-field"
      :id="inputId"
      :class="{ error: hasError }"
      @input="$emit('update:value', $event.target.value)"
    />
    <div v-if="hasError" class="error-message">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
    },
    label: {
      type: String,
    },
    value: {
      type: [String, Number],
    },
    placeholder: {
      type: String,
      required: false,
    },
    inputId: {
      type: String,
    },
  },
};
</script>
<style>
.input-container {
  width: 80%;
  margin: 0 auto;
  text-align: left;
  position: relative;
}

.input-label {
  margin-bottom: 10px;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.7);
  text-align: left;
}

.input-field {
  height: 45px;
  border-radius: 0;
  border: none;
  border-bottom: 1px solid #23334f;
  background: transparent;
  color: #dbe2fb;
  width: 100%;
  font-family: inherit;
  font-size: 100%;
  line-height: 1.15;
  margin-bottom: 15px;
  padding: 0px;
  outline: none;
  box-sizing: border-box;
}

.input-field:focus {
  box-sizing: border-box;
}

.input-field.error {
  border-color: #ff5252;
}

.error-message {
  color: #ff5252;
  font-size: 14px;
  margin-top: 4px;
}
</style>
