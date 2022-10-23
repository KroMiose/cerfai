const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
    transpileDependencies: true,
    lintOnSave: false,
    publicPath: "./",
    devServer: {
        proxy: {
            "/api": {
                target: "http://localhost:3090",
                changeOrigin: true,
                pathRewrite: {
                "^/api": "/api/",
                },
            },
        },
    },
});
