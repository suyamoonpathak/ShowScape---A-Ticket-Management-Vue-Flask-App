<template>
  <div class="signin-page">
    <div class="box">
      <CustomHeading1>Sign In</CustomHeading1>
      <CustomTextInput
        label="Username"
        type="text"
        placeholder="Enter your username"
        :value="username"
        required="true"
        @update:value="username = $event"
      />
      <CustomTextInput
        label="Password"
        type="password"
        placeholder="Choose a password"
        :value="password"
        required="true"
        @update:value="password = $event"
      />
      <div v-if="hasError" class="error-message">{{ errorMessage }}</div>
      <CustomAppButton class="primary" @click="submit">Sign In</CustomAppButton>
      <div>
        <CustomParagraph
          >Don't have an account? <CustomLink to="SignUp">Sign Up</CustomLink>
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
import { decodeJwtToken } from "../../../utils/jwtUtils";

export default {
  name: "SignIn",
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
      password: "",
      hasError: false,
      errorMessage: "",
    };
  },
  methods: {
    submit() {
      if (!this.username || !this.password) {
        alert("Enter all the fields!");
      } else {
        const userData = {
          username: this.username,
          password: this.password,
        };

        axios
          .post("http://localhost:5000/api/signin", userData)
          .then((response) => {
            localStorage.setItem("access_token", response.data.access_token);

            const accessToken = localStorage.getItem("access_token");
            const jwtPayload = decodeJwtToken(accessToken);
            const role = jwtPayload.role;

            if (role == "admin") {
              this.$router.push("/AdminHome");
            } else {
              this.$router.push("/ClientHome");
            }
          })
          .catch((error) => {
            console.error("User signup failed:", error.response.data);
            this.hasError = true;
            this.errorMessage = "Credentials don't match. Please try again";
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

.signin-page {
  display: flex;
  height: 100vh;
  background-image: url("../../assets/bg.jpg");
  background-size: cover;
  background-position: center;
}

.primary {
  margin: 5% auto;
}

.error-message {
  margin-top: 2%;
}
</style>
