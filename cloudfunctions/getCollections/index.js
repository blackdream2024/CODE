// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

const db = cloud.database()

// 获取收藏列表
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  const openid = wxContext.OPENID

  try {
    const res = await db.collection('collections')
      .where({ openid })
      .orderBy('createTime', 'desc')
      .get()

    return {
      success: true,
      collections: res.data
    }
  } catch (error) {
    console.error('获取收藏失败:', error)
    return {
      success: true,
      collections: []
    }
  }
}
