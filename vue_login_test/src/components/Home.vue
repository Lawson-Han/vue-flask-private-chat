<template>
  <div class='chat'>
    <el-header>
        <el-menu :default-active="activeIndex" v-model="muted" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="1">Home</el-menu-item>
          <el-menu-item index="/forum">Forum</el-menu-item>
          <el-menu-item index="/chat">Chat</el-menu-item>
          <el-menu-item :disabled="username!=='admin'" index="/admin">Admin</el-menu-item>
          <el-menu-item style="float: right">Logged in as: {{ username }}</el-menu-item>
          <el-menu-item v-show="this.muted" style="float: right; color:red">You're currently muted</el-menu-item>
        </el-menu>
        <div class="line"></div>
    </el-header>
    <el-container style="height: 500px; border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
            <el-menu :default-openeds="['2', '3']">
              <el-menu-item :disabled="this.muted" index="1" @click="submit_file()"><i class="el-icon-upload2"></i>Share materials</el-menu-item>
              <el-submenu index="2" v-model="courseContent">
                <template slot="title"><i class="el-icon-document"></i>Course</template>
                  <el-menu-item v-for="(item) in courseContent" @click="openContent(item)"
                      :key="item.name"
                      :label="item.title"
                      :name="item.name">
                    {{ item.title }}
                  </el-menu-item>
              </el-submenu>
              <el-submenu index="3">
                <template slot="title"><i class="el-icon-setting"></i>Settings</template>
                  <el-menu-item index="3-1" @click="logout()"><i class="el-icon-back"></i>Log out</el-menu-item>
              </el-submenu>
            </el-menu>
        </el-aside>
        <el-container>
          <el-main id="main">
            <Component :is='pageName' :item="contentItem" @shareEvent="updateCourse"></Component>
          </el-main>
          <el-footer v-show="pageName==='Content'">
            <el-pagination
              layout="prev, pager, next"
              :total="50">
            </el-pagination>
          </el-footer>
        </el-container>
    </el-container>
  </div>
</template>
<script>
import Content from './Content'
import Share from './Share'
import axios from 'axios'
export default {
  data () {
    return {
      activeIndex: '1',
      pageName: '',
      contentItem: '',
      courseContent: [],
      username: sessionStorage.getItem('username'),
      muted: null
    }
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
      url: 'http://localhost:5000/api/get_file'
    }).then((res) => {
      this.courseContent = res.data
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
  },
  watch: {
    check_muted (mute) {
      this.muted = mute
    }
  },
  components: { Content, Share },
  methods: {
    handleSelect (key, keyPath) {
      if (key !== '1') {
        this.$router.push(key)
      }
    },
    openContent (item) {
      this.pageName = 'Content'
      this.contentItem = item
    },
    updateCourse (courseContent) {
      this.courseContent.push(courseContent)
    },
    submit_file () {
      this.pageName = 'Share'
    },
    logout () {
      sessionStorage.removeItem('username')
      sessionStorage.removeItem('privateKey')
      this.$router.push('/login')
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
