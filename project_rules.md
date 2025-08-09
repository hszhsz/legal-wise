# Rightify 项目开发规范

## 项目概述

Rightify 是一个智能法律咨询系统，基于 LangChain 和 LangGraph 的 plan-and-execute agent 架构，旨在让公正触手可及。

## 技术栈规范

### 前端技术栈

- **框架**: Next.js 15.4.6 (React 19.1.0)
- **语言**: TypeScript 5.x
- **样式**: Tailwind CSS 4.x
- **UI组件**: 
  - Headless UI 2.2.6
  - Heroicons 2.2.0
  - Lucide React 0.539.0
- **动画**: Framer Motion 12.23.12
- **工具库**: 
  - clsx 2.1.1
  - tailwind-merge 3.3.1
- **开发工具**: 
  - ESLint 9.x
  - TypeScript 5.x
  - Turbopack (Next.js 内置)

### 后端技术栈

- **框架**: FastAPI 0.104.0+
- **语言**: Python 3.12+
- **ASGI服务器**: Uvicorn 0.24.0+
- **AI框架**: 
  - LangChain 0.1.0+
  - LangChain Community 0.0.10+
  - LangChain OpenAI 0.0.5+
  - LangGraph 0.0.20+
- **HTTP客户端**: httpx 0.25.0+
- **流式响应**: sse-starlette 2.0.0+
- **文件处理**: 
  - python-multipart 0.0.6+
  - aiofiles 23.0.0+
- **配置管理**: python-dotenv 1.0.0+
- **数据验证**: Pydantic 2.0.0+
- **模板引擎**: Jinja2 3.1.0+
- **AI模型**: OpenAI 1.0.0+

## 依赖管理规范

### Python 依赖管理

**必须使用 `uv` 作为 Python 包管理器**

```bash
# 安装 uv
pip install uv

# 安装项目依赖
uv sync

# 添加新依赖
uv add package_name

# 添加开发依赖
uv add --dev package_name

# 运行 Python 脚本
uv run python script.py

# 运行后端服务
uv run uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Node.js 依赖管理

**使用 `npm` 管理前端依赖**

```bash
# 安装依赖
npm install

# 添加新依赖
npm install package_name

# 添加开发依赖
npm install --save-dev package_name

# 运行开发服务器
npm run dev
```

## 项目启动和停止规范

### 启动服务

**使用 `start.sh` 脚本启动完整服务**

```bash
# 启动前后端服务
./start.sh
```

启动脚本会：
- 检查必要依赖（Node.js、Python3、uv）
- 启动后端服务（端口 8001）
- 启动前端服务（端口 3000）
- 创建日志文件（`logs/backend.log`、`logs/frontend.log`）
- 显示服务状态和访问地址

### 停止服务

**使用 `stop.sh` 脚本停止所有服务**

```bash
# 停止前后端服务
./stop.sh
```

停止脚本会：
- 通过 PID 文件停止对应服务
- 清理占用端口的残留进程
- 删除临时 PID 文件

### 服务端口规范

- **前端服务**: http://localhost:3000
- **后端服务**: http://localhost:8001
- **后端健康检查**: http://localhost:8001/api/health

## 开发规范

### 代码风格

**前端**:
- 使用 TypeScript 严格模式
- 遵循 ESLint 配置
- 使用 Tailwind CSS 进行样式开发
- 组件使用函数式组件 + Hooks

**后端**:
- 使用 Python 3.12+ 特性
- 遵循 PEP 8 代码规范
- 使用 FastAPI 的依赖注入和类型注解
- 异步编程优先

### 目录结构

```
rightify/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── app/             # Next.js App Router
│   │   ├── components/      # 可复用组件
│   │   └── contexts/        # React Context
│   └── public/              # 静态资源
├── backend/                 # 后端项目
│   ├── agents/              # AI Agent 实现
│   ├── tools/               # 工具函数
│   ├── utils/               # 工具类
│   ├── config.py            # 配置文件
│   └── main.py              # 应用入口
├── logs/                    # 日志文件
├── tests/                   # 测试文件
├── uploads/                 # 上传文件
├── start.sh                 # 启动脚本
├── stop.sh                  # 停止脚本
├── pyproject.toml           # Python 项目配置
└── project_rules.md         # 项目规范文档
```

### 环境配置

1. 复制 `.env.example` 为 `.env`
2. 配置必要的环境变量（API Keys 等）
3. 确保 Python 3.12+ 和 Node.js 18+ 已安装
4. 安装 `uv`: `pip install uv`

### 日志管理

- 前端日志: `logs/frontend.log`
- 后端日志: `logs/backend.log`
- 实时查看日志: `tail -f logs/frontend.log` 或 `tail -f logs/backend.log`

## 注意事项

1. **依赖管理**: 严格使用 `uv` 管理 Python 依赖，不要使用 `pip` 直接安装
2. **端口冲突**: 确保 3000 和 8001 端口未被占用
3. **环境变量**: 不要将 `.env` 文件提交到版本控制
4. **日志文件**: 日志文件已在 `.gitignore` 中排除
5. **进程管理**: 使用提供的脚本启动和停止服务，避免手动管理进程

---

**最后更新**: 2024年12月
**维护者**: AI Team