<template>
  <div class="signup-page">
    <div class="box">
      <img src="./../../assets/logo.png" class="logo">
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
        type="email"
        placeholder="Enter your email"
        :value="email"
        required="true"
        pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        @update:value="email = $event"
      />
      <CustomTextInput
        label="Password"
        type="password"
        placeholder="Choose a password"
        :value="password"
        required="true"
        pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{5,}$"
        @update:value="password = $event"
      />
      <CustomCheckbox v-model="isAdmin" @input="isAdmin = $event">
        I am an Admin
      </CustomCheckbox>
      <CustomAppButton class="primary" @click="submit">Sign Up</CustomAppButton>
      <div>
        <CustomParagraph
          >Already have an account? <CustomLink to="SignIn">Sign In</CustomLink>
        </CustomParagraph>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import CustomTextInput from "../common/CustomTextInput.vue";
import CustomAppButton from "../common/CustomAppButton.vue";
import CustomHeading1 from "../common/CustomHeading1.vue";
import CustomParagraph from "../common/CustomParagraph.vue";
import CustomLink from "../common/CustomLink.vue";
import CustomCheckbox from "../common/CustomCheckbox.vue";
import { decodeJwtToken } from "../../../utils/jwtUtils";

export default {
  name: "SignUp",
  components: {
    CustomTextInput,
    CustomAppButton,
    CustomLink,
    CustomHeading1,
    CustomParagraph,
    CustomCheckbox,
  },
  data() {
    return {
      username: "",
      email: "",
      password: "",
      isAdmin: false,
    };
  },
  methods: {
    submit() {
      if (!this.username || !this.email || !this.password) {
        alert("Enter all the fields");
      } else {
        const userData = {
          username: this.username,
          email: this.email,
          password: this.password,
          isAdmin: this.isAdmin,
        };

        // Make an API call to the backend to register the user
        axios
          .post("https://showscape-backend.onrender.com/api/signup", userData)
          .then((response) => {
            // Handle the response (e.g., show success message, redirect to login)
            localStorage.setItem("access_token", response.data.access_token);
            const accessToken = localStorage.getItem("access_token");
            const jwtPayload = decodeJwtToken(accessToken);
            const role = jwtPayload.role;

            if (role === "admin") {
              this.$router.push("/AdminHome");
            } else {
              this.$router.push("/ClientHome");
            }
          })
          .catch((error) => {
            // Handle error (e.g., show error message)
            console.error("User signup failed:", error.response.data);
            // Show error message to the user
            alert("Signup failed. Please try again.");
          });
      }
    },
  },
};
</script>
<style scoped>
.box {
  display: block;
  text-align: center;
  width: 100%;
  height: auto;
  max-width: 540px;
  padding: 60px 45px;
  margin: auto;
  box-shadow: 0px 0px 29.4px 0.6px rgba(0, 0, 0, 0.5);
  background: #001232;
}

.signup-page {
  display: flex;
  height: 100vh;
  background-image: url("../../assets/bg.jpg");
  background-size: cover;
  background-position: center;
}

.primary {
  margin: 5% auto;
}

.logo{
  width: 50%;
}

@media (max-width: 768px) {
  .logo{
  width: 70%;
}
}

</style>
