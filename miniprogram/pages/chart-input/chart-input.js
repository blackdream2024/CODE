// pages/chart-input/chart-input.js
const app = getApp()

Page({
  data: {
    // 表单数据
    name: '',
    genderIndex: 0,
    genderOptions: ['男', '女'],
    birthDate: '',
    birthTime: '',
    birthPlace: '',
    calendarIndex: 0,
    calendarOptions: ['公历', '农历'],
    
    // 已录入命盘列表
    charts: [],
    
    // 表单验证状态
    isFormValid: false
  },

  onLoad() {
    // 页面加载时执行
    this.loadCharts()
  },

  onShow() {
    // 页面显示时执行
    this.loadCharts()
  },

  // 加载已录入的命盘
  loadCharts() {
    const charts = wx.getStorageSync('charts') || []
    this.setData({ charts })
  },

  // 姓名输入
  onNameInput(e) {
    this.setData({ name: e.detail.value })
    this.validateForm()
  },

  // 性别选择
  onGenderChange(e) {
    this.setData({ genderIndex: e.detail.value })
    this.validateForm()
  },

  // 日期选择
  onDateChange(e) {
    this.setData({ birthDate: e.detail.value })
    this.validateForm()
  },

  // 时间选择
  onTimeChange(e) {
    this.setData({ birthTime: e.detail.value })
    this.validateForm()
  },

  // 出生地输入
  onPlaceInput(e) {
    this.setData({ birthPlace: e.detail.value })
    this.validateForm()
  },

  // 历法选择
  onCalendarChange(e) {
    this.setData({ calendarIndex: e.detail.value })
    this.validateForm()
  },

  // 表单验证
  validateForm() {
    const { name, birthDate, birthTime } = this.data
    const isFormValid = name.trim() !== '' && birthDate !== '' && birthTime !== ''
    this.setData({ isFormValid })
  },

  // 提交表单
  onSubmit() {
    if (!this.data.isFormValid) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      })
      return
    }

    const { name, genderIndex, genderOptions, birthDate, birthTime, birthPlace, calendarIndex, calendarOptions } = this.data
    
    // 创建新命盘
    const newChart = {
      id: Date.now().toString(),
      name: name.trim(),
      gender: genderOptions[genderIndex] === '男' ? 'male' : 'female',
      birth_date: birthDate,
      birth_time: birthTime,
      birth_place: birthPlace.trim(),
      calendar: calendarOptions[calendarIndex],
      created_at: new Date().toISOString()
    }

    // 保存到本地存储
    const charts = wx.getStorageSync('charts') || []
    charts.push(newChart)
    wx.setStorageSync('charts', charts)

    // 更新页面数据
    this.setData({ charts })
    
    // 清空表单
    this.setData({
      name: '',
      genderIndex: 0,
      birthDate: '',
      birthTime: '',
      birthPlace: '',
      calendarIndex: 0,
      isFormValid: false
    })

    wx.showToast({
      title: '命盘已保存',
      icon: 'success'
    })
  },

  // 查看命盘
  viewChart(e) {
    const id = e.currentTarget.dataset.id
    wx.switchTab({
      url: '/pages/chart-view/chart-view'
    })
  },

  // 删除命盘
  deleteChart(e) {
    const id = e.currentTarget.dataset.id
    
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这个命盘吗？',
      success: (res) => {
        if (res.confirm) {
          let charts = wx.getStorageSync('charts') || []
          charts = charts.filter(chart => chart.id !== id)
          wx.setStorageSync('charts', charts)
          
          this.setData({ charts })
          
          wx.showToast({
            title: '已删除',
            icon: 'success'
          })
        }
      }
    })
  }
})
