<template>
    <div class="chat-interface">
      <div class="chat-header">
        <div class = "chat-history"></div>
        <h2>Fit-It</h2>
        <div class="cube">

        </div>
      </div>
      <div class="chat-messages">
        <div v-for="message in messages" :key="message.id" class="message">
          <div :class="['message-text', message.sender === 'user' ? 'user-message' : 'bot-message']">
            {{ message.text }}
          </div>
        </div>
      </div>
      <div class="chat-input">
        <input
          v-model="newMessage"
          placeholder="Type your message..."
          @keyup.enter="sendMessage"
          class="input-field"
        />
        <button @click="sendMessage" class="send-button">Send</button>
      </div>
    </div>
  </template>
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ChatInterface',
    data() {
      return {
        messages: [],
        newMessage: '',
      };
    },
    methods: {
  sendMessage() {
    if (this.newMessage.trim() !== '') {
      const userMessage = {
        id: Date.now(),
        text: this.newMessage,
        sender: 'user',
      };
      this.messages.push(userMessage);

      this.sendQueryToServer(this.newMessage);
      this.newMessage = '';
    }
  },
  sendQueryToServer(query) {
  const cacheKey = this.generateCacheKey(query);
  const cachedResult = this.checkCache(cacheKey);

  if (cachedResult) {
    this.handleServerResponse(cachedResult);
  } else {
    axios.post('http://localhost:5000/search', { query, cacheKey })
      .then(response => {
        this.handleServerResponse(response.data);
        this.cacheResult(cacheKey, response.data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
},
  generateCacheKey(query) {
    // Implement a hashing function to generate a unique cache key for the query
    // For example, you can use a library like crypto-js or a simple string manipulation
    return query.replace(/\s+/g, '').toLowerCase();
  },
  checkCache(cacheKey) {
    // Check if the result for the given cacheKey exists in the cache
    // You can use a simple object as a cache or a more sophisticated caching mechanism
    const cache = {}; // Replace with your caching mechanism
    return cache[cacheKey];
  },
  cacheResult(cacheKey, result) {
    // Cache the result for the given cacheKey
    // You can use a simple object as a cache or a more sophisticated caching mechanism
    const cache = {}; // Replace with your caching mechanism
    cache[cacheKey] = result;
  },
  handleServerResponse(response) {
    const botMessage = {
      id: Date.now() + 1,
      text: response.result,
      sender: 'bot',
    };
    this.messages.push(botMessage);
  },
},
    };
  </script>
  <style scoped>
  .chat-interface {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #4001011F;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s ease;
  }
  .chat-interface:hover {
  background-color: #5001011F;
}
  .chat-header {
    background-color: #06383E;
    border-radius: 10px;
    color: #fff;
    padding: 5px;
    text-align: center;
  }

  .cube {
  width: 795px;
  height: 250px;
  background-color: #C6D6D8;
  border-radius: 10px;
  
}
  .chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 10px;
  }
  
  .message {
    margin-bottom: 10px;
  }
  
  .message-text {
    padding: 8px 12px;
    border-radius: 16px;
    max-width: 70%;
  }
  
  .user-message {
    background-color: #006BB8;
    color: #fff;
    align-self: flex-end;
  }
  
  .bot-message {
    background-color: #ddd;
    color: #333;
    align-self: flex-start;
  }
  
  .chat-input {
    display: flex;
    padding: 10px;
    background-color: #f9f9f9;
    border-top: 1px solid #ddd;
  }
  
  .input-field {
    flex-grow: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    transition: border-color 0.3s ease;
  }
  .input-field:focus {
  border-color: #00E1FF;
}

.send-button {
  background-color: #00E1FF;
  color: #fff;
  border: none;
  padding: 0.5em 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
  
}

.send-button:hover {
  background-color: #00B2CC;

}

.send-button:disabled {
  background-color: #7FD8FF;
  cursor: not-allowed;
}
.chat-history {
  flex-grow: 1;
  overflow-y: auto;
}
  </style>