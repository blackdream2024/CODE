// pages/simulation/simulation.js
const app = getApp()

Page({
  data: {
    // 命盘列表
    charts: [],
    chartNames: [],
    selectedChartIndex: 0,
    
    // 推演配置
    scenarioOptions: ['事业推演', '婚姻推演', '合作推演', '搬迁推演', '投资推演', '健康推演', '学习推演'],
    scenarioValues: ['career', 'marriage', 'cooperation', 'relocation', 'investment', 'health', 'learning'],
    scenarioIndex: 0,
    startDate: '',
    steps: 12,
    samples: 50,
    
    // 推演状态
    isSimulating: false,
    isFormValid: false,
    
    // 推演结果
    simulationResult: null
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

  // 选择命盘
  onChartSelect(e) {
    this.setData({ selectedChartIndex: e.detail.value })
    this.validateForm()
  },

  // 选择推演场景
  onScenarioChange(e) {
    this.setData({ scenarioIndex: e.detail.value })
  },

  // 选择起始日期
  onStartDateChange(e) {
    this.setData({ startDate: e.detail.value })
    this.validateForm()
  },

  // 输入仿真步数
  onStepsInput(e) {
    this.setData({ steps: parseInt(e.detail.value) || 12 })
  },

  // 输入采样次数
  onSamplesInput(e) {
    this.setData({ samples: parseInt(e.detail.value) || 50 })
  },

  // 表单验证
  validateForm() {
    const { charts, selectedChartIndex, startDate } = this.data
    const isFormValid = charts.length > 0 && startDate !== ''
    this.setData({ isFormValid })
  },

  // 格式化推演结果数据
  formatResult(data) {
    if (!data) return data
    
    // 格式化风险分析中的百分比
    if (data.risk_analysis && data.risk_analysis.overall_risk_score !== undefined) {
      data.risk_analysis.risk_score_percent = Math.round(data.risk_analysis.overall_risk_score * 100) + '%'
    }
    
    return data
  },

  // 开始推演
  onSimulate() {
    if (!this.data.isFormValid || this.data.isSimulating) return
    
    const { charts, selectedChartIndex, scenarioIndex, scenarioValues, startDate, steps, samples } = this.data
    const selectedChart = charts[selectedChartIndex]
    
    if (!selectedChart) {
      wx.showToast({
        title: '请选择命盘',
        icon: 'none'
      })
      return
    }
    
    this.setData({ isSimulating: true })
    
    // 调用后端API进行推演
    const apiUrl = app.globalData.apiBaseUrl + '/api/simulate'
    
    wx.request({
      url: apiUrl,
      method: 'POST',
      data: {
        agents: [{
          name: selectedChart.name,
          birth_date: selectedChart.birth_date,
          birth_time: selectedChart.birth_time,
          gender: selectedChart.gender
        }],
        scenario: scenarioValues[scenarioIndex],
        steps: steps,
        samples: samples,
        start_year: parseInt(startDate.split('-')[0]),
        start_month: parseInt(startDate.split('-')[1])
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // 预处理数据，格式化百分比等
          const result = this.formatResult(res.data)
          this.setData({
            simulationResult: result,
            isSimulating: false
          })
          
          wx.showToast({
            title: '推演完成',
            icon: 'success'
          })
        } else {
          wx.showToast({
            title: '推演失败',
            icon: 'none'
          })
          this.setData({ isSimulating: false })
        }
      },
      fail: (err) => {
        console.error('推演失败:', err)
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        })
        this.setData({ isSimulating: false })
      }
    })
  }
})
