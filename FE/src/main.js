import { createApp } from 'vue'; // Import the createApp function from the Vue library
import App from './App.vue'; // Import the root App component
import router from './router'; // Import the router configuration

// Create and mount the Vue application
createApp(App)
  .use(router) // Use the router instance in the application
  .mount('#app'); // Mount the application to the HTML element with the ID 'app'