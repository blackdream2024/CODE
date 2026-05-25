// 云函数：初始化数据库
const cloud = require('wx-server-sdk')

cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
})

const db = cloud.database()

// 初始化健身房数据
exports.main = async (event, context) => {
  try {
    // 删除旧数据
    await db.collection('gyms').where({}).remove()

    // 插入石家庄健身房数据
    const gyms = [
      {
        name: '石家庄金仕堡健身',
        address: '长安区中山东路289号',
        phone: '0311-87654321',
        rating: 4.8,
        reviewCount: 328,
        hours: '06:00-22:00',
        description: '金仕堡健身致力于为石家庄市民提供专业的健身服务，拥有国际先进的健身器材和资深的教练团队。馆内设有有氧区、力量区、瑜伽房、游泳池等多个功能区域。',
        image: 'https://img.icons8.com/ios-filled/100/1E3A5F/gym.png',
        location: { latitude: 38.045, longitude: 114.515 },
        facilities: [
          { name: '有氧区', icon: 'https://img.icons8.com/ios/100/1E3A5F/treadmill.png', available: true },
          { name: '力量区', icon: 'https://img.icons8.com/ios/100/1E3A5F/dumbbell.png', available: true },
          { name: '瑜伽房', icon: 'https://img.icons8.com/ios/100/1E3A5F/lotus-position.png', available: true },
          { name: '游泳池', icon: 'https://img.icons8.com/ios/100/1E3A5F/swimming-pool.png', available: true },
          { name: '私教区', icon: 'https://img.icons8.com/ios/100/1E3A5F/personal-trainer.png', available: true },
          { name: '动感单车', icon: 'https://img.icons8.com/ios/100/1E3A5F/bicycle.png', available: true },
          { name: '搏击区', icon: 'https://img.icons8.com/ios/100/1E3A5F/boxing-gloves.png', available: true },
          { name: '普拉提', icon: 'https://img.icons8.com/ios/100/1E3A5F/pilates.png', available: false }
        ],
        packages: [
          {
            name: '月卡',
            price: 399,
            originalPrice: 599,
            discount: '6.7折',
            benefits: ['无限次使用', '储物柜', '淋浴', '团课'],
            recommend: false
          },
          {
            name: '季卡',
            price: 999,
            originalPrice: 1599,
            discount: '6.2折',
            benefits: ['无限次使用', '储物柜', '淋浴', '团课', '私教2节'],
            recommend: false
          },
          {
            name: '年卡',
            price: 1999,
            originalPrice: 3999,
            discount: '5折',
            benefits: ['无限次使用', '储物柜', '淋浴', '团课', '私教12节', '游泳'],
            recommend: true
          }
        ],
        reviews: [
          {
            user: '健身达人小王',
            avatar: 'https://img.icons8.com/ios-filled/100/1E3A5F/user.png',
            rating: 5,
            date: '2024-01-15',
            content: '环境很好，器材齐全，教练也很专业！'
          },
          {
            user: '运动爱好者',
            avatar: 'https://img.icons8.com/ios-filled/100/1E3A5F/user.png',
            rating: 4,
            date: '2024-01-10',
            content: '性价比很高，推荐年卡套餐。'
          }
        ],
        createTime: db.serverDate()
      },
      {
        name: '一兆韦德健身',
        address: '桥西区自强路128号',
        phone: '0311-87654322',
        rating: 4.6,
        reviewCount: 256,
        hours: '07:00-23:00',
        description: '一兆韦德健身是国内知名连锁健身品牌，配备国际一流品牌器材，提供专业的私教服务和丰富的团课课程。',
        image: 'https://img.icons8.com/ios-filled/100/1E3A5F/dumbbell.png',
        location: { latitude: 38.040, longitude: 114.500 },
        facilities: [
          { name: '有氧区', icon: 'https://img.icons8.com/ios/100/1E3A5F/treadmill.png', available: true },
          { name: '力量区', icon: 'https://img.icons8.com/ios/100/1E3A5F/dumbbell.png', available: true },
          { name: '动感单车', icon: 'https://img.icons8.com/ios/100/1E3A5F/bicycle.png', available: true },
          { name: '搏击区', icon: 'https://img.icons8.com/ios/100/1E3A5F/boxing-gloves.png', available: true },
          { name: '私教区', icon: 'https://img.icons8.com/ios/100/1E3A5F/personal-trainer.png', available: true },
          { name: '瑜伽房', icon: 'https://img.icons8.com/ios/100/1E3A5F/lotus-position.png', available: false },
          { name: '游泳池', icon: 'https://img.icons8.com/ios/100/1E3A5F/swimming-pool.png', available: false },
          { name: '普拉提', icon: 'https://img.icons8.com/ios/100/1E3A5F/pilates.png', available: false }
        ],
        packages: [
          {
            name: '月卡',
            price: 299,
            originalPrice: 499,
            discount: '6折',
            benefits: ['无限次使用', '储物柜', '淋浴'],
            recommend: false
          },
          {
            name: '季卡',
            price: 799,
            originalPrice: 1299,
            discount: '6.1折',
            benefits: ['无限次使用', '储物柜', '淋浴', '团课', '私教1节'],
            recommend: false
          },
          {
            name: '年卡',
            price: 1680,
            originalPrice: 3680,
            discount: '4.6折',
            benefits: ['无限次使用', '储物柜', '淋浴', '团课', '私教8节'],
            recommend: true
          }
        ],
        reviews: [
          {
            user: '健身新手',
            avatar: 'https://img.icons8.com/ios-filled/100/1E3A5F/user.png',
            rating: 5,
            date: '2024-01-12',
            content: '教练很耐心，新手友好！'
          }
        ],
        createTime: db.serverDate()
      },
      {
        name: '英派斯健身俱乐部',
        address: '裕华区建设大街380号',
        phone: '0311-87654323',
        rating: 4.5,
        reviewCount: 189,
        hours: '06:30-22:30',
        description: '英派斯健身俱乐部是一家综合性健身会所，拥有完善的设施和专业的教练团队，致力于为会员提供优质的健身体验。',
        image: 'https://img.icons8.com/ios-filled/100/1E3A5F/barbell.png',
        location: { latitude: 38.038, longitude: 114.520 },
        facilities: [
          { name: '有氧区', icon: 'https://img.icons8.com/ios/100/1E3A5F/treadmill.png', available: true },
          { name: '力量区', icon: 'https://img.icons8.com/ios/100/1E3A5F/dumbbell.png', available: true },
          { name: '瑜伽房', icon: 'https://img.icons8.com/ios/100/1E3A5F/lotus-position.png', available: true },
          { name: '私教区', icon: 'https://img.icons8.com/ios/100/1E3A5F/personal-trainer.png', available: true },
          { name: '普拉提', icon: 'https://img.icons8.com/ios/100/1E3A5F/pilates.png', available: true },
          { name: '游泳池', icon: 'https://img.icons8.com/ios/100/1E3A5F/swimming-pool.png', available: false },
          { name: '动感单车', icon: 'https://img.icons8.com/ios/100/1E3A5F/bicycle.png', available: false },
          { name: '搏击区', icon: 'https://img.icons8.com/ios/100/1E3A5F/boxing-gloves.png', available: false }
        ],
        packages: [
          {
            name: '月卡',
            price: 268,
            originalPrice: 468,
            discount: '5.7折',
            benefits: ['无限次使用', '储物柜', '淋浴'],
            recommend: false
          },
          {
            name: '季卡',
            price: 688,
            originalPrice: 1188,
            discount: '5.8折',
            benefits: ['无限次使用', '储物柜', '淋浴', '团课'],
            recommend: false
          },
          {
            name: '年卡',
            price: 1288,
            originalPrice: 2888,
            discount: '4.5折',
            benefits: ['无限次使用', '储物柜', '淋浴', '团课', '私教6节', '普拉提'],
            recommend: true
          }
        ],
        reviews: [
          {
            user: '瑜伽爱好者',
            avatar: 'https://img.icons8.com/ios-filled/100/1E3A5F/user.png',
            rating: 4,
            date: '2024-01-08',
            content: '瑜伽课很专业，环境也不错。'
          }
        ],
        createTime: db.serverDate()
      },
      {
        name: '乐刻健身',
        address: '新华区中华北大街168号',
        phone: '0311-87654324',
        rating: 4.4,
        reviewCount: 412,
        hours: '24小时营业',
        description: '乐刻健身是一家24小时连锁健身品牌，主打高性价比和便捷服务，让您随时都能享受健身的乐趣。',
        image: 'https://img.icons8.com/ios-filled/100/1E3A5F/fitness-center.png',
        location: { latitude: 38.048, longitude: 114.495 },
        facilities: [
          { name: '有氧区', icon: 'https://img.icons8.com/ios/100/1E3A5F/treadmill.png', available: true },
          { name: '力量区', icon: 'https://img.icons8.com/ios/100/1E3A5F/dumbbell.png', available: true },
          { name: '团课区', icon: 'https://img.icons8.com/ios/100/1E3A5F/dancing.png', available: true },
          { name: '淋浴区', icon: 'https://img.icons8.com/ios/100/1E3A5F/shower.png', available: true },
          { name: '瑜伽房', icon: 'https://img.icons8.com/ios/100/1E3A5F/lotus-position.png', available: false },
          { name: '游泳池', icon: 'https://img.icons8.com/ios/100/1E3A5F/swimming-pool.png', available: false },
          { name: '私教区', icon: 'https://img.icons8.com/ios/100/1E3A5F/personal-trainer.png', available: false },
          { name: '搏击区', icon: 'https://img.icons8.com/ios/100/1E3A5F/boxing-gloves.png', available: false }
        ],
        packages: [
          {
            name: '月卡',
            price: 99,
            originalPrice: 199,
            discount: '5折',
            benefits: ['24小时使用', '储物柜', '淋浴', '团课'],
            recommend: true
          },
          {
            name: '季卡',
            price: 269,
            originalPrice: 499,
            discount: '5.4折',
            benefits: ['24小时使用', '储物柜', '淋浴', '团课'],
            recommend: false
          },
          {
            name: '年卡',
            price: 999,
            originalPrice: 1999,
            discount: '5折',
            benefits: ['24小时使用', '储物柜', '淋浴', '团课'],
            recommend: false
          }
        ],
        reviews: [
          {
            user: '夜猫子',
            avatar: 'https://img.icons8.com/ios-filled/100/1E3A5F/user.png',
            rating: 5,
            date: '2024-01-14',
            content: '24小时营业太方便了，晚上下班也能来健身！'
          },
          {
            user: '学生党',
            avatar: 'https://img.icons8.com/ios-filled/100/1E3A5F/user.png',
            rating: 4,
            date: '2024-01-11',
            content: '价格很实惠，适合学生。'
          }
        ],
        createTime: db.serverDate()
      }
    ]

    // 批量插入
    for (const gym of gyms) {
      await db.collection('gyms').add({ data: gym })
    }

    return {
      success: true,
      message: '数据库初始化完成',
      count: gyms.length
    }
  } catch (error) {
    console.error('初始化失败:', error)
    return {
      success: false,
      message: '初始化失败',
      error: error.message
    }
  }
}
