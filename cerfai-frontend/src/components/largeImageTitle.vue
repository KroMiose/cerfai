<!--巨幕和轮播图组件-->
<template>
    <div class="large-image-title" :style="{ height: real_height,overflow:'hidden'}">
        <el-carousel :interval="5000" arrow="always" :height="real_height">
            <el-carousel-item v-for="item in items" :key="item">
                <div :style="{backgroundImage:'url('+item+')'}" class="cvImg"></div>
            </el-carousel-item>
        </el-carousel>
        <div class="text_layer" :style="{ bottom: real_height, height: 'calc(' + real_height + ' - 80px)'}">
            <slot></slot>
        </div>
    </div>
</template>
<script>
export default{
    props: ["items", "title","height"],
    data(){
        return{
            
        }
    },computed:{
        real_height(){
            return this.height+"px"
        }
    }
}
</script>
<style>
.large-image-title{
    background: rgb(59, 59, 59);
}
.text_layer{
    position: relative;
    left:100px;
    width: calc(100% - 200px);
    text-align: center;
    color:white;
    z-index: 10;
    padding:20px;
}
.el-carousel__item .cvImg {
    filter: brightness(0.6);
    width: 100%;
    height: 100%;
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
}
</style>