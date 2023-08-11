<template>
  <nav class="navbar">
    
    <div class="nav-wrapper">
    <!-- Logo on the left side -->
    <div class="navbar-logo">
      <img src="../../assets/logo.png" class="logo">
    </div>
    <div class="navbar-hamburger" @click="toggleMenu">
      <i class="fa-solid fa-bars fa-xl"></i>
    </div>
  </div>

    <!-- Navigation links on the right side -->
    <div class="navbar-links" :class="{ 'navbar-links-open': menuOpen }">
      <!-- Show different links based on user role -->
      <!-- For admin -->
      <div v-if="userRole === 'admin'" class="navbar-links-group">
        <a href="#" @click="logout">Logout</a>
      </div>

      <!-- For client -->
      <div v-else-if="userRole === 'client'" class="navbar-links-group">
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
  data() {
    return {
      menuOpen: false, // Track the menu open state
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('access_token'); 
      this.$router.push('SignIn');
    },
    toggleMenu() {
      this.menuOpen = !this.menuOpen; // Toggle the menu open state
    },
  },
};
</script>

<style>

/* Reset default margin and padding */

/* Navbar styles */
.navbar {
  position: relative;
  width: 100%;
  height: 80px; /* Adjust the height as needed */
  background-color: #001232;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 100;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* Add a shadow to create a clean layover effect */
  border-bottom: 1px solid white;
}

/* Logo styles */
.navbar-logo {
  position: absolute;
  width: 100%;
  display: flex;
  justify-content: center;
  top:5px;
}

.logo{
  width: 13%;
  min-width: 10%;
  height: auto;
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

.navbar-hamburger{
    display: none;
  }

@media (max-width: 768px) {
  .navbar {
    display: flex;
    position: relative;
    width: 100%;
    padding: 0;
    border: none;
    background: transparent;
  }

  .nav-wrapper{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }

  .navbar-hamburger{
    display: inline-block;
    color:white;
    margin-top: 15px;
    padding-right: 20px;
  }

  .navbar-logo {
    position: relative;
    margin: 10px 0px; /* Add space above the logo */
    width: auto;
    padding-left: 20px;
  }

  .logo{
    height: 60px;
    width: auto;
  }

  .navbar-links {
    position: relative;
    flex-direction: column; /* Stack links vertically on small screens */
    align-items: flex-start; /* Align links to the left */
    position: absolute;
    top: 80px; /* Adjust the top position as needed */
    right: 0;
    background-color: #001232; /* Use a background color for the menu */
    width: 100%;
    max-height: 0; /* Hide menu by default */
    overflow: hidden;
    transition: max-height 0.3s ease-out; /* Add smooth transition effect */
    margin-right: 0;
  }

  .navbar-links-open {
    max-height: 200px;
    width: 100%
  }

  .navbar-links-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%; /* Make the link group full width */
    padding: 10px 20px; /* Add padding for links */
    border-bottom: 1px solid white; /* Add a separator between link groups */
  }

  .navbar-links a {
    margin: 10px 0; /* Add spacing between links */
  }
}

</style>
