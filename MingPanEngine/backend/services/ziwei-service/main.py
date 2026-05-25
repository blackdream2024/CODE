"""
紫微斗数 FastAPI 服务
提供紫微斗数排盘计算 API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.utils.ziwei_engine import calculate_ziwei, ZiWeiEngine

app = FastAPI(
    title="紫微斗数排盘服务",
    description="紫微斗数命盘计算API - 十二宫、14主星、辅星煞星、四化飞星、大限流年",
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

class ZiWeiRequest(BaseModel):
    """紫微斗数计算请求"""
    birth_date: str = Field(..., description="出生日期 (YYYY-MM-DD)", examples=["1990-01-15"])
    birth_time: str = Field(..., description="出生时间 (HH:MM)", examples=["14:30"])
    gender: str = Field(..., description="性别 (male/female)", examples=["male"])
    lunar_month: Optional[int] = Field(None, description="农历月 (可选，1-12)")
    lunar_day: Optional[int] = Field(None, description="农历日 (可选，1-30)")
    is_leap_month: Optional[bool] = Field(False, description="是否闰月")

    class Config:
        json_schema_extra = {
            "example": {
                "birth_date": "1990-01-15",
                "birth_time": "14:30",
                "gender": "male",
                "lunar_month": None,
                "lunar_day": None
            }
        }


class StarInfo(BaseModel):
    """星曜信息"""
    name: str
    category: str
    hua: List[str] = []


class PalaceInfo(BaseModel):
    """宫位信息"""
    name: str
    zhi: str
    tian_gan: str
    is_ming_palace: bool
    stars: List[StarInfo]


class ZiWeiResponse(BaseModel):
    """紫微斗数计算结果"""
    lunar_date: Dict
    gender: str
    wu_xing_ju: str
    ming_palace_zhi: str
    ming_palace_tian_gan: str
    shen_palace_zhi: str
    ming_zhu: str
    shen_zhu: str
    palaces: List[PalaceInfo]
    main_stars: Dict
    sihua: Dict
    da_xian: List[Dict]


# ==================== API端点 ====================

@app.get("/")
async def root():
    """服务信息"""
    return {
        "service": "紫微斗数排盘服务",
        "version": "1.0.0",
        "description": "提供紫微斗数命盘计算、十二宫排布、四化飞星等功能",
        "endpoints": [
            "POST /api/v1/ziwei/calculate - 紫微排盘",
            "GET /api/v1/ziwei/palace-names - 十二宫名称",
            "GET /api/v1/ziwei/main-stars - 14主星列表",
            "GET /api/v1/ziwei/sihua/{year_gan} - 四化查询",
            "GET /api/v1/ziwei/wu-xing-ju - 五行局说明"
        ]
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "ziwei-service"}


@app.post("/api/v1/ziwei/calculate", response_model=ZiWeiResponse)
async def calculate(request: ZiWeiRequest):
    """
    紫微斗数排盘计算

    根据出生日期、时间和性别计算紫微斗数命盘：
    - 十二宫排布
    - 14主星安星
    - 辅星、煞星安星
    - 四化飞星
    - 大限排列
    """
    try:
        # 解析出生日期和时间
        birth_datetime = datetime.strptime(
            f"{request.birth_date} {request.birth_time}",
            "%Y-%m-%d %H:%M"
        )

        # 验证性别
        if request.gender not in ('male', 'female'):
            raise HTTPException(status_code=400, detail="性别必须为 'male' 或 'female'")

        # 计算紫微斗数
        result = calculate_ziwei(
            birth_datetime,
            request.gender,
            request.lunar_month or 0,
            request.lunar_day or 0
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"日期格式错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


@app.get("/api/v1/ziwei/palace-names")
async def get_palace_names():
    """获取十二宫名称"""
    return {
        "palaces": [
            {"name": "命宫", "description": "主性格、外貌、才能"},
            {"name": "兄弟宫", "description": "主兄弟姐妹、合作关系"},
            {"name": "夫妻宫", "description": "主婚姻、感情"},
            {"name": "子女宫", "description": "主子女、性生活"},
            {"name": "财帛宫", "description": "主财运、理财能力"},
            {"name": "疾厄宫", "description": "主健康、疾病"},
            {"name": "迁移宫", "description": "主外出、旅行、社交"},
            {"name": "交友宫", "description": "主朋友、部属"},
            {"name": "事业宫", "description": "主事业、工作"},
            {"name": "田宅宫", "description": "主不动产、居住环境"},
            {"name": "福德宫", "description": "主精神生活、兴趣爱好"},
            {"name": "父母宫", "description": "主父母、长辈、教育"}
        ]
    }


@app.get("/api/v1/ziwei/main-stars")
async def get_main_stars():
    """获取14主星列表"""
    return {
        "main_stars": [
            {"name": "紫微", "description": "帝星，主尊贵、领导力", "element": "土"},
            {"name": "天机", "description": "主智慧、谋略、变化", "element": "木"},
            {"name": "太阳", "description": "主光明、博爱、贵人", "element": "火"},
            {"name": "武曲", "description": "主财星、刚毅、果断", "element": "金"},
            {"name": "天同", "description": "主福气、享受、懒散", "element": "水"},
            {"name": "廉贞", "description": "主桃花、政治、法律", "element": "火"},
            {"name": "天府", "description": "主财库、稳重、保守", "element": "土"},
            {"name": "太阴", "description": "主田宅、母亲、女性", "element": "水"},
            {"name": "贪狼", "description": "主桃花、才艺、欲望", "element": "木"},
            {"name": "巨门", "description": "主口舌、是非、暗星", "element": "土"},
            {"name": "天相", "description": "主印星、服务、辅佐", "element": "水"},
            {"name": "天梁", "description": "主荫星、解厄、长寿", "element": "土"},
            {"name": "七杀", "description": "主将星、冲劲、变动", "element": "金"},
            {"name": "破军", "description": "主耗星、开创、破坏", "element": "水"}
        ]
    }


@app.get("/api/v1/ziwei/sihua/{year_gan}")
async def get_sihua(year_gan: str):
    """
    查询四化飞星

    Args:
        year_gan: 年干 (甲乙丙丁戊己庚辛壬癸)
    """
    from ziwei_engine import SIHUA_TABLE, SIHUA_NAMES

    if year_gan not in SIHUA_TABLE:
        raise HTTPException(status_code=400, detail=f"无效的年干: {year_gan}")

    sihua = SIHUA_TABLE[year_gan]
    result = {}
    for i, name in enumerate(SIHUA_NAMES):
        result[name] = sihua[i]

    return {
        "year_gan": year_gan,
        "sihua": result
    }


@app.get("/api/v1/ziwei/wu-xing-ju")
async def get_wu_xing_ju():
    """获取五行局说明"""
    return {
        "wu_xing_ju": [
            {"name": "水二局", "number": 2, "element": "水", "description": "智慧、灵活、多变"},
            {"name": "木三局", "number": 3, "element": "木", "description": "仁慈、成长、向上"},
            {"name": "金四局", "number": 4, "element": "金", "description": "刚毅、果断、义气"},
            {"name": "土五局", "number": 5, "element": "土", "description": "稳重、包容、信用"},
            {"name": "火六局", "number": 6, "element": "火", "description": "热情、光明、礼节"}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
