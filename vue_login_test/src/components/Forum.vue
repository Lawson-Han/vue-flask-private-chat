<template>
  <div class='chat'>
    <el-header>
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="/home">Home</el-menu-item>
          <el-menu-item index="2">Forum</el-menu-item>
          <el-menu-item index="/chat">Chat</el-menu-item>
          <el-menu-item :disabled="username!=='admin'" index="/admin">Admin</el-menu-item>
          <el-menu-item style="float: right">Logged in as: {{ username }}</el-menu-item>
          <el-menu-item v-show="this.muted" style="float: right; color:red">You're currently muted</el-menu-item>
        </el-menu>
        <div> {{ username }}</div>
        <div class="line"></div>
    </el-header>
    <el-container style="height: 500px; border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
            <el-menu :default-openeds="['2']">
              <el-menu-item :disabled="this.muted" index="1" @click="post()"><i class="el-icon-question"></i>Post question</el-menu-item>
              <el-submenu index="2" v-model="question">
                <template slot="title"><i class="el-icon-help"></i>Questions</template>
                  <el-menu-item v-for="(item) in question" @click="openContent(item)"
                      :key="item.name"
                      :label="item.title"
                      :name="item.name">
                    {{ item.title }}
                  </el-menu-item>
              </el-submenu>
            </el-menu>
        </el-aside>
        <el-container>
          <el-main id="main" v-model="question">
            <Post :item="postItem" v-if="currentPage==='Question'"></Post>
            <div v-show="currentPage==='Post'">
              <el-form ref="formRef" :model="form" label-width="80px" :label-position='labelPosition'>
                <h1>Post your question</h1>
                <el-form-item label="Title" prop="title">
                  <el-input v-model="form.title"
                  maxlength="10"
                  show-word-limit>
                  </el-input>
                </el-form-item>
                <el-form-item label="Description">
                  <el-input type="textarea" :rows="4" v-model="form.desc" prop="description"
                  placeholder="What's in your mind..."
                  maxlength="100"
                  show-word-limit></el-input>
                </el-form-item>
                <el-form-item label="Private" prop="private">
                  <el-switch v-model="form.private"></el-switch>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="postQuestion">Post now</el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-main>
        </el-container>
    </el-container>
  </div>
</template>
<script>
import Post from './Post'
import axios from 'axios'
import AES from '@/AES'
export default {
  data () {
    return {
      labelPosition: 'left',
      activeIndex: '2',
      postItem: '',
      currentPage: '',
      question: [],
      muted: '',
      username: sessionStorage.getItem('username'),
      form: {
        title: '',
        private: false,
        user: sessionStorage.getItem('username'),
        desc: ''
      },
      encrypted: {
        title: '',
        private: false,
        user: sessionStorage.getItem('username'),
        desc: ''
      }
    }
  },
  components: { Post },
  computed: {
    // 计算属性 进行加密
    encryptMessage: function () {
      // `this` 指向 vm 实例
      const that = this
      if (this.form.private) {
        that.encrypted.desc = AES.encrypt(this.form.desc, this.systemKey)
        that.encrypted.title = AES.encrypt(this.form.title, this.systemKey)
      } else {
        that.encrypted.desc = this.form.desc
        that.encrypted.title = this.form.title
      }
      return that.encrypted
    }
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
      url: 'http://localhost:5000/api/get_question',
      data: {
      }
    }).then((res) => {
      for (let i = 0; i < res.data.length; i++) {
        if (res.data[i].if_private === 1) {
          res.data[i].description = AES.decrypt(res.data[i].description, this.systemKey)
          res.data[i].title = AES.decrypt(res.data[i].title, this.systemKey)
          if (this.username !== 'admin' && this.username !== res.data[i].provider) {
            continue
          }
        }
        this.question.push(res.data[i])
      }
    })
  },
  methods: {
    handleSelect (key, keyPath) {
      if (key !== '2') {
        this.$router.push(key)
      }
    },
    openContent (item) {
      this.postItem = item
      this.currentPage = 'Question'
    },
    post () {
      this.currentPage = 'Post'
    },
    postQuestion () {
      axios({
        method: 'post',
        url: 'http://localhost:5000/api/add_question',
        data: {
          title: this.encryptMessage.title,
          description: this.encryptMessage.desc,
          private: this.form.private,
          provider: sessionStorage.getItem('username')
        }
      }).then((res) => {
        const currentQuestion = {
          qid: res.data.status,
          title: this.form.title,
          description: this.form.desc,
          private: this.form.private,
          provider: sessionStorage.getItem('username')
        }
        this.question.push(currentQuestion)
        this.$message({
          type: 'success',
          message: 'Post question successfully'
        })
        this.$refs.formRef.resetFields()
        this.form.desc = ''
      })
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
</style>
