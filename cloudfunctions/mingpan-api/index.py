# -*- coding: utf-8 -*-
"""
命理星河 API 网关 - CloudBase HTTP 云函数
统一路由小程序请求到各个计算引擎
"""

import json
import sys
import os
from datetime import datetime

# 添加共享模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from shared.utils.bazi_engine import calculate_bazi
from shared.utils.fengshui_engine import analyze_fengshui
from shared.utils.relation_engine import analyze_relationship
from shared.utils.ziwei_engine import calculate_ziwei
from shared.utils.oasis.agent_model import create_agent
from shared.utils.oasis.simulation_service import run_simulation

app = FastAPI(title="命理星河 API 网关", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        'service': '命理星河 API 网关',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': ['/api/simulate', '/api/relation', '/api/fengshui', '/health']
    }


@app.get("/health")
async def health():
    return {'status': 'healthy'}


@app.post("/api/simulate")
async def simulate(request: Request):
    """推演仿真"""
    try:
        body = await request.json()
        agents_data = body.get('agents', [])
        scenario = body.get('scenario', 'career')
        steps = body.get('steps', 12)
        samples = body.get('samples', 50)

        if not agents_data:
            return JSONResponse(status_code=400, content={'error': '请提供Agent数据'})

        agents = []
        for i, agent_data in enumerate(agents_data):
            name = agent_data.get('name', f'Agent_{i}')
            birth_date = agent_data.get('birth_date')
            birth_time = agent_data.get('birth_time', '00:00:00')
            gender = agent_data.get('gender', 'male')

            if not birth_date:
                return JSONResponse(status_code=400, content={'error': f'Agent {name} 缺少出生日期'})

            # 计算八字
            bazi_result = calculate_bazi(birth_date, birth_time, gender)

            # 计算紫微(可选)
            ziwei_result = None
            try:
                dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
                ziwei_result = calculate_ziwei(dt, gender)
            except:
                pass

            # 创建Agent
            agent = create_agent(
                agent_id=f"agent_{i}",
                name=name,
                bazi_result=bazi_result,
                gender=gender,
                ziwei_result=ziwei_result
            )
            agents.append(agent)

        # 运行仿真
        result = run_simulation(
            agents=agents,
            scenario=scenario,
            steps=steps,
            samples=samples
        )

        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={'error': f'推演失败: {str(e)}'})


@app.post("/api/relation")
async def relation(request: Request):
    """关系分析"""
    try:
        body = await request.json()
        person1 = body.get('person1', {})
        person2 = body.get('person2', {})

        if not person1 or not person2:
            return JSONResponse(status_code=400, content={'error': '请提供两个人的命盘数据'})

        # 计算八字
        chart1 = calculate_bazi(
            person1.get('birth_date'),
            person1.get('birth_time', '00:00'),
            person1.get('gender', 'male')
        )
        chart2 = calculate_bazi(
            person2.get('birth_date'),
            person2.get('birth_time', '00:00'),
            person2.get('gender', 'male')
        )

        # 分析关系
        result = analyze_relationship(chart1, chart2, 'spouse')

        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={'error': f'关系分析失败: {str(e)}'})


@app.post("/api/fengshui")
async def fengshui(request: Request):
    """风水分析"""
    try:
        body = await request.json()
        location = body.get('location', {})
        birth_year = body.get('birth_year', 1990)
        gender = body.get('gender', 'male')
        building_direction = body.get('building_direction', 180)
        building_year = body.get('building_year', 2000)

        # 使用参数进行风水分析
        result = analyze_fengshui(
            birth_year=birth_year,
            gender=gender,
            building_direction=building_direction,
            building_year=building_year,
            current_year=2026
        )

        # 添加位置信息
        if location:
            result['location'] = location

        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={'error': f'风水分析失败: {str(e)}'})
