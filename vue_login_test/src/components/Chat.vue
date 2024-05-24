<template>
  <div class='chat'>
    <el-header>
        <el-menu :disabled="this.muted" :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="/home">Home</el-menu-item>
          <el-menu-item index="/forum">Forum</el-menu-item>
          <el-menu-item index="3">Chat</el-menu-item>
          <el-menu-item :disabled="username!=='admin'" index="/admin">Admin</el-menu-item>
          <el-menu-item style="float: right">Logged in as: {{ username }}</el-menu-item>
          <el-menu-item v-show="this.muted" style="float: right; color:red">You're currently muted</el-menu-item>
        </el-menu>
        <div class="line"></div>
    </el-header>
    <el-container style="height: 500px; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <el-menu :default-openeds="['2', '3']">
          <el-menu-item :disabled="this.muted" index="1" @click="add_friend()"><i class="el-icon-user"></i>Add friend</el-menu-item>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-chat-line-round"></i>Friends</template>
              <el-menu-item v-for="(item,index) in friends" :key="index" @click="openChat(item)">{{item}}</el-menu-item>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title"><i class="el-icon-setting"></i>Settings</template>
              <el-menu-item index="3-1" @click="logout()"><i class="el-icon-back"></i>Log out</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header class="chat__header">
          <span class='chat__header__greetings'>
              To {{ this.friendName }}
            </span>
        </el-header>
        <el-main id="main">
          <chat-list :msgs='msgData' :username=this.userName></chat-list>
        </el-main>
        <chat-form v-if="this.friendName !== ''" @submitMessage='sendMessage'></chat-form>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import ChatList from './ChatList'
