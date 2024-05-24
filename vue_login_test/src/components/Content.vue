<template>
  <div class="block">
    <el-main v-model="item">
      <el-descriptions class="margin-top" title="Course Description" :column="1">
        <el-descriptions-item label="Title"> {{ item.title }}</el-descriptions-item>
        <el-descriptions-item label="Provider"> {{ item.user }}</el-descriptions-item>
        <el-descriptions-item label="UID" :span="2">{{ item.uid }}</el-descriptions-item>
        <el-descriptions-item label="Format" :span="2">{{ item.format }}</el-descriptions-item>
        <el-descriptions-item label="Tag">
          <el-tag size="small">Materials</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="URL">{{ item.url }}</el-descriptions-item>
      </el-descriptions>
      <el-button style="margin-top: 10px" type="primary" icon="el-icon-download"
      @click="download(item)">Download</el-button>
    </el-main>
  </div>
</template>

<script>
import download from 'downloadjs'
export default {
  props: ['item'],
  data () {
    return {

    }
  },
  methods: {
    download (item) {
      // window.open('http://127.0.0.1:8887/' + item.name)
      download('http://127.0.0.1:8887/' + item.name)
    }
  }
}
</script>
