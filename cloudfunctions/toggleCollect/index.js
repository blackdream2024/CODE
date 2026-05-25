// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

const db = cloud.database()

// 收藏/取消收藏
exports.main = async (event, context) => {
  const { gymId, gymName, action } = event
  const wxContext = cloud.getWXContext()
  const openid = wxContext.OPENID

  try {
    if (action === 'add') {
      // 添加收藏
      await db.collection('collections').add({
        data: {
          openid,
          gymId,
          gymName,
          createTime: db.serverDate()
        }
      })
      return { success: true }
    } else if (action === 'remove') {
      // 取消收藏
      await db.collection('collections')
        .where({ openid, gymId })
        .remove()
      return { success: true }
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
    return { success: false }
  }
}
