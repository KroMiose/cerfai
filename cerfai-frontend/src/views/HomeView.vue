<template>
    <div class="home">
        <el-menu :default-active="activeIndex" class="menu" mode="horizontal" @select="handleSelect">
            <el-menu-item index="tag">Novelai词条贡献站 ></el-menu-item>
            <el-menu-item index="tag_search">搜索词条</el-menu-item>
            <el-menu-item index="contributor">贡献榜</el-menu-item>
            <el-menu-item index="share">共享计划</el-menu-item>
        </el-menu>

        <el-collapse class="collapse" v-model="activeNames">
            <el-collapse-item title="Novelai词条资源贡献站" name="1">
                <div>
                    本站皆在建立novelai中所包含的词条解释数据库，为广大魔导师提供词条贡献平台，所有收集的数据在收集整理后进行公开，为novelai开源生态建立数据仓库基础，如果您有其他数据源或者自行整理的词条信息，并且希望参与本站建设，可以直接联系我们进行批量数据导入<br />
                    联系方式：QQ: 2513675036(墨安) / 621816415(洛儿)<br />
                    本站交流群：660612010
                </div>
                <div>目前已收到用户贡献词条数: {{ up_cnt }}</div>
                <div>当前站点已收录总词条数: {{ ct_total }}</div>
                <div>参与贡献基本原则：在不破坏他人劳动成果的前提下，对词条原有信息做任何有效补充均可视为有效贡献</div>
            </el-collapse-item>
            <el-collapse-item title="贡献操作指南" name="2">
                <div>
                    您所看到的所有词条内容来自 机器翻译/人工初筛/其他用户个人上传。
                    欢迎对词条进行内容审核或者参与实际测试，并提供宝贵的建议。
                    如果您认为该词条准确无误，请点击提交，将自动随机下一条标签。
                    输入词条分类关键词，可以快速选择词条分类。
                    如果该词条没有适合的分类，请输入并选择 “标签扩展” 并可在备注中描述新的分类，
                    如果经多方测试，标签无效或者当前版本无效，请输入并选择“无效标签”
                    如果您对当前标签没兴趣或者不需要进行修改，点击“换一个”更换词条。
                </div>
                <div>
                    <strong>词条名：<br /></strong>
                    是指导入数据库的Tag英文原名，软件可识别的词条/标签。
                </div>
                <div>
                    <strong>词条译名：<br /></strong>
                    是指词条翻译的中文名，或者贡献者修改的译名，最好是中文版AI可识别的译名。因为尚未校正，可能存在翻译错误。
                </div>
                <div>
                    <strong>是否NSWF：<br /></strong>
                    当前标签生成图片时是否会出现不适合工作场合的画面，包括不限于血腥暴力和敏感内容，如果是请打开此项。
                </div>
                <div>
                    <strong>词条说明：<br /></strong>
                    对于词条的补充和内容说明。对标签进行测试时，建议标明SD测试还是NF测试，两者会有些许差异。单独使用标签与实际混合标签时会产生不同效果，cfg参数会影响标签效果，标签数字权重与{}的增加也会标签产生的效果，建议多次测试确定效果。
                </div>
                <div>
                    <strong>备注信息：<br /></strong>
                    词条的来源和调查。词条的正确译名可能需要借助谷歌等搜索引擎，容易产生误解的是画师账号昵称和人名，并且可能由于关联搜索而出现奇怪的内容，导致内容与标签毫无关联，这取决于模型的收录程度，如果要强调画师或者风格，应该加上by_或者（style）
                </div>
                <div>
                    <strong>贡献者：<br /></strong>
                    所有参与词条编辑的人都可以填入贡献者名字，请使用常用的昵称或者数字字母，提交词条将计入贡献名单，优秀的内容提交者将在榜单上体现，请尊重自己和他人的劳动成果，恶意删改将会触发网站防御，并拉入AI绘画信息并联计划黑名单。
                </div>
            </el-collapse-item>
        </el-collapse>

        <div class="container">

            <!-- 贡献表单 -->
            <el-form v-show="activeIndex == 'tag'" ref="form" :model="form" label-width="100px">
                <el-form-item label="词条名：">
                    <div class="row">
                        <el-input v-model="form.name" disabled></el-input>
                        <el-button type="primary" v-clipboard:copy="form.name" v-clipboard:success="onCopy"
                            v-clipboard:error="onError">复制词条名</el-button>
                    </div>
                </el-form-item>
                <el-form-item label="词条译名：">
                    <el-input v-model="form.t_name"></el-input>
                </el-form-item>
                <el-form-item label="词条分类：">
                    <category-selector :value="form.c_id" @change="nv => form.c_id =nv"></category-selector>
                </el-form-item>
                <el-form-item label="是否NSFW：">
                    <el-switch v-model="form.is_nsfw"></el-switch>
                    <span class="nsfw-span" style="color: #e66" v-show="form.is_nsfw">这是一个包含工作场所不宜内容的词条</span>
                    <span class="nsfw-span" v-show="!form.is_nsfw">这是一个任何场所安全的词条</span>
                </el-form-item>
                <el-form-item label="词条说明：">
                    <el-input type="textarea" v-model="form.desc" placeholder="请输入词条说明信息，作为该词条的使用参考或者效果"></el-input>
                </el-form-item>
                <el-form-item label="备注信息：">
                    <el-input type="textarea" v-model="form.remarks" placeholder="请输入备注信息，可包含该词条信息依据的参考资料链接"></el-input>
                </el-form-item>
                <el-form-item label="贡献者：">
                    <el-input v-model="form.contributor" placeholder="请留下您的用户名或昵称，以便我们记录贡献者，多位贡献者请用英文逗号分隔"></el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="onSubmit">提交</el-button>
                    <el-button @click="roll_tag">换一个</el-button>
                </el-form-item>
            </el-form>

            <!-- 搜索页面 -->
            <div class="search" v-show="activeIndex == 'tag_search'">
                <div class="row">
                    <el-input v-model="search_keyword" @keyup.enter.native="search" placeholder="请输入词条名"></el-input>
                    <el-button type="primary" icon="el-icon-search" @click="search"></el-button>
                </div>
                <el-table @row-click="getRow" :data="search_res" class="searchTable" border fit style="width: 100%">
                    <el-table-column prop="name" label="词条名"></el-table-column>
                    <el-table-column prop="t_name" label="词条译名"></el-table-column>
                    <el-table-column prop="desc" label="描述说明"></el-table-column>
                    <el-table-column prop="remark" label="备注"></el-table-column>
                    <el-table-column prop="contributor" label="贡献者"></el-table-column>
                    <el-table-column prop="c_name" label="分类名"></el-table-column>
                    <el-table-column prop="nsfw" label="是否工作场所不宜"></el-table-column>
                    <el-table-column prop="opration" label="操作">
                        <template>
                            <el-button size="mini" type="primary" style="margin: 0 1px" @click="toDonate" plain>贡献
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>

            <!-- 贡献榜 -->
            <div class="contributor" v-show="activeIndex == 'contributor'">
                <p>词条贡献榜(每小时更新一次)</p>
                <el-table :data="contributor_toplist" class="searchTable" border fit style="width: 100%"
                    :default-sort="{ prop: 'cnt', order: 'descending' }">
                    <el-table-column prop="name" label="贡献者"></el-table-column>
                    <el-table-column prop="cnt" label="贡献词条数" sortable></el-table-column>
                </el-table>
            </div>

            <!-- 共享计划 -->
            <div class="share" v-show="activeIndex == 'share'">
                <p>NovelAI词条贡献站 - 数据开放平台 根据 <a href="https://www.bilibili.com/read/cv19252957"
                        target="_blank">NovelAI信息并联计划公约</a> 约定：</p>
                <p>
                    贡献站所有词条数据资源来源于用户/网络搜集，免费服务于所有用户，任何个人/团队均可免费使用本站资源于任何 <strong style="color:#e55;">非商用/盈利目的</strong>
                    项目<br />
                    您只需要联系本站开发团队任意成员，提供 "任意联系方式", "应用名" 即可免费获取本站的数据源访问token，用于您的开发项目中
                </p>
                <p>本站提供接口详见 <a
                        href="https://console-docs.apipost.cn/preview/dbc3a0be7aff05cb/526a9c13fe093c2c?target_id=632986c9-4ce6-4b50-b6b8-409e41be0c4b">接口文档</a>
                </p>
                <p>本站交流群：660612010</p>
                <p>PS:由于开发任务繁重、人手有限，页面样式未有充足时间进行美化，如果您有一技之长希望加入我们，欢迎加入交流群共议</p>
            </div>
        </div>
    </div>
