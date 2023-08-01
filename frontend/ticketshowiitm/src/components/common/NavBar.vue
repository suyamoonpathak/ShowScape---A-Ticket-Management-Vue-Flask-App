<template>
  <nav class="navbar">
    <!-- Logo on the left side -->
    <div class="navbar-logo">
      <img src="../../assets/logo.png" class="logo">
    </div>

    <!-- Navigation links on the right side -->
    <div class="navbar-links">
      <!-- Show different links based on user role -->
      <!-- For admin -->
      <div v-if="userRole === 'admin'">
        <router-link to="/summary">Summary</router-link>
        <a href="#" @click="logout">Logout</a>
      </div>

      <!-- For client -->
      <div v-else-if="userRole === 'client'">
        <router-link to="/my-bookings">My Bookings</router-link>
        <a href="#" @click="logout">Logout</a>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  props: {
    userRole: {
      type: String,
      required: true,
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token'); 
      this.$router.push('SignIn');
    },
  },
};
</script>

<style>

/* Reset default margin and padding */

/* Navbar styles */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 80px; /* Adjust the height as needed */
  background-color: #001232;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  z-index: 100;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Add a shadow to create a clean layover effect */
  border-bottom: 1px solid white;
}

/* Logo styles */
.navbar-logo {
  width: 100%;
  display: flex;
  position: absolute;
  justify-content: center;
}

.logo{
  width: 13%;
  min-width: 10%;
  height: auto;
}
@media (max-width: 768px) {
  .logo {
    min-width: 150px; /* Set a minimum width for the logo */
    max-width: 40%; /* Adjust the maximum width as needed */
  }
}

/* Navigation links styles */
.navbar-links {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-right: 5%;
  width: 100%;
  z-index: 5;
}

.navbar-links a {
  color: white;
  font-size: 20px;
  text-decoration: none;
  margin-left: 20px; /* Adjust the space between links as needed */
}


/* Optional: Add hover and active styles for the links */
.navbar-links a:hover {
  color: #ff5252; /* Change the color on hover */

}

/* Optional: Active link style (when the link is active/selected) */
.navbar-links a.active {
  font-weight: bold;
}

/* Optional: Media query to adjust styles for smaller screens */
@media (max-width: 768px) {
  /* Add styles for smaller screens here */
}

/* Add any additional styles as needed */

</style>
