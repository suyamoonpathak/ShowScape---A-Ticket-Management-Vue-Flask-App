<template>
  <div class="signup-page">
  <div class="box">
    <CustomHeading1>Sign Up</CustomHeading1>
    <CustomTextInput
      label="Name"
      type="text"
      placeholder="Enter your name"
      :value="name"
      @update:value="name = $event"
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
      name: "",
      email: "",
      password: "",
    };
  },
  methods: {
    submit() {
      // Handle primary button click
      console.log(this.name, this.email, this.password);
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
