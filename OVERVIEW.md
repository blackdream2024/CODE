# 石家庄健身房查找小程序 - 项目概览

## 📱 项目信息

**项目名称**：石家庄健身房查找小程序  
**项目类型**：微信小程序  
**开发环境**：CloudBase 云开发  
**完成日期**：2026年3月17日

---

## ✨ 项目特点

### 核心功能
1. **智能定位**：自动获取用户位置，查找附近健身房
2. **套餐对比**：自动对比不同健身房套餐价格和权益
3. **设施对比**：可视化展示各健身房设施和服务
4. **最优推荐**：智能推荐最优惠的套餐
5. **收藏管理**：支持收藏喜欢的健身房

### 设计亮点
- **精致奢华风格**：深海军蓝(#1E3A5F) + 金色(#C9A961)配色
- **思源字体**：宋体标题 + 黑体正文，提升品质感
- **非对称布局**：打破常规，创造视觉层次
- **专业图标**：使用 Icons8 专业图标库

---

## 📂 项目结构

```
Claw/
├── miniprogram/              # 小程序前端
│   ├── pages/
│   │   ├── index/           # 首页（附近健身房 + 地图）
│   │   ├── detail/          # 详情页（套餐对比 + 设施服务）
│   │   ├── search/          # 搜索页（热门搜索 + 历史记录）
│   │   └── profile/         # 个人中心（收藏管理）
│   ├── images/tabbar/       # 底部导航图标
│   ├── app.js               # 小程序入口
│   ├── app.json             # 全局配置
│   └── app.wxss             # 全局样式
├── cloudfunctions/           # 云函数
│   ├── getNearbyGyms/       # 获取附近健身房（含距离计算）
│   ├── getGymDetail/        # 获取健身房详情
│   ├── searchGyms/          # 搜索健身房
│   ├── toggleCollect/       # 收藏/取消收藏
│   ├── getCollections/      # 获取收藏列表
│   ├── checkCollected/      # 检查是否已收藏
│   └── initDatabase/        # 初始化数据库（含4家健身房数据）
├── config/                   # 配置文件
│   └── .agent/rules/         # AI 助手规则
├── project.config.json       # 项目配置
└── README.md                 # 项目文档
```

---

## 🗄️ 数据库设计

### gyms 集合（健身房）
- 基本信息：名称、地址、电话、评分、营业时间
- 位置坐标：latitude, longitude
- 设施列表：有氧区、力量区、瑜伽房、游泳池等
- 套餐列表：月卡、季卡、年卡（含价格、折扣、权益）
- 用户评价：用户名、头像、评分、内容

### collections 集合（收藏）
- 用户 openid
- 健身房 ID 和名称
- 收藏时间

---

## 🚀 快速开始

### 1. 配置小程序
```bash
# 修改 project.config.json
"appid": "你的小程序AppID"
```

### 2. 配置 CloudBase
```javascript
// 已在 app.js 中配置
wx.cloud.init({
  env: 'test-1985-4gn0smgye6208976'
})
```

### 3. 初始化数据库
1. 在微信开发者工具中上传 `initDatabase` 云函数
2. 调用云函数初始化数据
3. 自动创建 gyms 和 collections 集合

### 4. 部署云函数
依次部署以下云函数：
- getNearbyGyms
- getGymDetail
- searchGyms
- toggleCollect
- getCollections
- checkCollected

---

## 📊 功能演示

### 首页（附近健身房）
- 显示用户当前位置
- 列表展示附近健身房（含距离、评分、价格）
- 地图视图查看分布
- 一键导航

### 详情页（套餐对比）
- 套餐价格对比（原价、现价、折扣）
- 权益列表展示
- 最优惠套餐标记
- 设施服务对比
- 用户评价查看

### 搜索页
- 热门搜索词
- 搜索历史记录
- 模糊搜索支持

### 个人中心
- 收藏列表管理
- 一键取消收藏
- 关于我们
- 联系客服

---

## 🎨 设计规范

```
配色方案：
- 主色：#1E3A5F（深海军蓝）
- 强调色：#C9A961（金色）
- 背景色：#F8F4EF（米白色）
- 文字：#2C3E50（深灰）
- 成功：#27AE60（绿色）

字体方案：
- 标题：Noto Serif SC（思源宋体）
- 正文：Noto Sans SC（思源黑体）

布局策略：
- 非对称卡片布局
- 左上角突出核心信息
- 带有重叠效果的价格标签
- 渐进式信息展示
```

---

## 🔧 技术实现

### 距离计算
使用 Haversine 公式计算两点间距离：
```javascript
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371000; // 地球半径（米）
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}
```

### 套餐对比算法
自动计算折扣率，标记最优惠套餐：
```javascript
discount = (price / originalPrice * 10).toFixed(1) + "折"
```

---

## 📝 已完成功能清单

- ✅ 小程序项目结构搭建
- ✅ 首页（附近健身房列表 + 地图）
- ✅ 详情页（套餐对比 + 设施服务 + 用户评价）
- ✅ 搜索页（热门搜索 + 历史记录）
- ✅ 个人中心（收藏管理）
- ✅ CloudBase 数据库集成
- ✅ 云函数开发（7个云函数）
- ✅ 位置定位功能
- ✅ 距离计算与排序
- ✅ 收藏/取消收藏功能
- ✅ 搜索筛选功能
- ✅ 一键拨打电话
- ✅ 导航功能
- ✅ 底部导航栏
- ✅ 精致 UI 设计
- ✅ 图标资源下载

---

## 🎯 CloudBase 控制台

- **概览**：https://tcb.cloud.tencent.com/dev?envId=test-1985-4gn0smgye6208976#/overview
- **文档数据库**：https://tcb.cloud.tencent.com/dev?envId=test-1985-4gn0smgye6208976#/db/doc
- **云函数**：https://tcb.cloud.tencent.com/dev?envId=test-1985-4gn0smgye6208976#/scf

---

## 💡 后续优化建议

1. **用户体验优化**
   - 添加骨架屏加载动画
   - 优化图片懒加载
   - 增加下拉刷新

2. **功能扩展**
   - 添加用户评价功能
   - 实现套餐购买流程
   - 添加优惠券系统
   - 支持多城市切换

3. **数据分析**
   - 添加健身数据统计
   - 用户行为分析
   - 热门健身房排行

4. **社交功能**
   - 添加社交分享
   - 健身打卡功能
   - 健身社区

---

## 📞 技术支持

如遇到问题，请检查：
1. CloudBase 环境是否正确
2. 云函数是否已部署
3. 数据库是否已初始化
4. 小程序 AppID 是否配置

---

**项目状态**：✅ 已完成，可部署使用
