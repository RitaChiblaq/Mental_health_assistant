import { createRouter, createWebHistory } from 'vue-router'; // Importing necessary functions from 'vue-router' for creating a router and history
import Home from '../views/Home.vue'; // Importing the Home component
import Chat from '../views/Chat.vue'; // Importing the Chat component

// Defining routes for the application
const routes = [
  {
    path: '/', // Path for the Home component
    name: 'Home', // Name of the route
    component: Home // Component to render when this route is accessed
  },
  {
    path: '/chat', // Path for the Chat component
    name: 'Chat', // Name of the route
    component: Chat // Component to render when this route is accessed
  }
];

// Creating a router instance with history mode
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // Using HTML5 history mode for navigation
  routes // Assigning the defined routes to the router
});

export default router; // Exporting the router instance for use in the main application