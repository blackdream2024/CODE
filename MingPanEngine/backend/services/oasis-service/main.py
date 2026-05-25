"""
OASIS推演 FastAPI 服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import sys
import os

# 添加父目录到路径（与其他服务一致）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# 导入引擎模块（使用包路径）
from shared.utils.bazi_engine import calculate_bazi
from shared.utils.ziwei_engine import calculate_ziwei
from shared.utils.oasis.agent_model import create_agent, MingPanAgent
from shared.utils.oasis.simulation_service import run_simulation

app = FastAPI(title="OASIS推演服务", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentInput(BaseModel):
    name: str = Field(..., description="Agent名称")
    birth_date: str = Field(..., description="出生日期 (YYYY-MM-DD)")
    birth_time: str = Field(..., description="出生时间 (HH:MM:SS)")
    gender: str = Field(..., description="性别 (male/female)")


class SimulationRequest(BaseModel):
    agents: List[AgentInput] = Field(..., description="Agent列表")
    scenario: str = Field(..., description="场景类型 (career/marriage/cooperation/relocation)")
    steps: int = Field(12, description="仿真步数(月)")
    samples: int = Field(50, description="采样次数")


@app.get("/")
async def root():
    return {"service": "OASIS推演服务", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/v1/oasis/simulate")
async def simulate(request: SimulationRequest):
    """运行推演仿真"""
    try:
        agents = []

        for i, agent_input in enumerate(request.agents):
            # 计算八字
            bazi_result = calculate_bazi(
                agent_input.birth_date,
                agent_input.birth_time,
                agent_input.gender
            )

            # 计算紫微(可选)
            try:
                dt = datetime.strptime(
                    f"{agent_input.birth_date} {agent_input.birth_time}",
                    "%Y-%m-%d %H:%M:%S"
                )
                ziwei_result = calculate_ziwei(dt, agent_input.gender)
            except:
                ziwei_result = None

            # 创建Agent
            agent = create_agent(
                agent_id=f"agent_{i}",
                name=agent_input.name,
                bazi_result=bazi_result,
                gender=agent_input.gender,
                ziwei_result=ziwei_result
            )
            agents.append(agent)

        # 运行仿真
        result = run_simulation(
            agents=agents,
            scenario=request.scenario,
            steps=request.steps,
            samples=request.samples
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/oasis/scenarios")
async def get_scenarios():
    """获取可用场景"""
    return {
        "scenarios": [
            {"type": "career", "name": "事业推演", "description": "分析事业发展前景，含格局影响、大运十神、事业宫星曜"},
            {"type": "marriage", "name": "婚姻推演", "description": "分析感情婚姻走势，含桃花星、夫妻宫、红鸾天喜"},
            {"type": "cooperation", "name": "合作推演", "description": "分析合作关系发展，含五行生克、性格兼容、贵人星"},
            {"type": "relocation", "name": "搬迁推演", "description": "分析搬迁时机，含驿马星、迁移宫、流年飞星"},
            {"type": "investment", "name": "投资推演", "description": "分析投资财运，含财星、禄神、偏财格"},
            {"type": "health", "name": "健康推演", "description": "分析健康状况，含天医星、五行平衡、长生宫"},
            {"type": "learning", "name": "学习推演", "description": "分析学习考试运，含文昌贵人、华盖星、正印格"}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
