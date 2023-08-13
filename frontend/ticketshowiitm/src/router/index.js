import { createRouter, createWebHistory } from "vue-router";
import SignUp from "../components/pages/SignUp";
import SignIn from "../components/pages/SignIn";
import ClientHome from "../components/pages/ClientHome";
import AdminHome from "../components/pages/AdminHome";
import ErrorPage from "../components/pages/ErrorPage.vue";
import TheatreSummary from "../components/pages/TheatreSummary.vue"

import TheatresListForAdmin from "../components/pages/TheatreManagement/TheatresListForAdmin";
import TheatreDetails from "../components/pages/TheatreManagement/TheatreDetails";
import EditTheatre from "../components/pages/TheatreManagement/EditTheatre";
import CreateTheatre from "../components/pages/TheatreManagement/CreateTheatre";

import CreateShow from "../components/pages/ShowManagement/CreateShow";
import EditShow from "../components/pages/ShowManagement/EditShow";
import ShowDetails from "../components/pages/ShowManagement/ShowDetails";
import ShowListFromTheatre from "../components/pages/ShowManagement/ShowListFromTheatre";

import MyBookings from "@/components/pages/BookingManagement/MyBookings"
import BookingSuccess from "@/components/pages/BookingManagement/BookingSuccess";
import BookingFailed from "@/components/pages/BookingManagement/BookingFailed";

const routes = [
  {
    path: "/signup",
    component: SignUp,
  },
  {
    path: "/",
    component: SignUp,
  },
  {
    path: "/signin",
    component: SignIn,
  },
  {
    path: "/clienthome",
    component: ClientHome,
    meta: { requiresAuth: true, requiredRole: "client" },
  },
  {
    path: "/adminhome",
    component: AdminHome,
    meta: { requiresAuth: true, requiredRole: "admin" },
  },
  {
    path: "/theatres-list-for-admin/",
    name: "TheatresListForAdmin",
    component: TheatresListForAdmin,
    meta: { requiresAuth: true, requiredRole: "admin" },
  },
  {
    path: "/theatres/:id",
    name: "TheatreDetails",
    component: TheatreDetails,
    meta: { requiresAuth: true, requiredRole: "admin" },
  },
  {
    path: "/theatres/:id/edit",
    name: "EditTheatre",
    component: EditTheatre,
    meta: { requiresAuth: true, requiredRole: "admin" },
  },
  {
    path: "/theatres/create/",
    name: "CreateTheatre",
    component: CreateTheatre,
    meta: { requiresAuth: true, requiredRole: "admin" },
  },
  {
    path: "/show-list-from-theatre/:id",
    name: "ShowListFromTheatre",
    component: ShowListFromTheatre,
  },
  {
    path: "/show/:id",
    name: "ShowDetails",
    component: ShowDetails,
  },
  {
    path: "/create-show/:id",
    name: "CreateShow",
    component: CreateShow,
    meta: { requiresAuth: true, requiredRole: "admin" },
  },
  {
    path: "/edit-show/:theaterid/:showid/",
    name: "EditShow",
    component: EditShow,
    meta: { requiresAuth: true, requiredRole: "admin"},
  },
  { 
    path: "/booking-success", 
    component: BookingSuccess 
  },
  {
    path: "/booking-failed", 
    component: BookingFailed 
  },
  {
    path:"/my-bookings",
    component: MyBookings,
    meta: { requiresAuth: true, requiredRole: "client"},
  },
  {
    path:"/summary",
    component: TheatreSummary,
    meta: { requiresAuth: true, requiredRole: "admin"},
  },
  {
    path: "/:catchAll(.*)", // Use a param with a custom regexp
    component: ErrorPage,
  },

];
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

function decodeJwtToken(token) {
  const tokenParts = token.split(".");
  const base64Payload = tokenParts[1];
  const decodedPayload = atob(base64Payload);
  return JSON.parse(decodedPayload);
}

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem("access_token"); // Check if the access_token is present in Local Storage
  const requiresAuth = to.matched.some((route) => route.meta.requiresAuth);
  const requiredRole = to.meta.requiredRole; // Get the required role for the route

  if (requiresAuth && !isLoggedIn) {
    // If the route requires authentication and the user is not logged in, redirect to the login page
    next({ name: "Login" });
  } else if (requiresAuth && requiredRole) {
    // If the route requires authentication and a specific role is required
    const accessToken = localStorage.getItem("access_token");
    const jwtPayload = decodeJwtToken(accessToken);
    const userRole = jwtPayload.role;

    if (userRole !== requiredRole) {
      // If the user's role does not match the required role, redirect to an error page or a page with an "Unauthorized" message
      next({ name: "ErrorPage", params: { errorCode: 403 } }); 
    } else {
      next(); // Proceed with the navigation
    }
  } else {
    next(); // Proceed with the navigation for other cases (e.g., public routes)
  }
});

export default router;
