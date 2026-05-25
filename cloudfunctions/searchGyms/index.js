// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

const db = cloud.database()
const _ = db.command

// 搜索健身房
exports.main = async (event, context) => {
  const { keyword } = event

  try {
    // 模糊搜索名称和地址
    const res = await db.collection('gyms')
      .where({
        $or: [
          { name: db.RegExp({ regexp: keyword, options: 'i' }) },
          { address: db.RegExp({ regexp: keyword, options: 'i' }) }
        ]
      })
      .get()

    return {
      success: true,
      gyms: res.data
    }
  } catch (error) {
    console.error('搜索失败:', error)
    return {
      success: false,
      gyms: []
    }
  }
}
