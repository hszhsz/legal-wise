# Rightify - 智能法律咨询系统

基于 LangChain 和 LangGraph 的 plan-and-execute agent 架构的智能法律咨询系统，支持自然语言查询法律案例和咨询法律问题。系统提供专业的法律建议和智能分析服务。

**让公正触手可及** - Rightify致力于通过AI技术让法律服务更加智能化、便民化。

## 功能特点

- 🤖 **智能法律咨询** - 基于 plan-and-execute agent 的专业法律建议
- 🔍 **法律案例分析** - 智能分析和检索相关法律案例
- 📋 **案例搜索** - 快速查找相关法律案例和判例
- 👨‍💼 **律师推荐** - 根据案件类型推荐合适的律师
- 📄 **法律报告生成** - 自动生成专业的法律分析报告
- ⚡ **实时流式响应** - 基于 SSE 技术的实时交互体验
- 🎨 **现代化界面** - 基于 Next.js 和 Tailwind CSS 的美观界面

## 技术栈

### 后端
- **Python 3.12+** - 现代 Python 开发
- **FastAPI 0.104.0+** - 高性能 Web 框架
- **LangChain 0.1.0+** - AI 应用开发框架
- **LangGraph 0.0.20+** - Plan-and-execute agent 架构
- **SSE-Starlette 2.0.0+** - 服务器发送事件支持
- **Uvicorn** - ASGI 服务器
- **OpenAI API** - 大语言模型接口

### 前端
- **Next.js 15.4.6** - React 全栈框架
- **React 19.1.0** - 用户界面库
- **TypeScript 5.x** - 类型安全的 JavaScript
- **Tailwind CSS 4.x** - 实用优先的 CSS 框架
- **Headless UI 2.2.6** - 无样式 UI 组件
- **Framer Motion 12.23.12** - 动画库
- **Heroicons & Lucide React** - 图标库

## 快速开始

### 环境要求

- **Python 3.12+**
- **Node.js 18+**
- **npm 8+**
- **uv** (Python 包管理器)

### 一键启动（推荐）

使用项目提供的启动脚本：

```bash
# 给脚本执行权限
chmod +x start.sh

# 启动前后端服务
./start.sh
```

### 手动设置

#### 1. 安装 uv（Python 包管理器）
```bash
pip install uv
```

#### 2. 后端设置

```bash
# 安装 Python 依赖
uv sync

# 创建 .env 文件并设置 API 密钥
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 启动后端服务
cd backend
uv run uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

#### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## API 文档

### 主要接口

- `POST /api/legal/consult` - 法律咨询接口（流式响应）
- `POST /api/legal/analyze` - 法律案例分析接口
- `POST /api/legal/search-cases` - 法律案例搜索接口
- `POST /api/legal/recommend-lawyers` - 律师推荐接口
- `POST /api/legal/generate-report` - 法律报告生成接口
- `GET /api/health` - 健康检查接口
- `GET /api/agent/status` - Agent 状态检查接口

### 开发和测试

```bash
# 启动开发服务器
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload

# 运行测试
uv run pytest tests/

# 停止所有服务
./stop.sh
```

## 使用说明

1. 访问 http://localhost:3000 打开前端界面
2. 选择服务类型：
   - **法律咨询** - 获取专业法律建议
   - **案例分析** - 分析具体法律案例
   - **案例搜索** - 查找相关判例
   - **律师推荐** - 获取律师推荐
   - **报告生成** - 生成法律分析报告
3. 输入您的问题或案例描述
4. 点击提交按钮获取实时流式回复

## 项目结构

```
rightify/
├── backend/                 # 后端服务
│   ├── agents/             # AI Agent 实现
│   ├── tools/              # 法律工具集
│   ├── utils/              # 工具函数
│   ├── config.py           # 配置文件
│   └── main.py             # 主应用入口
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── app/            # Next.js 应用页面
│   │   ├── components/     # React 组件
│   │   └── contexts/       # React 上下文
│   └── package.json        # 前端依赖
├── tests/                  # 测试文件
├── logs/                   # 日志目录
├── start.sh               # 启动脚本
├── stop.sh                # 停止脚本
└── pyproject.toml         # Python 项目配置
```

## 注意事项

- 请确保在使用前设置有效的 OpenAI API 密钥
- 系统使用 plan-and-execute agent 架构，可在 config.py 中修改配置
- 后端服务默认运行在 **8001** 端口
- 前端开发服务器默认运行在 **3000** 端口
- 系统支持实时流式响应，提供更好的用户体验
- 推荐使用 `uv` 作为 Python 包管理器以获得更好的性能

## 许可证

MIT License