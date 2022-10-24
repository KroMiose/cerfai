<template>
  <div class="page">
    <div class="left">
      <div class="logo" @click="openAccessInputer">CERF-AI</div>
      <el-menu
        default-active="1-1"
        class="el-menu"
        @open="handleOpen"
        @close="handleClose"
        @select="selectMenu"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-location"></i>
            <span>词条贡献站</span>
          </template>
          <el-menu-item index="1-1">词条管理面板</el-menu-item>
        </el-submenu>
      </el-menu>
    </div>

    <div class="container">
      <el-page-header class="panel-header" @back="goBack" title="退出系统" :content="panelTitle"></el-page-header>
      <tagPanel ref="tagPanel" v-if="active_page == '1-1'" class="panel"></tagPanel>
    </div>
  </div>
</template>

<script>
import tagPanel from '@/components/tagPanel.vue'

export default {
  
  components: {tagPanel},
  data() {
    return {
      panelTitle: '词条管理页面',
      active_page: '1-1',
      categories: [],
      contributor_toplist: [],
      up_cnt: 0,
      prompt_enable: false,
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    selectMenu(key, keyPath) {
      console.log(key, keyPath);
      this.active_page = key
    },
    goBack() {
      this.$router.push('/')
    },
    // 获取分类
    get_categories() {
      let _this = this
      // 获取categories列表
      this.$http({
        method: 'GET',
        url: `${_this.$store.state.serverhost}/get_categories`,
      })
        .then((res) => {
          // console.log(res.data)
          // _this.categories = res.data.data
          _this.up_cnt = res.data.up_cnt
          // _this.categories.forEach((v, i) => {
          //   _this.categories[i].value = v.name
          // })
          // _this.roll_tag()
          let cd = res.data.contributor
          let nlist = []
          for(let key in cd){
            // console.log(key,obj[key])
            nlist.push({name: key, cnt: cd[key]})
          }
          _this.contributor_toplist = nlist
        })
        .catch((err) => {
          console.log(err)
        })
    },        

    openAccessInputer() {
      this.prompt_enable = true
      this.$prompt('请输入授权码', '提示', {
        confirmButtonText: '提交',
        cancelButtonText: '返回首页',
        inputErrorMessage: '输入内容有误'
      }).then(({ value }) => {
        let _this = this
        this.$http({
          method: 'POST',
          url: `${_this.$store.state.serverhost}/admin/check_access`,
          data: {token: value}
        })
          .then((res) => {
            if(res.data.code == 200) {
              this.$message({type: 'success', message: res.data.msg, duration: 2000});
              _this.$store.commit('setToken', value)
              _this.$refs.tagPanel.search()
            } else {
              // this.$router.push('/')
              this.$message({type: 'error', message: res.data.msg, duration: 2000});
              this.openAccessInputer()
            }
            this.prompt_enable = false
          })
        }).catch(() => {
          this.$message({type: 'error', message: '访问该页面需要授权码，即将自动跳转至首页', duration: 1500});
          setTimeout(() => {
            this.$router.push('/')
          }, 1000);
          this.prompt_enable = false
      });
    }
  },
  mounted() {
    let _this = this
    // this.get_categories()
    this.openAccessInputer()
  },
}
</script>

<style lang="scss" scoped>
.page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;

  .left {
    width: 200px;
    height: 100%;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .logo {
      height: 60px;
      width: 100%;
      background-color: #353a3a;
      color: #eee;
      font-size: 28px;
      line-height: 60px;
      text-align: center;
    }

    .el-menu {
      width: 200px;
      flex: 1;
    }
  }

  .container {
    height: 100%;
    flex: 1;
    
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;

    .panel-header {
      width: 100%;
      height: 60px;
      line-height: 60px;
      padding: 0 20px;
      border-bottom: 1px solid #eee;
      box-sizing: border-box;
    }

    .panel {
      width: 100%;
      flex: 1;
      box-sizing: border-box;
      padding: 16px;
    }
  }
}
</style>