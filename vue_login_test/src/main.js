import Vue from 'vue'
import './plugins/bootstrap-vue'
import './plugins/axios'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/element.js'
// 导入全局样式表
import './assets/css/global.css'
import jsRsasign from 'jsrsasign'

// import VueSocketio from 'vue-socket.io'
// Vue.use(VueSocketio, 'https://127.0.0.1:5000')
// import axios from 'axios'
// import './plugins/socketPlugin'

// 配置请求的根路径
// axios.defaults.baseURL = 'http://127.0.0.1:5000/api/'
// Vue.prototype.$http = axios

// import VueSocketIO from 'vue-socket.io'
// Vue.config.productionTip = false
// Vue.use(new VueSocketIO({
//   debug: true,
//   connection: 'https://localhost:5000',
//   autoConnect: false
// }))

Vue.prototype.systemKey = 'aOm1a0Z1Tx9FGY7K'

/**
 * 生成签名
 * @param {Object} strIng
 * @return {type}
 **/
// 加签(用自己的私钥对signData进行签名)
Vue.prototype.$signature = function (strIng, key) {
  // 创建RSAKey对象
  // var rsa = new jsRsasign.RSAKey()
  // 因为后端提供的是pck#8的秘钥对，所以这里使用 KEYUTIL.getKey来解析秘钥
  var signPrivateKey = key
  // 将密钥转码,其实就是将头部尾部默认字符串去掉
  // alg:对应的是规则 需要和后端统一
  var sig = new jsRsasign.KJUR.crypto.Signature({ alg: 'MD5withRSA', prov: 'cryptojs/jsrsa', prvkeypem: signPrivateKey })
  // 初始化
  sig.init(signPrivateKey)
  // 传入待加密字符串
  sig.updateString(strIng)
  // 生成密文
  // 如果对加密后内容进行URI编码
  // sign = encodeURIComponent(sign)
  return sig.sign()
}

/**
 * 验证签名
 * @param {String} strIng 签名前的明文
 * @param {String} data 签名后的数据
 * @return {Boolean} true | false
 */
Vue.prototype.$testSignature = function (strIng, data, key) {
  // 创建RSAKey对象
  // var rsa = new jsRsasign.RSAKey()
  // 因为后端提供的是pck#8的公钥对，所以这里使用 KEYUTIL.getKey来解析公钥
  var signPublicKey = key
  // 创建Signature对象，设置签名编码算法
  var sig = new jsRsasign.KJUR.crypto.Signature({

    alg: 'MD5withRSA',
    prov: 'cryptojs/jsrsa',
    prvkeypem: signPublicKey
  })
  // 初始化

  sig.updateString(strIng)
  return sig.verify(data)
}
Vue.prototype.$dispatchEventStorage = function (key, val) {
  const signSetItem = localStorage.setItem
  localStorage.setItem = function (key, val) {
    const setEvent = new Event('setItemEvent')
    setEvent.key = key
    setEvent.newValue = val
    window.dispatchEvent(setEvent)
    signSetItem.apply(this, arguments)
  }
}
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
