#!/bin/bash

# Restart FastAPI Server Script
# Kills existing server and starts a new one with updated environment

cd /Users/oabolade/agents_app_build/lead_sniper_ai

echo "🔄 Restarting FastAPI Server..."
echo ""

# Kill existing server on port 8000
echo "Stopping existing server..."
lsof -ti:8000 2>/dev/null | xargs kill -9 2>/dev/null
sleep 2

# Check if port is free
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "⚠️  Port 8000 still in use. Trying again..."
    sleep 2
    lsof -ti:8000 2>/dev/null | xargs kill -9 2>/dev/null
fi

echo "✅ Server stopped"
echo ""

# Activate venv and start server
echo "Starting server with new environment..."
source venv/bin/activate

# Start server in background
nohup python api/run_server.py > /tmp/fastapi_server.log 2>&1 &
SERVER_PID=$!

sleep 3

# Check if server started
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server started (PID: $SERVER_PID)"
    echo ""
    echo "📋 Server logs: tail -f /tmp/fastapi_server.log"
    echo "🌐 API URL: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "⏳ Waiting for server to be ready..."
    sleep 2
    
    # Test health endpoint
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Server is healthy and ready!"
        echo ""
        curl -s http://localhost:8000/health | python3 -m json.tool
    else
        echo "⚠️  Server may still be starting. Check logs: tail -f /tmp/fastapi_server.log"
    fi
else
    echo "❌ Server failed to start. Check logs: tail -f /tmp/fastapi_server.log"
    exit 1
fi
