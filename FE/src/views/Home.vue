<template>
  <div class="home-container">
    <h1>Your Mental Assistant</h1>
    <img src="@/assets/image.png" alt="Mental Assistant Logo" class="logo" />
    <button @click="startChat" class="start-button">Start</button>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    startChat() {
      this.$router.push('/chat');
    }
  }
};
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
  background-color: #ffffff; /* Match the background color */
}

h1 {
  color: #1DB981; /* Use a color that matches the text in the image */
  font-size: 24px;
  margin-bottom: 20px;
}

.logo {
  width: 300px;
  height: 300px;
  margin-bottom: 20px;
}

.start-button {
  padding: 10px 20px;
  font-size: 16px;
  font-family: 'Inter', sans-serif;
  background-color: #1DB981;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.start-button:hover {
  background-color: #1DB899;
}
</style>