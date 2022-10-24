<template>
  <div class="tagPanel">
    <div class="row">
      <el-pagination class="pagination"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pageIndex"
        :page-sizes="[20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
      <div class="row">
        <el-input v-model="search_keyword" placeholder="请输入词条名"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="search"></el-button>
        <el-button type="danger" plain icon="el-icon-close" @click="clear"></el-button>
        <!-- <tableFilter class="tableFilter" :showPanel="showPanel"></tableFilter> -->
      </div>
    </div>
    <div class="table-view">
      <el-table
        :data="tableData"
        :height="'99%'"
        @row-click="getRow"
        border fit
        @sort-change="sort_change"
        :default-sort="{prop: 'update_time', order: 'descending'}"
        style="width: 100%">
        <el-table-column prop="name" label="词条名" min-width="80" sortable="custom"></el-table-column>
        <el-table-column prop="t_name" label="词条译名" min-width="80" sortable="custom">
          <template v-slot="scope">
            <el-tooltip class="item" effect="dark" :content="tableData[scope.$index].t_name" placement="top-start">
              <span class="s_name_dsp">{{tableData[scope.$index].t_name}}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="c_id" label="分类" min-width="80" sortable="custom">
          <template v-slot="scope">
            <span v-text="get_category_name(tableData[scope.$index].c_id)"></span>
          </template>
        </el-table-column>
        <el-table-column prop="desc" label="词条说明" min-width="80" sortable="custom">
          <template v-slot="scope">
            <el-tooltip class="item" effect="dark" :content="tableData[scope.$index].desc" placement="top-start">
              <span class="s_name_dsp">{{tableData[scope.$index].desc}}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="remarks" label="词条备注" min-width="80" sortable="custom">
          <template v-slot="scope">
            <el-tooltip class="item" effect="dark" :content="tableData[scope.$index].remarks" placement="top-start">
              <span class="s_name_dsp">{{tableData[scope.$index].remarks}}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="contributor" label="贡献者" min-width="80" sortable="custom">
          <template v-slot="scope">
            <el-tooltip class="item" effect="dark" :content="tableData[scope.$index].contributor" placement="top-start">
              <span class="s_name_dsp">{{tableData[scope.$index].contributor}}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="is_nsfw" label="是否NSFW" min-width="90" sortable="custom">
          <template v-slot="scope">
            <el-tag v-if="tableData[scope.$index].is_nsfw" type="danger">NSFW</el-tag>
            <el-tag v-else>安全</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_locked" label="是否锁定" min-width="80" sortable="custom">
          <template v-slot="scope">
            <el-tag v-if="tableData[scope.$index].is_locked" type="warning">已锁定</el-tag>
            <el-tag v-else type="success">未锁定</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="update_time" label="上次更新时间" min-width="110" sortable="custom">
          <template v-slot="scope">
            <span v-text="GMTToStr(tableData[scope.$index].update_time)"></span>
          </template>
        </el-table-column>
        <el-table-column prop="update_times" label="更新次数" min-width="80" sortable="custom"></el-table-column>
        <el-table-column label="操作" width="90">
          <template>
            <el-button size="mini" type="primary" style="margin: 0 1px" @click="drawer = true" plain>详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-drawer
      title="歌单详情"
      :withHeader="false"
      :visible.sync="drawer"
      size="800px"
      direction="rtl"
    >
      <div class="drawer">
        <el-descriptions
          class="margin-top"
          title="词条详情"
          :column="2"
          size="small"
          border
        >
          <template slot="extra">
            <el-button type="primary" size="small" @click="submitUpdate"
              >提交修改</el-button
            >
          </template>

          <el-descriptions-item>
            <template slot="label"><i class="el-icon-mobile-phone"></i>词条名</template>
            {{ selRowData.name }}
          </el-descriptions-item>

          
          <el-descriptions-item span="1">
            <template slot="label">
              <i class="el-icon-s-comment"></i>
              词条译名
            </template>
            <el-input
              placeholder="请输入词条译名"
              v-model="selRowData.t_name"
            >
            </el-input>
          </el-descriptions-item>

          <el-descriptions-item>
            <template slot="label"><i class="el-icon-s-custom"></i>是否NSFW</template>
            <el-switch
              style="display: block"
              v-model="selRowData.is_nsfw"
              active-color="#ff8989"
              inactive-color="#13ce66"
              active-text="NSFW"
              inactive-text="正常">
            </el-switch>
          </el-descriptions-item>

          <el-descriptions-item>
            <template slot="label"><i class="el-icon-key"></i>是否锁定</template>
            <el-switch
              style="display: block"
              v-model="selRowData.is_locked"
              active-color="#ffd949"
              inactive-color="#13ce66"
              active-text="锁定词条"
              inactive-text="解锁词条">
            </el-switch>
          </el-descriptions-item>

          <el-descriptions-item>
            <template slot="label"><i class="el-icon-headset"></i>上次更新时间</template>
            {{ GMTToStr(selRowData.update_time) }}
          </el-descriptions-item>

          <el-descriptions-item>
            <template slot="label"><i class="el-icon-star-off"></i>更新总次数</template>
            {{ selRowData.update_times }}
          </el-descriptions-item>

          <el-descriptions-item span="2">
            <template slot="label">
              <i class="el-icon-s-comment"></i>
              词条分类
            </template>
            <category-selector :value="selRowData.c_id" @change="nv => selRowData.c_id =nv"></category-selector>
          </el-descriptions-item>

          <el-descriptions-item span="2">
            <template slot="label">
              <i class="el-icon-s-comment"></i>
              词条说明
            </template>
            <el-input
              type="textarea"
              :rows="6"
              placeholder="请输入词条说明"
              v-model="selRowData.desc"
            >
            </el-input>
          </el-descriptions-item>

          <el-descriptions-item span="2">
            <template slot="label">
              <i class="el-icon-s-comment"></i>
              词条备注
            </template>
            <el-input
              type="textarea"
              :rows="6"
              placeholder="请输入词条备注"
              v-model="selRowData.remarks"
            >
            </el-input>
          </el-descriptions-item>

          <el-descriptions-item span="2">
            <template slot="label">
              <i class="el-icon-s-comment"></i>
              贡献者
            </template>
            <el-input
              type="textarea"
              :rows="6"
              placeholder="请输入词条备注"
              v-model="selRowData.contributor"
            >
            </el-input>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import tableFilter from '@/components/tableFilter.vue'
