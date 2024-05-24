<template>
  <div class='chat'>
      <el-tabs class="chat__header" v-model="activeName">
      <el-tab-pane name="Back">
        <div slot="label" @click="back"><i class="el-icon-back"></i>Back</div>
      </el-tab-pane>
      <el-tab-pane name='User'>
        <span slot="label"><i class="el-icon-user"></i>User</span>
          <el-table
            :data="user_tableData"
            ref="singleTable"
            style="width: 100%"
            highlight-current-row
            max-height="680">
            <el-table-column
              label="ID"
              prop="id">
            </el-table-column>
            <el-table-column
              label="Name"
              prop="username">
            </el-table-column>
            <el-table-column
              label="Mute"
              prop="if_mute">
              <template slot-scope="scope">
                <i class="el-icon-turn-off-microphone" style="margin: 0 10px; font-size: 20px; color: red" v-show="scope.row.if_mute === 1"></i>
                <i class="el-icon-microphone" style="margin: 0 10px; font-size: 20px; color: green" v-show="scope.row.if_mute === 0"></i>
              </template>
            </el-table-column>
            <el-table-column
              align="right">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  v-show="scope.row.if_mute"
                  @click="handleEdit(scope.$index, scope.row)">Unmute</el-button>
                <el-button
                  size="mini"
                  v-show="!scope.row.if_mute"
                  @click="handleEdit(scope.$index, scope.row)">Mute</el-button>
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
              </template>
            </el-table-column>
          </el-table>
      </el-tab-pane>
      <el-tab-pane label="Documents">
        <span slot="label"><i class="el-icon-document"></i> Documents</span>
        <el-table
            :data="document_tableData"
            ref="singleTable"
            style="width: 100%"
            max-height="680">
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-position="left" inline class="demo-table-expand">
                  <el-form-item class="item" label="File title">
                    <span>{{ props.row.title }}</span>
                  </el-form-item>
                  <el-form-item class="item" label="File fullname">
                    <span>{{ props.row.name }}</span>
                  </el-form-item>
                  <el-form-item class="item" label="File format">
                    <span>{{ props.row.format }}</span>
                  </el-form-item>
                  <el-form-item class="item" label="File path">
                    <span>{{ props.row.url }}</span>
                  </el-form-item>
                  <el-form-item class="item" label="Provider">
                    <span>{{ props.row.user }}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column
              label="Filename"
              prop="name">
            </el-table-column>
            <el-table-column
              label="Format"
              prop="format">
            </el-table-column>
            <el-table-column
              label="User"
              prop="user">
            </el-table-column>
            <el-table-column
              align="right">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
              </template>
            </el-table-column>
          </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

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
  height: 100%;
}

  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #6e7a8c;
  }

  .demo-table-expand  {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
  .item {
    margin-right: 0;
    margin-bottom: 0;
    width: 600px;
  }

</style>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      user_tableData: [],
      document_tableData: [],
      currentRow: null,
      activeName: 'User'
    }
  },
  created () {
    axios({
      method: 'post',
      url: 'http://localhost:5000/api/get_user'
    }).then((res) => {
      this.user_tableData = res.data
    })
    axios({
      method: 'post',
      url: 'http://localhost:5000/api/get_file'
    }).then((res) => {
      this.document_tableData = res.data
    })
  },
  methods: {
    handleEdit (index) {
      if (this.user_tableData[index].if_mute === 0) {
        this.user_tableData[index].if_mute = 1
        this.$store.commit('mute', this.user_tableData[index].username)
      } else {
        this.user_tableData[index].if_mute = 0
        this.$store.commit('unmute', this.user_tableData[index].username)
      }
    },
    handleDelete (index, row) {
      console.log(index, row)
      this.$confirm('This will permanently delete the user. Continue?', 'Warning', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: 'Delete completed'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: 'Cancelled'
        })
      })
    },
    back () {
      this.$router.push('/home')
    }
  }
}
</script>