</template>

<script>
import categorySelector from '@/components/categorySelector.vue'
export default {
    name: 'Home',
    data() {
        return {
            // serverhost: 'www.morangames.xyz:3090',
            // serverhost: '127.0.0.1:3090',
            activeIndex: 'tag',
            form: {
                id: '',
                name: '',
                t_name: '',
                c_id: '',
                c_name: '',
                is_nsfw: false,
                desc: '',
                remarks: '',
                contributor: '',
            },
            categories: [],
            activeNames: ['1'],
            up_cnt: '获取中...',
            ct_total: '获取中...',
            search_keyword: '',
            search_res: [],
            contributor_toplist: [],
        }
    },
    methods: {
        // 提交tag
        onSubmit() {
            console.log('submit!');
            console.log(this.form)
            let _this = this
            // 获取categories列表
            this.$http({
                method: 'POST',
                url: `${_this.$store.state.serverhost}/update_taginfo`,
                data: _this.form,
            })
                .then((res) => {
                    if (res.data.code == 200) {
                        _this.$message({ type: 'success', message: res.data.msg, duration: 2000 })
                    } else {
                        _this.$message({ type: 'error', message: res.data.msg, duration: 2000 })
                    }
                })
                .catch((err) => {
                    _this.$message({ type: 'error', message: '请求后端服务器发生错误', duration: 2000 })
                })
        },
        // 获取随机tag
        roll_tag() {
            this.$message({ type: 'info', message: '正在获取随机tag', duration: 1000 })
            let _this = this
            // 获取categories列表
            this.$http({
                method: 'GET',
                url: `${_this.$store.state.serverhost}/get_random_tag`,
            })
                .then((res) => {
                    if (res.data.code == 200) {
                        _this.$message({ type: 'success', message: res.data.msg, duration: 2000 })
                        console.log(res.data)
                        _this.form.id = res.data.data.id
                        _this.form.c_id = res.data.data.c_id
                        _this.form.is_nsfw = res.data.data.is_nsfw ? true : false
                        _this.form.name = res.data.data.name
                        _this.form.t_name = res.data.data.t_name
                        _this.form.desc = res.data.data.desc ? res.data.data.desc : ''
                        _this.form.remarks = res.data.data.remarks ? res.data.data.remarks : ''

                        _this.categories.forEach((v) => {
                            if (v.id == res.data.data.c_id) {
                                _this.form.c_name = v.name
                            }
                        })
                    } else {
                        _this.$message({ type: 'error', message: res.data.msg, duration: 2000 })
                    }
                })
                .catch((err) => {
                    _this.$message({ type: 'error', message: '请求后端服务器发生错误', duration: 2000 })
                })
        },
        // 搜索tag
        search() {
            let _this = this
            // 获取categories列表
            this.$http({
                method: 'POST',
                url: `${_this.$store.state.serverhost}/search_tags`,
                data: {
                    keyword: _this.search_keyword
                }
            })
                .then((res) => {
                    if (res.data.code == 200) {
                        // console.log(res.data)
                        if (res.data.data.length > 0) {
                            for (let i = 0; i < res.data.data.length;i++){
                                let curId = parseInt(res.data.data[i].c_id),l1name="";
                                _this.$store.state.categories.l1.forEach(elem=>{
                                    if (elem.id == parseInt(curId / 100)) l1name=elem.name;
                                })
                                if (_this.$store.state.categories.l2[parseInt(curId/100)]!==undefined){
                                    _this.$store.state.categories.l2[parseInt(curId/100)].forEach(elem=>{
                                        if(elem.id == curId){
                                            res.data.data[i].c_name = l1name +">"+elem.name;
                                        }
                                    })
                                }
                            }
                            _this.search_res = res.data.data
                        } else {
                            _this.$message({ type: 'info', message: '查无相关数据', duration: 2000 })
                            _this.search_res = []
                        }

                    } else {
                        _this.$message({ type: 'error', message: res.data.msg, duration: 2000 })
                    }
                })
                .catch((err) => {
                    _this.$message({ type: 'error', message: '请求后端服务器发生错误', duration: 2000 })
                })
        },
        // 切换分页
        handleSelect(key, keyPath) {
            console.log(key, keyPath);
            this.activeIndex = keyPath[0]
        },
        // 切换分类选项
        categoryHandleSelect(item) {
            console.log(item);
            this.form.c_id = item.id
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
                    _this.ct_total = res.data.ct_total
                    // _this.$store.commit('setCategories', _this.categories)
                    _this.roll_tag()
                    let cd = res.data.contributor
                    let nlist = []
                    for (let key in cd) {
                        // console.log(key,obj[key])
                        nlist.push({ name: key, cnt: cd[key] })
                    }
                    _this.contributor_toplist = nlist;
                    //TODO:该函数为过渡方案，等待替换
                    _this.get_categories_full();
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        //获取完整的分类列表
        //TODO:该函数为过渡方案，等待替换
        get_categories_full(){
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
        // 复制成功时的回调函数
        onCopy(e) {
            this.$message.success("词条名已复制到剪切板！")
        },
        // 复制失败时的回调函数
        onError(e) {
            this.$message.error("抱歉，复制失败！")
        },
        // 获取行信息
        getRow(row) {
            this.selRowData = JSON.parse(JSON.stringify(row))
        },
        // 点击贡献
        toDonate() {
            let _this = this
            setTimeout(() => {
                _this.form.id = _this.selRowData.id
                _this.form.name = _this.selRowData.name
                _this.form.t_name = _this.selRowData.t_name
                _this.form.c_id = _this.selRowData.c_id
                _this.form.c_name = _this.selRowData.c_name
                _this.form.is_nsfw = _this.selRowData.is_nfsw ? true : false
                _this.form.desc = _this.selRowData.desc
                _this.form.remarks = _this.selRowData.remarks
                _this.form.contributor = _this.selRowData.contributor
                _this.activeIndex = 'tag'
            }, 50);

        }
    },
    mounted() {
        this.get_categories()
    }, components: {
        categorySelector
    }
}
</script>

<style lang="scss" scoped>
.home {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;

    .collapse {
        box-sizing: border-box;
        padding: 0 28px;
        width: 100%;
    }

    .board {
        margin-top: 5px;
    }

    .menu {
        width: 100%;
    }

    .container {
        box-sizing: border-box;
        padding: 16px;
        width: 100%;

        .row {
            width: 100%;
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            margin: 5px 0;

            .el-button {
                margin-left: 4px;
            }
        }

        .nsfw-span {
            margin: 0px 8px;
            color: #888;
            transition: all ease 0.5s;
        }

        .search {
            width: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            .searchTable {
                flex: 1;
                height: 60vh;
            }
        }
    }
}
</style>