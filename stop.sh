#!/bin/bash

# Rightify 项目停止脚本
# 停止前端和后端服务

echo "🛑 停止 Rightify 智能法律咨询系统..."
echo "================================"

# 从PID文件读取进程ID并停止服务
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "🔧 停止后端服务 (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        echo "✅ 后端服务已停止"
    else
        echo "⚠️  后端服务已经停止"
    fi
    rm -f .backend.pid
else
    echo "⚠️  未找到后端服务PID文件"
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "🎨 停止前端服务 (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        echo "✅ 前端服务已停止"
    else
        echo "⚠️  前端服务已经停止"
    fi
    rm -f .frontend.pid
else
    echo "⚠️  未找到前端服务PID文件"
fi

# 额外清理：通过端口查找并停止可能的残留进程
echo "🧹 清理可能的残留进程..."

# 停止占用3000端口的进程（前端）
FRONTEND_PIDS=$(lsof -ti:3000 2>/dev/null)
if [ ! -z "$FRONTEND_PIDS" ]; then
    echo "🎨 发现前端残留进程，正在清理..."
    echo $FRONTEND_PIDS | xargs kill -9 2>/dev/null
fi

# 停止占用8001端口的进程（后端）
BACKEND_PIDS=$(lsof -ti:8001 2>/dev/null)
if [ ! -z "$BACKEND_PIDS" ]; then
    echo "🔧 发现后端残留进程，正在清理..."
    echo $BACKEND_PIDS | xargs kill -9 2>/dev/null
fi

echo ""
echo "✅ 所有服务已停止"
echo "================================"