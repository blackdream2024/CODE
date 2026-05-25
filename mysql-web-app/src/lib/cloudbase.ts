import cloudbase from "@cloudbase/js-sdk";

// CloudBase 环境 ID
const ENV_ID = "cloud1-d5g6qt1jnd898a536";

// 初始化 CloudBase 应用
const app = cloudbase.init({
  env: ENV_ID,
});

// 获取认证实例
export const auth = app.auth();

// 获取关系型数据库实例
export const db = app.rdb();

// 导出应用实例
export { app, ENV_ID };
