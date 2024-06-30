<template>
  <div>
    <h1>Chat</h1>
    <div v-for="message in messages" :key="message.id" :class="message.sender">
      <p>{{ message.text }}</p>
    </div>
    <input v-model="input" @keyup.enter="sendMessage" placeholder="Type a message" />
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Chat',
  data() {
    return {
      messages: [],
      input: '',
    }
  },
  methods: {
    async sendMessage() {
      const user_id = 'your_user_id' // Replace with actual user ID
      const response = await axios.post('http://localhost:5000/add_message', {
        session_id: 'your_session_id', // Replace with actual session ID
        sender: 'user',
        message_text: this.input,
      })

      const message = {
        id: response.data.message_id,
        text: this.input,
        sender: 'user',
      }

      this.messages.push(message)
      this.input = ''

      // Call Chainlit API to get the response
      const botResponse = await axios.post('http://localhost:8000/api/message', {
        user_id: user_id,
        text: this.input,
      })

      const botMessage = {
        id: botResponse.data.message_id,
        text: botResponse.data.text,
        sender: 'bot',
      }

      this.messages.push(botMessage)
    }
  }
}
</script>

<style>
.user {
  text-align: right;
}
.bot {
  text-align: left;
}
</style>