import categorySelector from '@/components/categorySelector.vue'

export default {

  components: { tableFilter, categorySelector },
  data() {
    return {
      search_keyword: '',
      pageIndex: 1,
      pageSize: 20,
      total: 0,
      tableData: [],
      drawer: false,
      selRowData: {},
      sortkey: '-update_time',
      categories: [],

      showPanel: {
        date_picker: true,  // 日期区间
        order_opt: true,    // 排序选项
      },
    }
  },
  methods: {
    // 获取行信息
    getRow(row) {
      this.selRowData = JSON.parse(JSON.stringify(row))
      this.cmpSelRowData = JSON.parse(JSON.stringify(row))
    },
    // 搜索tag
    search() {
      let _this = this
      // 获取categories列表
      this.$http({
        method: 'POST',
        url: `${_this.$store.state.serverhost}/admin/filter_tags`,
        data: {
          keyword: _this.search_keyword,
          page: _this.pageIndex,
          limit: _this.pageSize,
          token: _this.$store.state.token,
          order: _this.sortkey
        }
      })
        .then((res) => {
          if(res.data.code == 200) {
            // console.log(res.data)
            if(res.data.data.length > 0) {
              _this.tableData =  res.data.data
              _this.total = res.data.total
              _this.$message({type: 'success', message: '获取词条列表成功', duration: 2000})
            } else {
              _this.$message({type: 'info', message: '查无相关数据', duration: 2000})
              _this.tableData = []
            }
            
          } else {
            _this.$message({type: 'error', message: res.data.msg, duration: 2000})
          }
        })
        .catch((err) => {
          _this.$message({type: 'error', message: '请求后端服务器发生错误或未授权', duration: 2000})
        })
    },
    clear() {
      this.search_keyword = ''
      this.search()
    },
    submitUpdate() {
      let _this = this
      // 提交修改
      this.$http({
        method: 'POST',
        url: `${_this.$store.state.serverhost}/admin/edit_tag`,
        data: {..._this.selRowData, token: _this.$store.state.token},
      })
        .then((res) => {
          if(res.data.code == 200) {
            _this.search()
            _this.drawer = false
            _this.$message({type: 'success', message: res.data.msg, duration: 2000})
          } else {
            _this.$message({type: 'error', message: res.data.msg, duration: 2000})
          }
        })
        .catch((err) => {
          _this.$message({type: 'error', message: '请求后端服务器发生错误或未授权', duration: 2000})
        })
    },
    sort_change(v) {
      console.log(v)
      if(v.order == "ascending")
        this.sortkey = v.prop
      else if (v.order == 'descending')
        this.sortkey = '-' + v.prop
      else
        this.sortkey = ''
      this.search()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.search()
    },
    handleCurrentChange(val) {
      this.pageIndex = val
      this.search()
    },
    // 转换时间
    GMTToStr(date){
      if(date) {
        // console.log(date)
        date = new Date(date.slice(0,-4))
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        m = m < 10 ? ('0' + m) : m;
        var d = date.getDate();
        d = d < 10 ? ('0' + d) : d;
        var h = date.getHours();
        h=h < 10 ? ('0' + h) : h;
        var minute = date.getMinutes();
        minute = minute < 10 ? ('0' + minute) : minute;
        var second=date.getSeconds();
        second=second < 10 ? ('0' + second) : second;
        return y + '-' + m + '-' + d+' '+h+':'+minute+':'+second;
      } else {
        return ''
      }
    },
    // 切换分类选项
    categoryHandleSelect(item) {
      console.log(item);
      this.selRowData.c_id = item.id
    },
    // 检索建议列表
    querySearch(queryString, cb) {
      var categories = this.categories;
      var results = queryString ? categories.filter(this.createFilter(queryString)) : categories;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    createFilter(queryString) {
      return (categories) => {
        return (categories.name.toLowerCase().indexOf(queryString.toLowerCase()) >= 0);
      };
    },
    // 获取分类列表
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
          let cd = res.data.contributor
          let nlist = []
          for(let key in cd){
            // console.log(key,obj[key])
            nlist.push({name: key, cnt: cd[key]})
          }
          _this.contributor_toplist = nlist
          _this.get_categories_full()
        })
        .catch((err) => {
          console.log(err)
        })
    },
    //获取完整的分类列表
    //TODO:该函数为过渡方案，等待替换
    get_categories_full() {
      let _this = this
      // 获取categories列表
      this.$http({
        method: 'GET',
        url: `${_this.$store.state.serverhost}/open/get_full_categories`,
      }).then((res) => {
        // console.log(res.data)
        _this.categories = res.data.data
        _this.$store.commit('setCategories', _this.categories)
      })
        .catch((err) => {
          console.log(err)
        })

    },
    // 获取分类名
    get_category_name(id) {
      let res = '未知分类'
      this.categories.forEach((v) => {
        if(v.id == id) {
          res = v.name
        }
      })
      return res
    },
  },
  mounted() {
    this.search()
    this.get_categories()
  }
}
</script>

<style lang="scss" scoped>
.tagPanel {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;

  .row {
    box-sizing: border-box;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin: 5px 0;

    .pagination {
      box-sizing: border-box;
    }

    .row {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
      max-width: 500px;

      .el-button {
        margin-left: 4px;
      }

      .tableFilter {
        margin-left: 4px;
      }
    }

  }

  .table-view {
    width: 99%;
    flex: 1;
    overflow: hidden;

    .s_name_dsp {
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 3;
      overflow: hidden;
    }
  }
}
</style>