"""
风水环境计算 FastAPI 服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.utils.fengshui_engine import analyze_fengshui, FengShuiEngine

app = FastAPI(title="风水环境计算服务", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FengShuiRequest(BaseModel):
    birth_year: int = Field(..., description="出生年份", examples=[1990])
    gender: str = Field(..., description="性别 (male/female)", examples=["male"])
    building_direction: float = Field(..., description="建筑朝向(度数, 0=北, 90=东)", examples=[180])
    building_year: int = Field(2000, description="建筑年份")
    current_year: int = Field(2026, description="当前年份")


@app.get("/")
async def root():
    return {"service": "风水环境计算服务", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/v1/fengshui/analyze")
async def analyze(request: FengShuiRequest):
    """风水综合分析"""
    try:
        result = analyze_fengshui(
            request.birth_year,
            request.gender,
            request.building_direction,
            request.building_year,
            request.current_year
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/fengshui/ming-gua/{birth_year}/{gender}")
async def get_ming_gua(birth_year: int, gender: str):
    """查询命卦"""
    engine = FengShuiEngine()
    ming_gua = engine.calc_ming_gua(birth_year, gender)
    return {
        'number': ming_gua.number,
        'direction': ming_gua.direction,
        'group': ming_gua.group,
        'gender': ming_gua.gender
    }


@app.get("/api/v1/fengshui/yearly-stars/{year}")
async def get_yearly_stars(year: int):
    """查询流年飞星"""
    engine = FengShuiEngine()
    yearly = engine._calc_yearly_fei_xing(year)
    return {"year": year, "yearly_stars": yearly}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
