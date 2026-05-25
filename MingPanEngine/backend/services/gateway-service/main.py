"""
命理星河 API 网关服务
统一路由小程序请求到各个微服务
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
import sys

# 添加父目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

app = FastAPI(
    title="命理星河 API 网关",
    description="统一路由小程序请求到各个微服务",
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

# 微服务地址配置（可通过环境变量覆盖）
SERVICES = {
    "bazi": os.getenv("BAZI_SERVICE_URL", "http://localhost:8001"),
    "ziwei": os.getenv("ZIWEI_SERVICE_URL", "http://localhost:8002"),
    "relation": os.getenv("RELATION_SERVICE_URL", "http://localhost:8004"),
    "fengshui": os.getenv("FENGSHUI_SERVICE_URL", "http://localhost:8005"),
    "oasis": os.getenv("OASIS_SERVICE_URL", "http://localhost:8007"),
}


@app.get("/")
async def root():
    """服务信息"""
    return {
        "service": "命理星河 API 网关",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "simulate": "/api/simulate",
            "relation": "/api/relation",
            "fengshui": "/api/fengshui",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "gateway-service"}


@app.post("/api/simulate")
async def simulate(request: Request):
    """
    推演仿真接口
    路由到 OASIS 推演服务
    """
    try:
        body = await request.json()
        
        # 转换请求格式
        oasis_request = {
            "agents": body.get("agents", []),
            "scenario": body.get("scenario", "career"),
            "steps": body.get("steps", 12),
            "samples": body.get("samples", 50)
        }
        
        # 调用 OASIS 服务
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['oasis']}/api/v1/oasis/simulate",
                json=oasis_request,
                timeout=60.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"OASIS 服务错误: {response.text}"
                )
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="OASIS 服务超时")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推演失败: {str(e)}")


@app.post("/api/relation")
async def relation(request: Request):
    """
    关系分析接口
    路由到人际关系耦合服务
    """
    try:
        body = await request.json()
        
        # 转换请求格式
        relation_request = {
            "person1_birth_date": body.get("person1", {}).get("birth_date"),
            "person1_birth_time": body.get("person1", {}).get("birth_time", "00:00"),
            "person1_gender": body.get("person1", {}).get("gender"),
            "person2_birth_date": body.get("person2", {}).get("birth_date"),
            "person2_birth_time": body.get("person2", {}).get("birth_time", "00:00"),
            "person2_gender": body.get("person2", {}).get("gender"),
            "relationship_type": "spouse"
        }
        
        # 调用关系分析服务
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['relation']}/api/v1/relation/analyze",
                json=relation_request,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"关系分析服务错误: {response.text}"
                )
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="关系分析服务超时")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"关系分析失败: {str(e)}")


@app.post("/api/fengshui")
async def fengshui(request: Request):
    """
    风水分析接口
    路由到风水环境计算服务
    """
    try:
        body = await request.json()
        
        # 转换请求格式
        fengshui_request = {
            "birth_year": 1990,  # 默认值，需要从用户信息获取
            "gender": "male",    # 默认值，需要从用户信息获取
            "building_direction": 180,  # 默认朝南
            "building_year": 2000,
            "current_year": 2026
        }
        
        # 如果有位置信息，使用位置信息
        if "location" in body:
            # 这里可以根据位置信息计算朝向等
            pass
        
        # 调用风水分析服务
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SERVICES['fengshui']}/api/v1/fengshui/analyze",
                json=fengshui_request,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"风水分析服务错误: {response.text}"
                )
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="风水分析服务超时")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"风水分析失败: {str(e)}")


@app.get("/api/services")
async def list_services():
    """列出所有可用的微服务"""
    return {
        "services": [
            {"name": "bazi", "url": SERVICES["bazi"], "description": "八字排盘服务"},
            {"name": "ziwei", "url": SERVICES["ziwei"], "description": "紫微斗数服务"},
            {"name": "relation", "url": SERVICES["relation"], "description": "人际关系耦合服务"},
            {"name": "fengshui", "url": SERVICES["fengshui"], "description": "风水环境计算服务"},
            {"name": "oasis", "url": SERVICES["oasis"], "description": "OASIS推演服务"}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)