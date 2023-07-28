import { createRouter, createWebHistory } from 'vue-router'
import TestComponent from '../components/common/TestComponent'
import SignUp from '../components/pages/SignUp'
import SignIn from '../components/pages/SignIn'
import HomePage from '../components/pages/HomePage'
import ClientHome from '../components/pages/ClientHome'
import AdminHome from '../components/pages/AdminHome'

import TheatresListForAdmin from '../components/pages/TheatreManagement/TheatresListForAdmin'
import TheatreDetails from '../components/pages/TheatreManagement/TheatreDetails'
import EditTheatre from '../components/pages/TheatreManagement/EditTheatre'
import CreateTheatre from '../components/pages/TheatreManagement/CreateTheatre'

import CreateShow from '../components/pages/ShowManagement/CreateShow'
import ShowDetails from '../components/pages/ShowManagement/ShowDetails'
import ShowListFromTheatre from '../components/pages/ShowManagement/ShowListFromTheatre'

const routes = [
  {
    path: '/test',
    name:'Test',
    component: TestComponent
  },
  {
    path: '/signup',
    component: SignUp
  },
  {
    path: '/',
    component: SignUp
  },
  {
    path: '/home',
    component: HomePage
  },
  {
    path: '/signin',
    component: SignIn
  },
  {
    path: '/clienthome',
    component: ClientHome,
    meta: { requiresAuth: true, requiredRole: 'client' },
  },
  {
    path: '/adminhome',
    component: AdminHome,
    meta: { requiresAuth: true, requiredRole: 'admin' },
  },
  {
    path: '/theatres-list-for-admin/',
    name: "TheatresListForAdmin",
    component: TheatresListForAdmin,
    meta: { requiresAuth: true, requiredRole: 'admin' },
  },
  {
    path: '/theatres/:id',
    name: "TheatreDetails",
    component: TheatreDetails,
    meta: { requiresAuth: true, requiredRole: 'admin' },
  },
  {
    path: '/theatres/:id/edit',
    name: "EditTheatre",
    component: EditTheatre,
    meta: { requiresAuth: true, requiredRole: 'admin' },
  },
  {
    path: '/theatres/create/',
    name: "CreateTheatre",
    component: CreateTheatre,
    meta: { requiresAuth: true, requiredRole: 'admin' },
  },
  {
    path: '/show-list-from-theatre/:id',
    name: 'ShowListFromTheatre',
    component: ShowListFromTheatre
  },
  {
    path: '/show/:id',
    name: 'ShowDetails',
    component: ShowDetails
  },
  {
    path: '/create-show/:id',
    name: 'CreateShow',
    component: CreateShow,
    meta: { requiresAuth: true, isAdmin: true } // Add meta data for authentication and role check
  },
]
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

function decodeJwtToken(token) {
  const tokenParts = token.split('.');
  const base64Payload = tokenParts[1];
  const decodedPayload = atob(base64Payload);
  return JSON.parse(decodedPayload);
}

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token'); // Check if the access_token is present in Local Storage
  const requiresAuth = to.matched.some((route) => route.meta.requiresAuth);
  const requiredRole = to.meta.requiredRole; // Get the required role for the route

  if (requiresAuth && !isLoggedIn) {
    // If the route requires authentication and the user is not logged in, redirect to the login page
    next({ name: 'Login' });
  } else if (requiresAuth && requiredRole) {
    // If the route requires authentication and a specific role is required
    const accessToken = localStorage.getItem('access_token');
    const jwtPayload = decodeJwtToken(accessToken);
    const userRole = jwtPayload.role;

    if (userRole !== requiredRole) {
      // If the user's role does not match the required role, redirect to an error page or a page with an "Unauthorized" message
      next({ name: 'Test' }); // Replace 'Unauthorized' with the route name for the unauthorized page or message
    } else {
      next(); // Proceed with the navigation
    }
  } else {
    next(); // Proceed with the navigation for other cases (e.g., public routes)
  }
});




export default router