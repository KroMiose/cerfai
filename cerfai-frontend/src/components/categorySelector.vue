<template>
    <div>
        <el-cascader placeholder="点击展开选择分类" :value="value" :options="options" filterable
            v-on:change="valueChanged" separator=">"></el-cascader>
    </div>
</template>
<script>
export default {
    props: ['value'],
    emits: ['change'],
    data() {
        return {
        }
    },
    computed: {
        options() {
            let opt = [], categoriesList = this.$store.state.categories;
            if (!categoriesList || !categoriesList.l1) return [];
            categoriesList.l1.forEach(element => {
                let l1Category = {
                    label: element.name,
                    value: element.id,
                    children: []
                }
                if (categoriesList.l2[element.id] !== undefined) {
                    categoriesList.l2[element.id].forEach(element => {
                        l1Category.children.push({
                            label: element.name,
                            value: element.id
                        })
                    })
                }

                opt.push(l1Category);
            });
            return opt;
        }
    }, methods: {
        valueChanged(val) {
            //TODO:找时间研究明白v-model语法，现在先将就一下（）
            val = val[val.length - 1]
            this.$emit('change', val);
        }
    }
}
</script>