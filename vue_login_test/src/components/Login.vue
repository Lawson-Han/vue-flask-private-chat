<template>
    <div class="login-register">
      <div class="contain">
        <div class="big-box" :class="{active:isLogin}">
          <div class="big-contain" v-if="isLogin">
            <div class="btitle">Log in</div>
            <div class="bform">
              <el-form ref="loginFormRef" :model="loginForm" :rules="loginFormRules" label-width="100px" class="login_form">
                <!-- Credentials -->
                <el-form-item label="Username" prop="username">
                  <el-input v-model="loginForm.username" prefix-icon="el-icon-user"></el-input>
                </el-form-item>

                <el-form-item label="Password" prop="password">
                <el-input type="password" v-model="loginForm.password" prefix-icon="el-icon-lock"></el-input>
                </el-form-item>
              </el-form>
            </div>
            <button class="bbutton" @click="loginCheck()">Log in</button>
          </div>
          <div class="big-contain" v-else>
            <div class="btitle">Register</div>
            <div class="bform">
              <el-form ref="loginFormRef" :model="loginForm" :rules="loginFormRules" label-width="100px" class="login_form">
                <!-- Credentials -->
                <el-form-item label="Username" prop="username">
                  <el-input v-model="loginForm.username" prefix-icon="el-icon-user"></el-input>
                </el-form-item>

                <el-form-item label="Password" prop="password">
                  <el-input type="password" v-model="loginForm.password" prefix-icon="el-icon-lock" autocomplete="off"></el-input>
                </el-form-item>

                <el-form-item label="Comfirm" prop="confirm">
                  <el-input type="password" v-model="loginForm.confirm" prefix-icon="el-icon-lock" autocomplete="off"></el-input>
                </el-form-item>

            </el-form>
            </div>
            <button class="bbutton" @click="register()">Register</button>

          </div>
        </div>
        <div class="small-box" :class="{active:isLogin}">
          <div class="small-contain" v-if="isLogin">
            <div class="stitle">Don't have an account?</div>
            <p class="scontent">Chat secretly with friends</p>
            <button class="sbutton" @click="changeType">Register</button>
          </div>
          <div class="small-contain" v-else>
            <div class="stitle">Already have an account?</div>
            <p class="scontent">Start your secure trip</p>
            <button class="sbutton" @click="changeType">Log in</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios'
