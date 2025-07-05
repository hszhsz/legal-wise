from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain.agents import AgentExecutor
from sse_starlette.sse import EventSourceResponse
import legal_tools
from logger import logger  # 添加这行导入

app = FastAPI()

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class LegalAgent:
    def __init__(self):
        # 直接使用load_law_model返回的agent
        self.agent = legal_tools.load_law_model('deepseek-chat')

    async def stream_legal_response(self, user_query: str, case_type: str):
        async def event_generator():
            # 在LegalAgent类中添加错误处理
            try:
                # 使用字符串输入而不是复杂对象
                prompt = f"用户查询：{user_query}\n案例类型：{case_type}"
                result = await self.agent.ainvoke({"input": prompt})
            except Exception as e:
                yield {'event': 'error', 'data': '法律引擎异常'}
                logger.error(f"LegalAgent error: {str(e)}")
                return
            for token in result.split():
                yield {'event': 'message', 'data': token}

        return EventSourceResponse(event_generator())

@app.post('/api/legal/consult')
async def legal_consultation(request: Request):
    try:
        data = await request.json()
        logger.info(f"Received consultation request: {data}")
        agent = LegalAgent()
        # 为case_type提供默认值，避免KeyError
        case_type = data.get('case_type', '一般法律咨询')
        return await agent.stream_legal_response(data['text'], case_type)
    except Exception as e:
        logger.error(f"Consultation error: {str(e)}")
        raise

@app.post('/api/query')
@app.get('/api/query')
async def handle_query(request: Request):
    try:
        # 处理GET请求（用于SSE）
        if request.method == 'GET':
            # 从查询参数中获取数据
            params = dict(request.query_params)
            logger.info(f"Received GET query: {params}")
            agent = LegalAgent()
            text = params.get('text', '')
            case_type = params.get('case_type', '一般法律咨询')
            return await agent.stream_legal_response(text, case_type)
        # 处理POST请求
        else:
            return await legal_consultation(request)
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise

@app.get('/api/health')
async def health_check():
    return {'status': 'running'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)