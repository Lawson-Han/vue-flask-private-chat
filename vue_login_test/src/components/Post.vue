<template>
  <div class="block">
    <el-main v-model="item">
      <el-descriptions class="margin-top" title="Question" :column="1">
        <el-descriptions-item label="Title"> {{ item.title }}</el-descriptions-item>
        <el-descriptions-item label="Provider"> {{ item.provider }}</el-descriptions-item>
        <el-descriptions-item label="Description"> {{ item.description }}</el-descriptions-item>
      </el-descriptions>
      <h4>Answer</h4>
      <span class="demonstration"
              v-for="(answer) in activeComment"
              :key="answer.id"
              :value="answer.answer">
       {{ answer.answer }}
       <el-divider content-position="right">{{ answer.user }}</el-divider>
       <br>
      </span>
    </el-main>
    <el-footer v-model="formInline">
        <el-form :inline="true" class="demo-form-inline">
          <el-form-item>
            <el-input :disabled="this.muted" type="textarea" v-model="formInline.answer" placeholder="The answer is..."></el-input>
          </el-form-item>
          <el-form-item>
            <el-button :disabled="this.muted" type="primary" @click="postAnswer(item)">Answer</el-button>
          </el-form-item>
        </el-form>
      </el-footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['item'],
  data () {
    return {
      comments: [
        { qid: 1, id: -1, user: 'noUser1', answer: 'There is only one answer to this' },
        { qid: 1, id: 0, user: 'admin', answer: 'Probably works' }
      ],
      formInline: [{
        answer: '',
        user: ''
      }],
      muted: '',
      username: sessionStorage.getItem('username')

    }
  },
  created () {
    if (localStorage.getItem(this.username + '_muted') === '0') {
      this.muted = false
      // this.$dispatchEventStorage(this.username + '_muted', 'haha')
    } else {
      this.muted = true
    }
  },
  computed: {
    activeComment: function () {
      return this.comments.filter((comment) => {
        return comment.qid === this.item.id
      })
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
    axios({
      method: 'post',
      url: 'http://localhost:5000/api/get_comment',
      data: {
        qid: this.item.id
      }
    }).then((res) => {
      for (let i = 0; i < res.data.length; i++) {
        this.comments.push(res.data[i])
      }
    })
  },
  methods: {
    postAnswer (item) {
      axios({
        method: 'post',
        url: 'http://localhost:5000/api/add_comment',
        data: {
          qid: this.item.id,
          user: sessionStorage.getItem('username'),
          answer: this.formInline.answer
        }
      }).then((res) => {
        const comment = {
          qid: this.item.id,
          id: res.data.status,
          user: sessionStorage.getItem('username'),
          answer: this.formInline.answer
        }
        this.comments.push(comment)
        this.$message({
          type: 'success',
          message: 'Post question successfully'
        })
        this.formInline.answer = ''
      })
    }

  }
}
</script>