import crypto from 'crypto'
export default {
  name: 'login-register',
  data () {
    const checkConfirm = (rule, value, callback) => {
      if (this.loginForm.confirm !== this.loginForm.password) {
        callback(new Error(rule))
      } else {
        callback()
      }
    }
    return {
      isLogin: true,
      // 登陆表单的数据绑定对象
      loginForm: {
        username: '',
        password: '',
        confirm: ''
      },
      encrypted: [],
      // 表单规则验证
      loginFormRules: {
        username: [
          { required: true, message: 'Empty username', trigger: 'blur' },
          { min: 3, max: 10, message: 'Between 3 to 10 characters', trigger: 'blur' },
          { pattern: /^[A-Za-z0-9]+$/, message: 'Only alphanumeric characters' }
        ],
        password: [
          { required: false, message: 'Empty password', trigger: 'blur' },
          { min: 8, max: 15, message: 'Between 8 to 15 characters', trigger: 'blur' },
          { pattern: /^[A-Za-z0-9]+$/, message: 'Only alphanumeric characters' }
        ],
        confirm: [
          { required: false, message: 'Empty password', trigger: 'blur' },
          { validator: checkConfirm, message: 'Password is not the same', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    changeType () {
      this.isLogin = !this.isLogin
      this.$refs.loginFormRef.resetFields()
    },
    loginCheck () {
      this.$refs.loginFormRef.validate((valid) => {
        if (valid) {
          axios({
            method: 'post',
            url: 'http://localhost:5000/api/login',
            data: {
              username: this.loginForm.username
            }
          }).then((res) => {
            // res.data -> 后端返回数据 -> {status: -1}
            if (res.data.status === -1) {
              this.$message({
                type: 'error',
                message: 'Username does not exist'
              })
            } else {
              // res.data -> 后端返回数据 -> [{'id': 1, 'password': 'ffc852a2c8c114de2529ae70b6f33a19', 'salt': '8j38qxVE5d'}]
              const check = this.encrypted_check(this.loginForm.password, res.data.status[0].salt, res.data.status[0].password)
              if (check) {
                this.$message({
                  type: 'success',
                  message: 'Login success'
                })
                sessionStorage.setItem('username', this.loginForm.username)
                sessionStorage.setItem('privateKey', localStorage.getItem(this.loginForm.username + 'privateKey'))
                if (!localStorage.getItem(this.loginForm.username + '_muted')) {
                  localStorage.setItem(this.loginForm.username + '_muted', res.data.status[0].if_mute)
                }
                if (res.data.status[0]) {
                  this.$router.push({
                  // go to /chat
                    name: 'home',
                    params: { username: this.loginForm.username }
                  })
                }
              } else {
                this.$message({
                  type: 'error',
                  message: 'Wrong username or password'
                })
              }
            }
          })
        }
      })
    },
    register () {
      this.$refs.loginFormRef.validate((valid) => {
        if (valid) {
          this.encrypted = this.encrypt(this.loginForm.password)
          axios({
            method: 'post',
            url: 'http://localhost:5000/api/register',
            data: {
              username: this.loginForm.username,
              password: this.encrypted[0],
              publicKey: this.encrypted[2]
            }
          }).then((res) => {
            switch (res.data.status) {
              case true:
                this.$message({
                  type: 'success',
                  message: 'Register success'
                })
                sessionStorage.setItem('username', this.loginForm.username)
                localStorage.setItem(this.loginForm.username + 'privateKey', this.encrypted[3])
                localStorage.setItem(this.loginForm.username + '_muted', '0')
                sessionStorage.setItem('privateKey', localStorage.getItem(this.loginForm.username + 'privateKey'))
                this.$router.push({
                  name: 'home',
                  params: { username: this.loginForm.username }
                })
                break
              case false:
                this.$message({
                  type: 'error',
                  message: 'Username already exists'
                })
                break
            }
          })
        }
      })
    },
    encrypted_check (password, salt, encrypted) {
      const md5Password = crypto.createHash('md5')
      md5Password.update(password)
      const md5PwResult = md5Password.digest('hex')
      // 先对password进行hash 拿到salt以后再进行一次hash
      const md5Salt = crypto.createHash('md5')
      md5Salt.update(md5PwResult + salt)
      const result = md5Salt.digest('hex')
      if (result === encrypted) {
        return true
      } else {
        return false
      }
    },
    encrypt (password) {
      // 加密md5模式
      const md5 = crypto.createHash('md5')
      // 创建一个随机数
      // const salt = this.salt()
      let publicKey = ''
      let privateKey = ''
      if (this.loginForm.username === 'user1') {
        publicKey = '-----BEGIN PUBLIC KEY-----\n' +
        'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANngbUUrHeBziu9xfc8yy3q3j18nXnAE\n' +
        'Pe+nC/zwjOkM+iO5EN98zQXzYG45B6RB86GiZYt1HF9HKL/3hfh9ROcCAwEAAQ==\n' +
        '-----END PUBLIC KEY-----\n'
        privateKey = '-----BEGIN PRIVATE KEY-----\n' +
          'MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEA2eBtRSsd4HOK73F9\n' +
          'zzLLerePXydecAQ976cL/PCM6Qz6I7kQ33zNBfNgbjkHpEHzoaJli3UcX0cov/eF\n' +
          '+H1E5wIDAQABAkA6k9BNDG6X7fior8a3clyqvbdaSedmDn3odO0QMExyS3/mhNpA\n' +
          'VvaaluLgxqPS4uY+RJMI0xaB8DadnJBkwW3hAiEA7S2E3uRUr6HHUVChJSc98nBK\n' +
          'NJPiA+gxtmxvqG+4Pk0CIQDrKsmoZ1nC0wkNUaSadfGuiQARn1LyCSW2ATFNRY+y\n' +
          'AwIhANwjvMkZS1U9JoBeA0Q12TSWbvnALS8NLF8y5KyFDZCdAiBHV8G5zzDSBAfY\n' +
          '/I29Nk7Nrk5RCk61ksTYBGCamqHPVQIgUS1pRHzsg64f94vWoqwNndcnGyZILIk9\n' +
          'psE371xBApc=\n' +
          '-----END PRIVATE KEY-----'
      } else {
        publicKey = '-----BEGIN PUBLIC KEY-----\n' +
          'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAMQhb0+TnSnPBj2Iz4+HEgQlNdVFDNt+\n' +
          'apimchFexGbQ0dPRHj0rMpC9a8oAVGtxS8qmEYKa6J/hWlBMn/aF8M0CAwEAAQ==\n' +
          '-----END PUBLIC KEY-----\n'
        privateKey = '-----BEGIN PRIVATE KEY-----\n' +
          'MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAxCFvT5OdKc8GPYjP\n' +
          'j4cSBCU11UUM235qmKZyEV7EZtDR09EePSsykL1rygBUa3FLyqYRgpron+FaUEyf\n' +
          '9oXwzQIDAQABAkBtAtBlgHxYIpMrXIFRGxfuaegz878juG3zDoBUG0I6ilh3xcuH\n' +
          '/Iwfce35tqXU/S5NVcvk5qSqvEgVJdhEXjhBAiEA8Od8iOlw7ikpxTxmFB0en/4i\n' +
          '1Y6dCAU3MpGx/v2DK0UCIQDQa7P8TVTlND6IPLFDji+Qf6saJM3WXJ2DZJrJm1bD\n' +
          '6QIhAOBFYXbEfNH7mFt6gz2ublhca2mNPzu8P0rgwGi28mpRAiApklIEMSiNzy3p\n' +
          '3rE82E+EcvKd9FlaOH7yhk6Zh/J2gQIgbG43S40VbmQIqpH4vzA9fUXNleTS7fBD\n' +
          'iHQVP8zS3eU=\n' +
          '-----END PRIVATE KEY-----\n'
      }
      // 无salt进行md5加密
      md5.update(password)
      // 存储结果 -> 放进数据库
      const encrypted = []
      // 先对password进行一次hash 传入后端以后拼接salt再进行一次hash
      encrypted[0] = md5.digest('hex')
      // encrypted[1] = salt
      encrypted[2] = publicKey
      encrypted[3] = privateKey
      return encrypted
    }
    // salt () {
    //   // 10位随机数
    //   const str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    //   let result = ''
    //   for (let i = 10; i > 0; --i) {
    //     result += str[Math.floor(Math.random() * str.length)]
    //   }
    //   return result
    // }
  }
}
</script>

<style scoped="scoped">
    .login-register{
      width: 100vw;
      height: 100vh;
      box-sizing: border-box;
    }
    .contain{
      width: 50%;
      height: 55%;
      position: relative;
      top: 50%;
      left: 50%;
      transform: translate(-50%,-50%);
      background-color: #fff;
      border-radius: 20px;
      box-shadow: 0 0 3px #f0f0f0,
            0 0 6px #f0f0f0;
    }
    .big-box{
      width: 70%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 30%;
      transform: translateX(0%);
      transition: all 1s;
    }
    .big-contain{
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
    .btitle{
      font-size: 2em;
      font-weight: bold;
      color: rgb(57,167,176);
    }
    .bform{
      width: 100%;
      height: 40%;
      padding: 2em 0;
      display: flex;
      flex-direction: column;
      justify-content: space-around;
      align-items: center;
    }
    .bform .errTips{
      display: block;
      width: 50%;
      text-align: left;
      color: red;
      font-size: 0.7em;
      margin-left: 1em;
    }
    .bform input{
      width: 50%;
      height: 30px;
      border: none;
      outline: none;
      border-radius: 10px;
      padding-left: 2em;
      background-color: #f0f0f0;
    }
    .bbutton{
      width: 20%;
      height: 40px;
      border-radius: 24px;
      border: none;
      outline: none;
      background-color: rgb(57,167,176);
      color: #fff;
      font-size: 0.9em;
      cursor: pointer;
    }
    .small-box{
      width: 30%;
      height: 100%;
      background: linear-gradient(135deg,rgb(57,167,176),rgb(56,183,145));
      position: absolute;
      top: 0;
      left: 0;
      transform: translateX(0%);
      transition: all 1s;
      border-top-left-radius: inherit;
      border-bottom-left-radius: inherit;
    }
    .small-contain{
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
    .stitle{
      width: 70%;
      font-size: 1.5em;
      font-weight: bold;
      color: #fff;
    }
    .scontent{
      font-size: 0.9em;

      color: #fff;
      text-align: center;
      padding: 2em 4em;
      line-height: 1.7em;
    }
    .sbutton{
      width: 60%;
      font-weight: bold;
      height: 40px;
      border-radius: 24px;
      border: 1px solid #fff;
      outline: none;
      background-color: transparent;
      color: #fff;
      font-size: 1.0em;
      cursor: pointer;
    }
    .big-box.active{
      left: 0;
      transition: all 0.5s;
    }
    .small-box.active{
      left: 100%;
      border-top-left-radius: 0;
      border-bottom-left-radius: 0;
      border-top-right-radius: inherit;
      border-bottom-right-radius: inherit;
      transform: translateX(-100%);
      transition: all 1s;
    }
</style>
