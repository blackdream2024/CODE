// app.js
App({
  onLaunch() {
    // 初始化云开发
    if (wx.cloud) {
      wx.cloud.init({
        env: 'test-1985-4gn0smgye6208976', // 云开发环境ID
        traceUser: true
      })
    }
    
    // 获取设备信息（使用新 API 替代已弃用的 getSystemInfoSync）
    try {
      const deviceInfo = wx.getDeviceInfo()
      const appBaseInfo = wx.getAppBaseInfo()
      
      this.globalData.deviceInfo = deviceInfo
      this.globalData.appBaseInfo = appBaseInfo
      
      // 判断是否为 iPhone X 系列（用于底部安全区域适配）
      const model = deviceInfo.model || ''
      this.globalData.isIphoneX = model.indexOf('iPhone X') >= 0 || 
                                   model.indexOf('iPhone 1') >= 0
    } catch (e) {
      console.warn('获取设备信息失败，使用兼容方案:', e)
      // 兼容旧版本
      const systemInfo = wx.getSystemInfoSync()
      this.globalData.deviceInfo = systemInfo
      this.globalData.isIphoneX = (systemInfo.model || '').indexOf('iPhone X') >= 0 || 
                                   (systemInfo.model || '').indexOf('iPhone 1') >= 0
    }
  },
  
  globalData: {
    deviceInfo: null,
    appBaseInfo: null,
    isIphoneX: false,
    userInfo: null,
    // API 基础地址（需要替换为你的后端地址）
    apiBaseUrl: 'http://localhost:8000'
  }
})
