// vue.config.js

const path = require('path')
const fs = require('fs')

module.exports = {
  devServer: {
    host: 'localhost',
    port: 8081, // 端口号
    open: true,
    https: {
      cert: fs.readFileSync(path.join(__dirname, 'src/ssl/cert.crt')),
      key: fs.readFileSync(path.join(__dirname, 'src/ssl/cert.key'))
    },
    proxy: {
      // '/File': {
      //   target: 'http://localhost:8887',
      //   ws: false,
      //   changeOrigin: true,
      //   pathRewrite: {
      //     '^/File': '/'
      //   }
      // },
      '/api': {
        target: 'http://localhost:5000',
        ws: false,
        changeOrigin: true
      }
    }
  }
}
