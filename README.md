# Rightify - 智能法律咨询系统

基于大语言模型和智能体技术的智能法律咨询系统，支持自然语言查询法律案例和咨询法律问题。系统使用DeepSeek大语言模型提供专业的法律建议。

**让公正触手可及** - Rightify致力于通过AI技术让法律服务更加智能化、便民化。

## 功能特点

- 自然语言法律咨询
- 智能案例检索
- 实时流式响应（SSE技术）
- 友好的用户界面
- 支持法律咨询和案例查询两种模式

## 技术栈

### 后端
- Python
- FastAPI
- LangChain (v0.1.15)
- SSE-Starlette (v2.3.6)
- DeepSeek API

### 前端
- React 18
- TypeScript
- Ant Design 5.0
- Axios
- EventSource API (SSE客户端)

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 14+
- npm 6+

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r ../requirements.txt
```

4. 创建 .env 文件并设置 DeepSeek API 密钥：
```bash
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
```

5. 启动后端服务：
```bash
python main.py
```

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm start
```

## API 文档

### 主要接口

- `GET/POST /api/query` - 法律查询接口，支持SSE流式响应
- `POST /api/legal/consult` - 法律咨询接口
- `GET /api/health` - 健康检查接口

```bash
# 启动开发服务器
python backend/main.py
# 或者
uvicorn backend.main:app --reload

# 运行测试
pytest tests/
```

## 使用说明

1. 访问 http://localhost:3000 打开前端界面
2. 选择查询类型（法律咨询或案例查询）
3. 输入您的问题或查询内容
4. 点击提交按钮获取实时流式回复

## 注意事项

- 请确保在使用前设置有效的 DeepSeek API 密钥
- 系统默认使用 DeepSeek Chat 模型，可在 config.py 中修改
- 后端服务默认运行在 8000 端口
- 前端开发服务器默认运行在 3000 端口
- 系统支持实时流式响应，提供更好的用户体验

## 许可证

MIT License