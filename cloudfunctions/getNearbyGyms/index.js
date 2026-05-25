// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

const db = cloud.database()

// 获取附近健身房
exports.main = async (event, context) => {
  const { latitude, longitude, radius = 5000 } = event

  try {
    // 计算范围
    const latDelta = radius / 111000 // 纬度1度约111km
    const lngDelta = radius / (111000 * Math.cos(latitude * Math.PI / 180))

    // 查询附近健身房
    const res = await db.collection('gyms')
      .where({
        'location.latitude': db.command.gte(latitude - latDelta).and(db.command.lte(latitude + latDelta)),
        'location.longitude': db.command.gte(longitude - lngDelta).and(db.command.lte(longitude + lngDelta))
      })
      .get()

    // 计算距离并排序
    const gyms = res.data.map(gym => {
      const distance = calculateDistance(latitude, longitude, gym.location.latitude, gym.location.longitude)
      return {
        ...gym,
        distance: formatDistance(distance)
      }
    }).sort((a, b) => parseFloat(a.distance) - parseFloat(b.distance))

    return {
      success: true,
      gyms: gyms.slice(0, 20) // 返回最近20家
    }
  } catch (error) {
    console.error('查询失败:', error)
    return {
      success: false,
      gyms: []
    }
  }
}

// 计算两点间距离（Haversine公式）
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371000 // 地球半径（米）
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

function toRad(deg) {
  return deg * Math.PI / 180
}

function formatDistance(distance) {
  if (distance < 1000) {
    return Math.round(distance) + 'm'
  } else {
    return (distance / 1000).toFixed(1) + 'km'
  }
}
