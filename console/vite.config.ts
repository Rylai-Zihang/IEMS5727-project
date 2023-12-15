import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path"; // 添加这行导入语句

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "/console/",
  resolve: {
    alias: [
      // 配置 @ 指代 src
      {
        find: "@",
        replacement: resolve(__dirname, "./src"),
      },
    ],
  },
  server: {
    // 开启热更新
    hmr: true,
  },
});
