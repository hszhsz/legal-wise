from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from typing import Dict, Any, AsyncGenerator
from datetime import datetime

from backend.agents.legal_agent import LegalPlanExecuteAgent
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Legal Wise API",
    description="智能法律咨询系统 - 基于LangChain和LangGraph的plan-and-execute agent",
    version="2.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局agent实例
legal_agent = None

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化agent"""
    global legal_agent
    try:
        legal_agent = LegalPlanExecuteAgent()
        await legal_agent.initialize()
        logger.info("Legal agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize legal agent: {e}")
        raise

@app.post("/api/legal/consult")
async def legal_consultation(request: Request):
    """法律咨询接口 - 流式响应"""
    try:
        data = await request.json()
        query = data.get("query", "")
        case_type = data.get("case_type", "general")
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        logger.info(f"Received consultation request: {query[:100]}...")
        
        async def generate_response() -> AsyncGenerator[str, None]:
            try:
                consultation_stream = legal_agent.stream_consultation(query, case_type)
                async for event in consultation_stream:
                    yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
            except Exception as e:
                logger.error(f"Error in consultation: {e}")
                error_event = {
                    "type": "error",
                    "content": "处理咨询时发生错误，请稍后重试",
                    "timestamp": datetime.now().isoformat()
                }
                yield f"data: {json.dumps(error_event, ensure_ascii=False)}\n\n"
        
        return EventSourceResponse(generate_response())
        
    except Exception as e:
        logger.error(f"Consultation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/legal/analyze")
async def legal_analysis(request: Request):
    """法律案情分析接口"""
    try:
        data = await request.json()
        case_description = data.get("case_description", "")
        
        if not case_description:
            raise HTTPException(status_code=400, detail="Case description is required")
        
        result = await legal_agent.analyze_case(case_description)
        return {"status": "success", "data": result}
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/legal/search-cases")
async def search_legal_cases(request: Request):
    """案例检索接口"""
    try:
        data = await request.json()
        keywords = data.get("keywords", "")
        case_type = data.get("case_type", "")
        
        if not keywords:
            raise HTTPException(status_code=400, detail="Keywords are required")
        
        result = await legal_agent.search_cases(keywords, case_type)
        return {"status": "success", "data": result}
        
    except Exception as e:
        logger.error(f"Case search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/legal/recommend-lawyers")
async def recommend_lawyers(request: Request):
    """律师推荐接口"""
    try:
        data = await request.json()
        case_type = data.get("case_type", "")
        location = data.get("location", "")
        
        result = await legal_agent.recommend_lawyers(case_type, location)
        return {"status": "success", "data": result}
        
    except Exception as e:
        logger.error(f"Lawyer recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/legal/generate-report")
async def generate_legal_report(request: Request):
    """生成法律分析报告接口"""
    try:
        data = await request.json()
        case_data = data.get("case_data", {})
        
        if not case_data:
            raise HTTPException(status_code=400, detail="Case data is required")
        
        result = await legal_agent.generate_report(case_data)
        return {"status": "success", "data": result}
        
    except Exception as e:
        logger.error(f"Report generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "agent_status": "ready" if legal_agent else "not_initialized"
    }

@app.get("/api/agent/status")
async def agent_status():
    """Agent状态检查"""
    if not legal_agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    status = await legal_agent.get_status()
    return {"status": "success", "data": status}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )