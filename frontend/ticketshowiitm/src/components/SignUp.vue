<template>
  <h1>Sign Up</h1>
  <input-field
    type="text"
    placeholder="Name"
    :value="name"
    @update:value="name = $event"
  />
  <input-field
    type="number"
    placeholder="Age"
    :value="age"
    @update:value="age = $event"
  />
  <input-field
    type="text"
    placeholder="Email"
    :value="email"
    @update:value="email = $event"
  />
  <input-field
    type="password"
    placeholder="Password"
    :value="password"
    @update:value="password = $event"
  />
  <AppButton class="primary" @click="submit">Submit</AppButton>
</template>
<script>
import InputField from "./InputField.vue";
import AppButton from "./AppButton.vue";

export default {
  name: "SignUp",
  components: {
    InputField,
    AppButton,
  },
  data() {
    return {
      name: "",
      age: null,
      email: "",
      password: "",
    };
  },
  methods: {
    submit() {
      // Handle primary button click
      console.log(this.name, this.age, this.email, this.password);
    },
  },
};
</script>
