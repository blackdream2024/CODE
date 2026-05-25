// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

const db = cloud.database()

// 获取健身房详情
exports.main = async (event, context) => {
  const { id } = event

  try {
    const res = await db.collection('gyms')
      .doc(id)
      .get()

    return {
      success: true,
      gym: res.data
    }
  } catch (error) {
    console.error('获取详情失败:', error)
    return {
      success: false,
      gym: null
    }
  }
}
