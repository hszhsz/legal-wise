#!/bin/bash

# Rightify 项目启动脚本
# 同时启动前端和后端服务

echo "🚀 启动 Rightify 智能法律咨询系统..."
echo "================================"

# 检查是否安装了必要的依赖
echo "📦 检查依赖..."

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查 uv (Python 包管理器)
if ! command -v uv &> /dev/null; then
    echo "❌ 错误: 未找到 uv，请先安装 uv (pip install uv)"
    exit 1
fi

echo "✅ 依赖检查完成"
echo ""

# 创建日志目录
mkdir -p logs

# 启动后端服务
echo "🔧 启动后端服务 (端口: 8001)..."
cd backend
uv run uvicorn main:app --host 0.0.0.0 --port 8001 --reload > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 3

# 检查后端是否启动成功
if ! curl -s http://localhost:8001/api/health > /dev/null; then
    echo "⚠️  后端服务可能需要更多时间启动，继续启动前端..."
else
    echo "✅ 后端服务启动成功"
fi

echo ""

# 启动前端服务
echo "🎨 启动前端服务 (端口: 3000)..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# 等待前端启动
echo "⏳ 等待前端服务启动..."
sleep 5

echo ""
echo "🎉 服务启动完成!"
echo "================================"
echo "📱 前端地址: http://localhost:3000"
echo "🔧 后端地址: http://localhost:8001"
echo "📊 后端健康检查: http://localhost:8001/api/health"
echo "📝 日志文件:"
echo "   - 前端日志: logs/frontend.log"
echo "   - 后端日志: logs/backend.log"
echo ""
echo "💡 提示:"
echo "   - 按 Ctrl+C 停止所有服务"
echo "   - 使用 'tail -f logs/frontend.log' 查看前端日志"
echo "   - 使用 'tail -f logs/backend.log' 查看后端日志"
echo ""

# 保存进程ID到文件，方便后续停止
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# 等待用户中断
trap 'echo "\n🛑 正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f .backend.pid .frontend.pid; echo "✅ 所有服务已停止"; exit 0' INT

# 保持脚本运行
echo "🔄 服务正在运行中... (按 Ctrl+C 停止)"
while true; do
    sleep 1
done