# 石家庄健身房查找小程序

一个帮助石家庄用户查找附近健身房、对比设施服务、找到最优套餐的微信小程序。

## 功能特性

### 核心功能
- 📍 **位置定位**：自动定位用户位置，查找附近5公里内的健身房
- 🏋️ **健身房列表**：展示附近健身房信息（名称、地址、距离、评分、价格）
- 🗺️ **地图视图**：在地图上查看健身房分布
- 🔍 **搜索功能**：支持按健身房名称或地址搜索
- 📊 **详情展示**：查看健身房详细信息
  - 套餐对比（价格、折扣、权益）
  - 设施服务（有氧区、力量区、瑜伽房、游泳池等）
  - 用户评价
- ⭐ **收藏功能**：收藏喜欢的健身房
- 📞 **联系咨询**：一键拨打电话
- 🧭 **导航功能**：导航到健身房

### 设计风格
- **精致奢华风格**：深海军蓝 + 金色配色方案
- **思源字体**：宋体标题 + 黑体正文
- **非对称布局**：创新的设计语言
- **专业图标**：使用 Icons8 专业图标库

## 技术栈

### 前端
- 微信小程序原生框架
- WXML / WXSS / JavaScript
- CloudBase SDK

### 后端
- CloudBase 云开发
- 云函数（Node.js）
- NoSQL 数据库

## 项目结构

```
Claw/
├── miniprogram/          # 小程序前端代码
│   ├── pages/           # 页面
│   │   ├── index/       # 首页（附近健身房）
│   │   ├── detail/      # 详情页
│   │   ├── search/      # 搜索页
│   │   └── profile/     # 个人中心
│   ├── images/          # 图片资源
│   ├── app.js           # 小程序入口
│   ├── app.json         # 全局配置
│   ├── app.wxss         # 全局样式
│   └── sitemap.json     # 站点地图
├── cloudfunctions/      # 云函数
│   ├── getNearbyGyms/   # 获取附近健身房
│   ├── getGymDetail/    # 获取健身房详情
│   ├── searchGyms/      # 搜索健身房
│   ├── toggleCollect/   # 收藏/取消收藏
│   ├── getCollections/  # 获取收藏列表
│   ├── checkCollected/  # 检查是否已收藏
│   └── initDatabase/    # 初始化数据库
├── config/              # 配置文件
│   └── .agent/          # AI 助手配置
├── project.config.json  # 项目配置
└── README.md            # 项目说明
```

## 数据库设计

### gyms 集合（健身房数据）
```javascript
{
  _id: "健身房ID",
  name: "健身房名称",
  address: "地址",
  phone: "电话",
  rating: 4.8,          // 评分
  reviewCount: 328,     // 评价数
  hours: "06:00-22:00", // 营业时间
  description: "描述",
  image: "图片URL",
  location: {           // 位置坐标
    latitude: 38.045,
    longitude: 114.515
  },
  facilities: [         // 设施列表
    { name: "有氧区", icon: "图标URL", available: true },
    // ...
  ],
  packages: [           // 套餐列表
    {
      name: "月卡",
      price: 399,
      originalPrice: 599,
      discount: "6.7折",
      benefits: ["权益1", "权益2"],
      recommend: false
    },
    // ...
  ],
  reviews: [            // 评价列表
    {
      user: "用户名",
      avatar: "头像URL",
      rating: 5,
      date: "2024-01-15",
      content: "评价内容"
    }
  ]
}
```

### collections 集合（收藏数据）
```javascript
{
  _id: "收藏ID",
  openid: "用户openid",
  gymId: "健身房ID",
  gymName: "健身房名称",
  createTime: Date
}
```

## 快速开始

### 1. 准备工作
- 安装微信开发者工具
- 申请微信小程序 AppID
- 创建 CloudBase 环境（已完成：test-1985-4gn0smgye6208976）

### 2. 配置项目
1. 打开 `project.config.json`
2. 修改 `appid` 为你的小程序 AppID
3. 修改 `env` 为你的 CloudBase 环境ID

### 3. 打开项目
1. 打开微信开发者工具
2. 导入项目，选择项目根目录
3. 点击「编译」预览

### 4. 初始化数据库
1. 在微信开发者工具中，右键 `cloudfunctions/initDatabase`
2. 选择「上传并部署：云端安装依赖」
3. 部署完成后，在云端测试调用 `initDatabase` 函数
4. 数据库将自动创建并填充石家庄健身房数据

### 5. 部署云函数
依次上传并部署以下云函数：
- getNearbyGyms
- getGymDetail
- searchGyms
- toggleCollect
- getCollections
- checkCollected

## 主要功能实现

### 1. 附近健身房查找
使用 Haversine 公式计算两点间距离，按距离排序返回最近20家健身房。

### 2. 套餐对比
自动标记"最优惠"套餐（最高折扣），展示价格对比和权益差异。

### 3. 设施服务对比
以网格形式展示设施，已开放/未开放状态清晰区分。

### 4. 收藏功能
基于用户 openid 的收藏管理，支持收藏、取消收藏、查询收藏列表。

## API 接口

### 云函数接口

#### getNearbyGyms
获取附近健身房
```javascript
{
  latitude: 38.0422,
  longitude: 114.5096,
  radius: 5000  // 搜索半径（米）
}
```

#### getGymDetail
获取健身房详情
```javascript
{
  id: "健身房ID"
}
```

#### searchGyms
搜索健身房
```javascript
{
  keyword: "金仕堡"
}
```

#### toggleCollect
收藏/取消收藏
```javascript
{
  gymId: "健身房ID",
  gymName: "健身房名称",
  action: "add" | "remove"
}
```

## CloudBase 控制台

- 概览：https://tcb.cloud.tencent.com/dev?envId=test-1985-4gn0smgye6208976#/overview
- 文档数据库：https://tcb.cloud.tencent.com/dev?envId=test-1985-4gn0smgye6208976#/db/doc
- 云函数：https://tcb.cloud.tencent.com/dev?envId=test-1985-4gn0smgye6208976#/scf

## 注意事项

1. **小程序 AppID**：需要在 `project.config.json` 中配置你的小程序 AppID
2. **CloudBase 环境**：确保环境ID正确，已在 `app.js` 中配置
3. **云函数权限**：确保云函数有正确的权限配置
4. **位置权限**：用户需要授权位置权限才能使用定位功能
5. **图标资源**：使用 Icons8 在线图标，建议下载到本地

## 后续优化方向

- [ ] 添加用户评价功能
- [ ] 实现套餐购买流程
- [ ] 添加优惠券系统
- [ ] 支持多城市切换
- [ ] 增加健身数据统计
- [ ] 添加社交分享功能
- [ ] 实现实时消息通知
- [ ] 优化搜索算法

## License

MIT License
