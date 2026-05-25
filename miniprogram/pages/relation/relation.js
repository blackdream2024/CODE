// pages/relation/relation.js
const app = getApp()

Page({
  data: {
    // 命盘列表
    charts: [],
    chartNames: [],
    person1Index: 0,
    person2Index: 0,
    
    // 分析配置
    startDate: '',
    
    // 分析状态
    isAnalyzing: false,
    isFormValid: false,
    
    // 分析结果
    analysisResult: null
  },

  onLoad() {
    // 页面加载时执行
    this.loadCharts()
  },

  onShow() {
    // 页面显示时执行
    this.loadCharts()
  },

  // 加载命盘列表
  loadCharts() {
    const charts = wx.getStorageSync('charts') || []
    const chartNames = charts.map(chart => chart.name)
    
    this.setData({ 
      charts,
      chartNames
    })
    
    this.validateForm()
  },

  // 选择第一个人
  onPerson1Select(e) {
    this.setData({ person1Index: e.detail.value })
    this.validateForm()
  },

  // 选择第二个人
  onPerson2Select(e) {
    this.setData({ person2Index: e.detail.value })
    this.validateForm()
  },

  // 选择起始日期
  onStartDateChange(e) {
    this.setData({ startDate: e.detail.value })
    this.validateForm()
  },

  // 表单验证
  validateForm() {
    const { charts, person1Index, person2Index, startDate } = this.data
    const isFormValid = charts.length >= 2 && 
                        person1Index !== person2Index && 
                        startDate !== ''
    this.setData({ isFormValid })
  },

  // 开始分析
  onAnalyze() {
    if (!this.data.isFormValid || this.data.isAnalyzing) return
    
    const { charts, person1Index, person2Index, startDate } = this.data
    const person1 = charts[person1Index]
    const person2 = charts[person2Index]
    
    if (!person1 || !person2) {
      wx.showToast({
        title: '请选择两个命盘',
        icon: 'none'
      })
      return
    }
    
    if (person1Index === person2Index) {
      wx.showToast({
        title: '请选择不同的命盘',
        icon: 'none'
      })
      return
    }
    
    this.setData({ isAnalyzing: true })
    
    // 调用云函数进行分析
    wx.cloud.callHTTPFunction({
      name: 'mingpan-api',
      path: '/api/relation',
      method: 'POST',
      data: {
        person1: {
          name: person1.name,
          birth_date: person1.birth_date,
          birth_time: person1.birth_time,
          gender: person1.gender
        },
        person2: {
          name: person2.name,
          birth_date: person2.birth_date,
          birth_time: person2.birth_time,
          gender: person2.gender
        },
        start_year: parseInt(startDate.split('-')[0]),
        start_month: parseInt(startDate.split('-')[1])
      },
      success: (res) => {
        this.setData({
          analysisResult: res.result || res.data,
          isAnalyzing: false
        })
        
        wx.showToast({
          title: '分析完成',
          icon: 'success'
        })
      },
      fail: (err) => {
        console.error('分析失败:', err)
        wx.showToast({
          title: '分析失败，请重试',
          icon: 'none'
        })
        this.setData({ isAnalyzing: false })
      }
    })
  }
})
