<template>
  <div class="input-container">
    <label class="input-label">{{ label }}</label>
    <input
      :placeholder="placeholder"
      :type="type"
      :value="value"
      class="input-field"
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
      required: true,
    },
    label: {
      type: String,
    },
    value: {
      type: [String, Number],
      required: true,
    },
    placeholder: {
      type: String,
      required: false,
    },
  },
};
</script>
<style>
.input-container {
  margin-bottom: 24px;
}

.input-label {
  color: #eb6a33;
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 8px;
}

.input-field {
  width: 50%;
  height: 30px;
  padding: 12px;
  border: 2px solid;
  border-radius: 8px;
  font-size: 16px;
  outline: none;
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
