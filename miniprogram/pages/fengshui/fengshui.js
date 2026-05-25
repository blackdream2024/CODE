// pages/fengshui/fengshui.js
const app = getApp()

Page({
  data: {
    location: null,
    fengshuiData: null,
    analyzing: false
  },

  onLoad() {
    // 页面加载时获取位置信息
    this.getLocation()
  },

  // 获取位置信息
  getLocation() {
    wx.getLocation({
      type: 'gcj02',
      success: (res) => {
        const location = {
          latitude: res.latitude,
          longitude: res.longitude
        }
        
        // 获取地址信息
        this.getAddressInfo(location)
      },
      fail: (err) => {
        console.error('获取位置失败:', err)
        wx.showToast({
          title: '获取位置失败，请检查权限设置',
          icon: 'none'
        })
      }
    })
  },

  // 获取地址信息
  getAddressInfo(location) {
    wx.chooseLocation({
      success: (res) => {
        this.setData({
          location: {
            ...location,
            address: res.address,
            name: res.name
          }
        })
      },
      fail: () => {
        // 如果用户取消选择地址，只使用坐标
        this.setData({
          location: location
        })
      }
    })
  },

  // 开始风水分析
  analyzeFengshui() {
    if (!this.data.location) {
      wx.showToast({
        title: '请先获取位置信息',
        icon: 'none'
      })
      return
    }

    this.setData({
      analyzing: true
    })

    // 调用云函数进行风水分析
    wx.cloud.callHTTPFunction({
      name: 'mingpan-api',
      path: '/api/fengshui',
      method: 'POST',
      data: {
        location: this.data.location,
        timestamp: Date.now()
      },
      success: (res) => {
        this.setData({
          fengshuiData: res.result || res.data
        })
      },
      fail: (err) => {
        console.error('风水分析请求失败:', err)
        wx.showToast({
          title: '分析失败，请重试',
          icon: 'none'
        })
      },
      complete: () => {
        this.setData({
          analyzing: false
        })
      }
    })
  },

  // 分享功能
  onShareAppMessage() {
    return {
      title: '风水分析 - 命盘推演',
      path: '/pages/fengshui/fengshui'
    }
  }
})