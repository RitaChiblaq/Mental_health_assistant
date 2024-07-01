<template>
  <div class="chat-container">
    <iframe src="http://localhost:8501" class="chat-iframe"></iframe>
  </div>
</template>

<script>
export default {
  name: 'Chat'
};
</script>

<style scoped>
.chat-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.chat-iframe {
  width: 100%;
  height: 100%;
  border: none;
}
</style>