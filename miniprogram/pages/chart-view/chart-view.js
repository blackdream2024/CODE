// pages/chart-view/chart-view.js
const app = getApp()

Page({
  data: {
    // 命盘列表
    charts: [],
    chartNames: [],
    selectedChartIndex: 0,
    selectedChart: null,
    
    // 八字数据
    baziData: {
      year: '',
      month: '',
      day: '',
      hour: ''
    },
    
    // 五行数据
    wuxingData: [],
    
    // 十神数据
    shishenData: []
  },

  onLoad() {
    // 页面加载时执行
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
    
    if (charts.length > 0) {
      this.selectChart(0)
    }
  },

  // 选择命盘
  onChartSelect(e) {
    const index = e.detail.value
    this.selectChart(index)
  },

  // 选择命盘并加载数据
  selectChart(index) {
    const selectedChart = this.data.charts[index]
    
    if (!selectedChart) return
    
    this.setData({
      selectedChartIndex: index,
      selectedChart
    })
    
    // 加载八字数据
    this.loadBaziData(selectedChart)
    
    // 加载五行数据
    this.loadWuxingData(selectedChart)
    
    // 加载十神数据
    this.loadShishenData(selectedChart)
  },

  // 加载八字数据
  loadBaziData(chart) {
    // 这里应该调用后端API获取八字数据
    // 目前使用模拟数据
    const baziData = {
      year: '甲子',
      month: '乙丑',
      day: '丙寅',
      hour: '丁卯'
    }
    
    this.setData({ baziData })
  },

  // 加载五行数据
  loadWuxingData(chart) {
    // 这里应该调用后端API获取五行数据
    // 目前使用模拟数据
    const wuxingData = [
      { element: '金', strength: 20 },
      { element: '木', strength: 25 },
      { element: '水', strength: 15 },
      { element: '火', strength: 20 },
      { element: '土', strength: 20 }
    ]
    
    this.setData({ wuxingData })
  },

  // 加载十神数据
  loadShishenData(chart) {
    // 这里应该调用后端API获取十神数据
    // 目前使用模拟数据
    const shishenData = [
      { name: '比肩', value: '甲' },
      { name: '劫财', value: '乙' },
      { name: '食神', value: '丙' },
      { name: '伤官', value: '丁' },
      { name: '偏财', value: '戊' },
      { name: '正财', value: '己' },
      { name: '七杀', value: '庚' },
      { name: '正官', value: '辛' },
      { name: '偏印', value: '壬' },
      { name: '正印', value: '癸' }
    ]
    
    this.setData({ shishenData })
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

  // 跳转到命盘录入
  goToChartInput() {
    wx.switchTab({
      url: '/pages/chart-input/chart-input'
    })
  }
})
