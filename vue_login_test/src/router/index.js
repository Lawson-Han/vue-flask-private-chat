import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Chat from '../components/Chat.vue'
import Admin from '../components/Admin.vue'
import Home from '../components/Home.vue'
import Forum from '../components/Forum.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    { path: '/login', component: Login },
    { name: 'chat', path: '/chat', component: Chat, meta: { loginRequired: true } },
    { name: 'admin', path: '/admin', component: Admin, meta: { adminRequired: true } },
    { name: 'home', path: '/home', component: Home, meta: { loginRequired: true } },
    { name: 'forum', path: '/forum', component: Forum, meta: { loginRequired: true } },
    { path: '/', redirect: '/login' }
  ]
})
router.beforeEach((to, from, next) => {
  if (to.path !== '/login') {
    if (to.meta.loginRequired) {
    // 判断该路由是否需要登录权限
      if (sessionStorage.getItem('username')) {
        // 通过封装好的cookies读取token，如果存在，name接下一步 如果不存在，那跳转回登录页
        next()
      } else {
        next({
          path: '/login',
          query: { redirect: to.fullPath } // 将跳转的路由path作为参数，登录成功后跳转到该路由
        })
      }
    } else if (to.meta.adminRequired) {
      if (sessionStorage.getItem('username') === 'admin') {
        // 通过封装好的cookies读取token，如果存在，name接下一步 如果不存在，那跳转回登录页
        next()
      } else {
        next({
          path: from.path
        })
      }
    } else {
      next('/home')
    }
  } else {
    next()
  }
})
export default router
