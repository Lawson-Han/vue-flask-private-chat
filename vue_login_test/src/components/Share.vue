<template>
  <div>
    <h1> Share your file with all students </h1>
    <el-main v-model="fileList">
      <span class="demonstration"
            v-for="(item) in fileList"
            :key="item.name">
      </span>
    </el-main>
    <el-upload
    class="upload-demo"
    ref="upload"
    drag
    action="/api/file"
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :on-success="handleSuccess"
    :file-list="fileList"
    multiple>
    <i class="el-icon-upload"></i>
    <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
    <div class="el-upload__tip" slot="tip">Files with a size less than 500kb</div>
  </el-upload>
  </div>
</template>
<script>

import axios from 'axios'

export default {
  data () {
    return {
      fileList: []
    }
  },
  created () {

  },
  methods: {
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file, fileList) {
      console.log(fileList)
    },
    handleSuccess (response, file, fileList) {
      const fileUploaded = {
        name: file.name,
        title: file.name.substring(0, file.name.lastIndexOf('.')),
        url: file.response,
        user: sessionStorage.getItem('username'),
        format: file.name.substring(file.name.lastIndexOf('.') + 1).toUpperCase()
      }
      this.fileList.push(fileUploaded)
      this.$emit('shareEvent', fileUploaded)
      axios({
        method: 'post',
        url: 'http://localhost:5000/api/add_file',
        data: {
          name: file.name,
          title: file.name.substring(0, file.name.lastIndexOf('.')),
          url: file.response,
          user: sessionStorage.getItem('username'),
          format: file.name.substring(file.name.lastIndexOf('.') + 1).toUpperCase()
        }
      })
    }
  }
}
</script>
