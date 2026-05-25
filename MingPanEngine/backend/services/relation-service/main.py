"""
人际关系耦合 FastAPI 服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.utils.bazi_engine import calculate_bazi
from shared.utils.relation_engine import analyze_relationship

app = FastAPI(title="人际关系耦合服务", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RelationRequest(BaseModel):
    person1_birth_date: str = Field(..., description="第一人生日 (YYYY-MM-DD)")
    person1_birth_time: str = Field(..., description="第一人出生时间 (HH:MM)")
    person1_gender: str = Field(..., description="第一人性别 (male/female)")
    person2_birth_date: str = Field(..., description="第二人生日 (YYYY-MM-DD)")
    person2_birth_time: str = Field(..., description="第二人出生时间 (HH:MM)")
    person2_gender: str = Field(..., description="第二人性别 (male/female)")
    relationship_type: str = Field("spouse", description="关系类型 (spouse/partner/friend/colleague)")


@app.get("/")
async def root():
    return {"service": "人际关系耦合服务", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/v1/relation/analyze")
async def analyze(request: RelationRequest):
    """合盘分析"""
    try:
        dt1 = datetime.strptime(f"{request.person1_birth_date} {request.person1_birth_time}", "%Y-%m-%d %H:%M")
        dt2 = datetime.strptime(f"{request.person2_birth_date} {request.person2_birth_time}", "%Y-%m-%d %H:%M")

        chart1 = calculate_bazi(dt1, request.person1_gender)
        chart2 = calculate_bazi(dt2, request.person2_gender)

        result = analyze_relationship(chart1, chart2, request.relationship_type)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
