<template>
  <div class="tableFilter">
    <el-popover placement="top" v-model="filterVisiable">

      <p class="ftitle">最后更新时间过滤:</p>
      <div v-if="showPanel.date_picker" class="row">
        <span>日期范围：</span>
        <div class="col" :span="12">
          <div class="block">
            <el-date-picker
              v-model="filterValue.dateValue"
              type="daterange"
              align="right"
              unlink-panels
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :picker-options="pickerOptions"
            >
            </el-date-picker>
          </div>
        </div>
      </div>

      <p v-if="showPanel.order_opt" style="padding-bottom: 2px; margin-bottom: 4px; border-bottom: 1px solid #eee">排序项:</p>
      <div v-if="showPanel.order_opt" class="row">
        <span>排序方式:</span>
        <div class="col" :span="12">
          <el-select v-model="filterValue.order" clearable placeholder="排序方式">
            <el-option
              v-for="(item, idx) in orderOptions"
              :key="idx"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </div>
      </div>

      <div style="text-align: right; margin: 10px 0 0">
        <el-button
          size="mini"
          type="text"
          @click="
            reload();
            filterVisiable = false;"
          >重置</el-button
        >
        <el-button
          type="primary"
          size="mini"
          @click="
            filterVisiable = false;
            freshen();"
          >确定</el-button
        >
      </div>
      <el-button slot="reference">
        <i class="el-icon-set-up"></i>
      </el-button>
    </el-popover>
  </div>
</template>

<script>
export default {
  props: {
    showPanel: Object,
  },
  data() {
    return {
      filterVisiable: false,
      filterValue: {
        dateValue: [],
        publishtime: '',
        order: '',
      },

      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近一年',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近两年',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365 * 2);
            picker.$emit('pick', [start, end]);
          }
        }, {
          text: '最近三年',
          onClick(picker) {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365 * 3);
            picker.$emit('pick', [start, end]);
          }
        }]
      },

      orderOptions: [
        {
            value: 'xxx',
            label: 'xxx升序',
        },
        {
            value: '-xxx',
            label: 'xxx降序',
        },
      ],

      wechatOps: [],
    }
  },
  mounted() {
    // console.log(this.showPanel)
  },
  methods: {
    getFilter() {
      let pub_time = ''
      if((this.filterValue.dateValue[0]) && this.formatDateTime(this.filterValue.dateValue[1])) {
        pub_time = this.formatDateTime(this.filterValue.dateValue[0]) + '_' + this.formatDateTime(this.filterValue.dateValue[1])
      }
      this.filterValue.publishtime = pub_time
      return this.filterValue
    },
    // 格式化时间成 YYYY-mm-dd
    formatDateTime(obj) {
      if (obj == null) {
          return null
      }
      let date = new Date(obj);
      let y = 1900 + date.getYear();
      let m = "0" + (date.getMonth() + 1);
      let d = "0" + date.getDate();
      return y + "-" + m.substring(m.length - 2, m.length) + "-" + d.substring(d.length - 2, d.length);
    },
  }
}
</script>

<style lang="scss" scoped>

.ftitle {
  padding-bottom: 2px;
  margin-bottom: 4px;
  border-bottom: 1px solid #eee;
}
.el-popover {
  width: 650px;
  padding: 0 10px;
  margin-right: 10px;
}

.el-picker-panel {
  margin-left: -40% !important;
}

.el-popper {
  .row {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;

    padding: 0 10px;
    margin-bottom: 4px;
    width: 100%;

    .col {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;
      margin: 0 10px;

      .el-input__inner {
        width: 350px;
      }
    }
  }

  .el-select {
    margin: 2px 0 2px;
  }
}

.el-picker-panel__body-wrapper {
  width: 640px;
}
</style>