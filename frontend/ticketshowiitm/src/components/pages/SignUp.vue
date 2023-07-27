<template>
  <div class="signup-page">
  <div class="box">
    <CustomHeading1>Sign Up</CustomHeading1>
    <CustomTextInput
      label="Username"
      type="text"
      placeholder="Enter your username"
      :value="username"
      required="true"
      @update:value="username = $event"
    />
    <CustomTextInput
      label="Email"
      type="text"
      placeholder="Enter your email"
      :value="email"
      @update:value="email = $event"
    />
    <CustomTextInput
      label="Password"
      type="password"
      placeholder="Choose a password"
      :value="password"
      @update:value="password = $event"
    />
    <CustomAppButton class="primary" @click="submit">Sign Up</CustomAppButton>
    <div>
      <CustomParagraph>Already have an account? <CustomLink to="Test">Login</CustomLink> </CustomParagraph>
    </div>
  </div>
</div>
</template>
<script>
import axios from 'axios';
import CustomTextInput from "../common/CustomTextInput.vue";
import CustomAppButton from "../common/CustomAppButton.vue";
import CustomHeading1 from "../common/CustomHeading1.vue";
import CustomParagraph from "../common/CustomParagraph.vue";
import CustomLink from "../common/CustomLink.vue";

export default {

  name: "SignUp",
  components: {
    CustomTextInput,
    CustomAppButton,
    CustomLink,
    CustomHeading1,
    CustomParagraph,
  },
  data() {
    return {
      username: "",
      email: "",
      password: "",
    };
  },
  methods: {
    submit() {
      const userData = {
        username: this.username,
        email: this.email,
        password: this.password
      };

      // Make an API call to the backend to register the user
      axios.post('http://localhost:5000/api/signup', userData)
        .then(response => {
          // Handle the response (e.g., show success message, redirect to login)
          console.log('User signup successful:', response.data);
          // Redirect to login page after successful signup
          this.$router.push('/home');
        })
        .catch(error => {
          // Handle error (e.g., show error message)
          console.error('User signup failed:', error.response.data);
          // Show error message to the user
          alert('Signup failed. Please try again.');
        });
    },
  },
};
</script>
<style scoped>

.box {
  display: block;
  text-align:center;
  width: 100%;
  height: auto;
  max-width: 540px;
  padding: 60px 45px;
  margin: auto;
  box-shadow: 0px 0px 29.4px 0.6px rgba(0, 0, 0, 0.5);
  background: #001232;
}
.signup-page{
  display:flex;
  height:100vh;
  background-image: url('../../assets/bg.jpg');
  background-size: cover;
  background-position: center;
}

</style>