import ChatForm from './ChatForm'
import axios from 'axios'
import SocketIO from 'socket.io-client'
import JSEncrypt from 'jsencrypt'
import AES from '@/AES.js'
export default {
  data () {
    return {
      activeIndex: '3',
      userName: sessionStorage.getItem('username'),
      friendName: '',
      friends: [],
      msgData: [],
      friend_pk: '',
      sessionKey: '',
      socket: SocketIO('http://127.0.0.1:5000'),
      username: sessionStorage.getItem('username'),
      muted: localStorage.getItem(this.username + '_muted')
    }
  },
  components: {
    ChatList,
    ChatForm
  },
  computed: {

  },
  created () {
    if (localStorage.getItem(this.username + '_muted') === '0') {
      this.muted = false
      // this.$dispatchEventStorage(this.username + '_muted', 'haha')
    } else {
      this.muted = true
    }
    axios({
      method: 'post',
      url: 'http://localhost:5000/api/get_friend',
      data: {
        username: sessionStorage.getItem('username')
      }
    }).then((res) => {
      // [{friend: user2}, {friend: user3}]
      console.log('retrieving friend list...')
      if (res.data.friend !== '') {
        this.friends = res.data.friend.split(';')
      }
    })
  },
  mounted () {
    // const that = this
    // 根据自己需要来监听对应的key
    const key = this.username + '_muted'
    const that = this
    window.addEventListener('storage', function (e) {
      // e.key : 是值发生变化的key
      // 例如 e.key==="token";
      // e.newValue : 是可以对应的新值
      if (e.key && e.key === (key) && e.newValue) {
        if (e.newValue === '0') {
          that.muted = false
        } else {
          that.muted = true
        }
      }
    })
    this.socket.on('RESPONSE', (data) => {
      var plaintext = ''
      // 消息的验证三步曲 rsa aes signature
      if (data.from_user !== this.userName) {
        // 用自己私钥解密出session key
        const rsaDecrypt = this.rsaPrivateData(data.message[0])
        console.log('RSA decryption get the session key: ' + rsaDecrypt)
        // 用session key进行aes解密得到明文
        const aesDecrypt = AES.decrypt(data.message[1], rsaDecrypt)
        console.log('AES decryption using session key to get the plaintext: ' + aesDecrypt)
        plaintext = aesDecrypt
        // 用朋友公钥配合明文密文验签
        const verifySignature = this.$testSignature(plaintext, data.message[2], this.friend_pk)
        console.log('Verify signature using friend public key: ' + verifySignature)
      } else {
        plaintext = AES.decrypt(data.message[1], this.sessionKey)
      }
      console.log('plain text: ' + plaintext)
      this.msgData.push({
        from: {
          name: data.from_user
        },
        msg: plaintext
      })
    })
    setTimeout(() => {
      const element = document.getElementById('main')
      element.scrollTop = element.scrollHeight
    }, 0)
  },
  methods: {
    handleSelect (key, keyPath) {
      if (key !== '3') {
        this.$router.push(key)
      }
    },
    logout () {
      sessionStorage.removeItem('username')
      sessionStorage.removeItem('privateKey')
      this.$router.push('/login')
    },
    add_friend () {
      this.$prompt('Please input your friend\'s username', 'Add new friend', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel'
      }).then(({ value }) => {
        if (value === this.userName || this.friends.indexOf(value) !== -1) {
          this.$message({
            type: 'error',
            message: 'Friend already exists'
          })
          return
        }
        axios({
          method: 'post',
          url: 'http://localhost:5000/api/add_friend',
          data: {
            userName: this.userName,
            friendName: value
          }
        }).then((res) => {
          switch (res.data.status) {
            case true:
              this.$message({
                type: 'success',
                message: value + ' has been added'
              })
              this.friends.push(value)
              break
            case false:
              this.$message({
                type: 'error',
                message: 'There\'s no user called ' + value
              })
              break
          }
        })
      })
    },
    openChat (item) {
      this.msgData = []
      this.friendName = item
      axios({
        method: 'post',
        url: 'http://localhost:5000/api/get_chat',
        data: {
          username: this.userName,
          friendname: this.friendName
        }
      }).then((res) => {
        this.friend_pk = res.data.publicKey
        console.log('Retrieved friend public key : ' + this.friend_pk)
        for (var i = 0; i < res.data.history.length; i++) {
          this.msgData.push({
            from: {
              name: res.data.history[i].from_username
            },
            msg: AES.decrypt(res.data.history[i].message, this.systemKey)
          })
        }
      })

      // AES generates a 16 digits random key and encrypt the message
      if (this.sessionKey === '') {
        this.sessionKey = AES.generatekey(16)
      }
      console.log('Randomly generates a session key ' + this.sessionKey)
    },
    sendMessage (msg) {
      // 使用朋友公钥加密session key  -  朋友使用自己私钥解密出session key
      console.log('Starting RSA public key encryption on session key...')
      const rsaEncrypt = this.rsaPublicData(this.sessionKey)
      console.log('RSA encryption: ' + rsaEncrypt)
      // 利用原session key 加密明文  -  朋友使用解密出的私钥解密原文
      const aesEncrypts = AES.encrypt(msg, this.sessionKey)
      console.log('AES encrypt the message using session key: ' + aesEncrypts)
      // 使用自己私钥签名  -  朋友使用我公钥验签
      const signature = this.$signature(msg, sessionStorage.getItem('privateKey'))
      console.log('Sign messsage using private key: ' + signature)
      // Enc(key), Enc(msg), Signature
      const encryptedMsg = []
      encryptedMsg[0] = rsaEncrypt
      encryptedMsg[1] = aesEncrypts
      encryptedMsg[2] = signature
      console.log('Sending encrypted message to socket server...')
      this.socket.emit('message', {
        user: this.userName,
        to: this.friendName,
        msg: encryptedMsg
      })
      console.log('Insert encrypted data to database...')

      axios({
        method: 'post',
        url: 'http://localhost:5000/api/add_chat',
        data: {
          username: this.userName,
          friendname: this.friendName,
          message: AES.encrypt(msg, this.systemKey)
        }
      })
      setTimeout(() => {
        const element = document.getElementById('main')
        element.scrollTop = element.scrollHeight
      }, 0)
    },
    rsaPublicData (data) {
      const jsencrypt = new JSEncrypt()
      console.log('friend public key is: ' + this.friend_pk)
      jsencrypt.setPublicKey(this.friend_pk)
      // 如果是对象/数组的话，需要先JSON.stringify转换成字符串
      const result = jsencrypt.encrypt(data)
      return result
    },
    /* JSEncrypt解密 */
    rsaPrivateData (data) {
      const jsencrypt = new JSEncrypt()
      jsencrypt.setPrivateKey(sessionStorage.getItem('privateKey'))
      // 如果是对象/数组的话，需要先JSON.stringify转换成字符串
      const result = jsencrypt.decrypt(data)
      return result
    }
  }
}
</script>

<style scoped>
.chat {
  display: flex;
  position: relative;
  flex-direction: column;
  justify-content: space-between;
  max-width: 1000px;
  height: 800px;
  background-color: #ffffff;
  margin: 5px auto 0rem;
  border-radius: 1.5rem;
  box-shadow: 0px 1px 20px #9c9cc855;
}

.chat__header {
  background: #ffffff;
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.05);
  border-radius: 24px 24px 0px 0px;
  padding: 1.8rem;
  font-size: 16px;
  font-weight: 700;
}

.chat__header__greetings {
  color: #292929;
  font-size: 20px;
}
</style>
