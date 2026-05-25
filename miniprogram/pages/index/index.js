// pages/index/index.js
const app = getApp()

Page({
  data: {
    // 页面数据
  },

  onLoad() {
    // 页面加载时执行
  },

  onShow() {
    // 页面显示时执行
  },

  // 跳转到命盘录入
  goToChartInput() {
    wx.switchTab({
      url: '/pages/chart-input/chart-input'
    })
  },

  // 跳转到命盘查看
  goToChartView() {
    wx.switchTab({
      url: '/pages/chart-view/chart-view'
    })
  },

  // 跳转到推演仿真
  goToSimulation() {
    wx.switchTab({
      url: '/pages/simulation/simulation'
    })
  },

  // 跳转到关系分析
  goToRelation() {
    wx.switchTab({
      url: '/pages/relation/relation'
    })
  },

  // 跳转到风水分析（非 tabBar 页面，使用 navigateTo）
  goToFengshui() {
    wx.navigateTo({
      url: '/pages/fengshui/fengshui'
    })
  }
})
