// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

const db = cloud.database()

// 检查是否已收藏
exports.main = async (event, context) => {
  const { gymId } = event
  const wxContext = cloud.getWXContext()
  const openid = wxContext.OPENID

  try {
    const res = await db.collection('collections')
      .where({ openid, gymId })
      .count()

    return {
      success: true,
      collected: res.total > 0
    }
  } catch (error) {
    console.error('检查收藏失败:', error)
    return {
      success: true,
      collected: false
    }
  }
}
