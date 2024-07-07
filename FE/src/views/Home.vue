<template>
  <!-- The template section defines the structure of the Home component -->
  <div class="home-container">
    <!-- Main heading for the home page -->
    <h1>Your Mental Assistant</h1>
    <!-- Logo image for the mental assistant -->
    <img src="@/assets/image.png" alt="Mental Assistant Logo" class="logo" />
    <!-- Button to start the chat, triggers the startChat method on click -->
    <button @click="startChat" class="start-button">Start</button>
  </div>
</template>

<script>
export default {
  name: 'Home', // Defines the name of the component as 'Home'
  methods: {
    // Method to navigate to the chat page
    startChat() {
      this.$router.push('/chat'); // Uses Vue Router to navigate to the chat page
    }
  }
};
</script>

<style scoped>
/* Scoped styles to ensure these styles apply only to this component */
.home-container {
  display: flex; /* Use flexbox for layout */
  flex-direction: column; /* Arrange children in a column */
  align-items: center; /* Center children horizontally */
  justify-content: center; /* Center children vertically */
  height: 100vh; /* Full viewport height */
  text-align: center; /* Center text horizontally */
  background-color: #ffffff; /* Match the background color */
}

h1 {
  color: #1DB981; /* Use a color that matches the text in the image */
  font-size: 24px; /* Set font size */
  margin-bottom: 20px; /* Space below the heading */
}

.logo {
  width: 300px; /* Set width of the logo image */
  height: 300px; /* Set height of the logo image */
  margin-bottom: 20px; /* Space below the logo image */
}

.start-button {
  padding: 10px 20px; /* Add padding around the button text */
  font-size: 16px; /* Set font size */
  font-family: 'Inter', sans-serif; /* Use the Inter font */
  background-color: #1DB981; /* Set background color */
  color: white; /* Set text color */
  border: none; /* Remove default border */
  border-radius: 5px; /* Round the button corners */
  cursor: pointer; /* Change cursor to pointer on hover */
  transition: background-color 0.3s; /* Smooth transition for background color change */
}

.start-button:hover {
  background-color: #1DB899; /* Change background color on hover */
}
</style>