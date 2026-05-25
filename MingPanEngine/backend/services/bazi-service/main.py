"""
八字排盘服务 - FastAPI接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.utils.bazi_engine import calculate_bazi, BaziEngine

app = FastAPI(
    title="八字排盘服务",
    description="提供八字排盘、十神计算、旺衰判定、大运排列等服务",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== 数据模型 ====================

class BaziRequest(BaseModel):
    """八字计算请求"""
    birth_date: str = Field(..., description="出生日期 YYYY-MM-DD", example="1990-05-15")
    birth_time: str = Field(..., description="出生时间 HH:MM:SS", example="14:30:00")
    gender: str = Field(..., description="性别 male/female", example="male")
    longitude: Optional[float] = Field(116.4074, description="出生地经度", example=116.4074)
    latitude: Optional[float] = Field(None, description="出生地纬度（可选）")
    city: Optional[str] = Field(None, description="出生城市（可选）")


class BaziResponse(BaseModel):
    """八字计算响应"""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


class ShishenRequest(BaseModel):
    """十神查询请求"""
    ri_gan: str = Field(..., description="日干", example="甲")
    other_gan: str = Field(..., description="对方天干", example="乙")


# ==================== API端点 ====================

@app.get("/")
async def root():
    """服务根路径"""
    return {
        "service": "八字排盘服务",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "calculate": "/api/v1/bazi/calculate",
            "shishen": "/api/v1/bazi/shishen",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "bazi-service"}


@app.post("/api/v1/bazi/calculate", response_model=BaziResponse)
async def calculate_bazi_api(request: BaziRequest):
    """
    计算八字排盘
    
    - **birth_date**: 出生日期 (YYYY-MM-DD)
    - **birth_time**: 出生时间 (HH:MM:SS)
    - **gender**: 性别 (male/female)
    - **longitude**: 出生地经度 (默认北京 116.4074)
    """
    try:
        # 验证日期格式
        try:
            datetime.strptime(request.birth_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，应为 YYYY-MM-DD")
        
        # 验证时间格式
        try:
            datetime.strptime(request.birth_time, "%H:%M:%S")
        except ValueError:
            raise HTTPException(status_code=400, detail="时间格式错误，应为 HH:MM:SS")
        
        # 验证性别
        if request.gender not in ['male', 'female']:
            raise HTTPException(status_code=400, detail="性别应为 male 或 female")
        
        # 计算八字
        result = calculate_bazi(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            gender=request.gender,
            longitude=request.longitude or 116.4074
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


@app.get("/api/v1/bazi/shishen")
async def get_shishen(ri_gan: str, other_gan: str):
    """
    查询十神关系
    
    - **ri_gan**: 日干
    - **other_gan**: 对方天干
    """
    from shared.utils.bazi_engine import SHISHEN_TABLE
    
    if ri_gan not in ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']:
        raise HTTPException(status_code=400, detail="日干应为十天干之一")
    
    if other_gan not in ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']:
        raise HTTPException(status_code=400, detail="对方天干应为十天干之一")
    
    shishen = SHISHEN_TABLE.get((ri_gan, other_gan), '未知')
    
    return {
        '日干': ri_gan,
        '对方天干': other_gan,
        '十神': shishen
    }


@app.get("/api/v1/bazi/wuxing/{gan}")
async def get_wuxing(gan: str):
    """
    查询天干五行
    
    - **gan**: 天干
    """
    from shared.utils.bazi_engine import TIAN_GAN_WUXING, TIAN_GAN_YINYANG
    
    if gan not in TIAN_GAN_WUXING:
        raise HTTPException(status_code=400, detail="应为十天干之一")
    
    return {
        '天干': gan,
        '五行': TIAN_GAN_WUXING[gan],
        '阴阳': TIAN_GAN_YINYANG[gan]
    }


@app.get("/api/v1/bazi/cang-gan/{zhi}")
async def get_cang_gan(zhi: str):
    """
    查询地支藏干
    
    - **zhi**: 地支
    """
    from shared.utils.bazi_engine import DI_ZHI_CANG_GAN, DI_ZHI_WUXING, DI_ZHI_YINYANG
    
    if zhi not in DI_ZHI_CANG_GAN:
        raise HTTPException(status_code=400, detail="应为十二地支之一")
    
    return {
        '地支': zhi,
        '五行': DI_ZHI_WUXING[zhi],
        '阴阳': DI_ZHI_YINYANG[zhi],
        '藏干': DI_ZHI_CANG_GAN[zhi]
    }


@app.get("/api/v1/bazi/liu-he")
async def get_liu_he():
    """查询地支六合"""
    from shared.utils.bazi_engine import DI_ZHI_LIU_HE
    
    return {
        '六合': DI_ZHI_LIU_HE,
        '说明': '子丑合土、寅亥合木、卯戌合火、辰酉合金、巳申合水、午未合土'
    }


@app.get("/api/v1/bazi/san-he")
async def get_san_he():
    """查询地支三合"""
    from shared.utils.bazi_engine import DI_ZHI_SAN_HE
    
    return {
        '三合': {
            '申子辰': '合水局',
            '寅午戌': '合火局',
            '巳酉丑': '合金局',
            '亥卯未': '合木局'
        }
    }


@app.get("/api/v1/bazi/liu-chong")
async def get_liu_chong():
    """查询地支六冲"""
    from shared.utils.bazi_engine import DI_ZHI_LIU_CHONG
    
    return {
        '六冲': DI_ZHI_LIU_CHONG,
        '说明': '子午冲、丑未冲、寅申冲、卯酉冲、辰戌冲、巳亥冲'
    }


# ==================== 启动 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)