<template>
  <!-- The template section defines the structure of the Chat component -->
  <div class="chat-container">
    <!-- Embeds an iframe to display the Streamlit app running at localhost:8501 -->
    <iframe src="http://localhost:8501" class="chat-iframe"></iframe>
  </div>
</template>

<script>
export default {
  name: 'Chat' // Defines the name of the component as 'Chat'
};
</script>

<style scoped>
/* Scoped styles to ensure these styles apply only to this component */
.chat-container {
  display: flex; /* Use flexbox to align items */
  justify-content: center; /* Center the iframe horizontally */
  align-items: center; /* Center the iframe vertically */
  height: 100vh; /* Full viewport height */
}

.chat-iframe {
  width: 100%; /* Full width of the container */
  height: 100%; /* Full height of the container */
  border: none; /* Remove the border of the iframe */
}
</style>