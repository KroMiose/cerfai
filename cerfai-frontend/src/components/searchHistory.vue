<template>
    <el-row class="historyBox">
        <el-col :span="2">
            <b><i class="el-icon-time"></i>历史记录:</b>
        </el-col>
        <el-col :span="21">
            <div class="histories" :class="{ lh: extended }">
                <el-tag class="history-block" v-for="{w,i} in datas" @click="$emit('select', $event.target.getAttribute('data-history-data'))" :data-history-data="w" :key="i">{{ w }}
                </el-tag>
            </div>
        </el-col>
        <el-col :span="1">
            <div class="control">
                <el-button icon="el-icon-arrow-up" circle v-if="!extended" @click="extended=1" size="small"></el-button>
                <el-button icon="el-icon-arrow-down" circle v-if="extended" @click="extended=0" size="small"></el-button>
            </div>
            <div class="control">
                <el-button icon="el-icon-delete" circle  @click="clearData" size="small"></el-button>
            </div>
        </el-col>
    </el-row>
</template>

<script>
export default {
    props: ["datas"],
    emits: ["select", "clear"],
    data() {
        return {
            extended: true
        }
    },methods: {
        clearData() {
            let _this = this;
            this.$confirm('确定删除历史记录吗？', '确认？', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
                
            }).then(() => {
                _this.$emit('clear')
            }).catch(()=>{});
        }
    }
}

</script>
<style>
.historyBox{
    width:100%;
    border: 1px solid #DCDFE6;
    border-radius: 4px;
}
.lh {
    height: 50px;
    overflow: hidden;
}
.control{
    text-align: right;
    padding: 3px;
}
.histories{
    padding: 5px;
}
.history-block{
    margin: 3px;
    cursor: pointer;
}
.history-block:hover{
    text-decoration: underline;
}
</style>