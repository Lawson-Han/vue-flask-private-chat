<template>
  <div class="chat__body" id="chat__body">
    <chat-message
      v-for="(msg, index) in msgs"
      :key="index"
      :msg="msg"
      :prev="[index == 0 ? null : msgs[index - 1]]"
      :username="username"
    >
    </chat-message>
  </div>
</template>

<script>
import ChatMessage from './ChatMessage'

export default {
  components: {
    ChatMessage
  },
  props: ['msgs', 'username']
}
</script>

<style>
.chat__body {
  padding: 2rem;
  overflow: scroll;
  scroll-behavior: smooth;
}

.chat__body::-webkit-scrollbar {
  display: none;
}
</style>
