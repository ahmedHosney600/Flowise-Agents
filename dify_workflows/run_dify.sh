#!/bin/bash
# -----------------------------------------------------------------------------
# 1-Click Setup & Launch Script for Local Dify Instance
# Automatically clones official Dify repository and starts via Docker Compose
# -----------------------------------------------------------------------------

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "============================================================"
echo "🚀 Starting Dify AI Workflow Studio..."
echo "============================================================"

# 1. Check Docker status
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ Error: Docker is not installed or not in PATH."
    echo "Please install Docker Desktop for Mac from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "⚠️ Warning: Docker Desktop is not running. Please open Docker Desktop and retry."
    exit 1
fi

# 2. Check local Gemini Proxy
PROXY_URL="http://localhost:4981/openai/v1/models"
echo "🔍 Checking gemini-web-to-api proxy at $PROXY_URL..."
if curl -s --connect-timeout 3 "$PROXY_URL" > /dev/null; then
    echo "🟢 SUCCESS: Connected to gemini-web-to-api proxy on port 4981!"
else
    echo "⚠️ Note: Proxy not responding on port 4981. Ensure 'go run cmd/server/main.go' is running."
fi

# 3. Clone or update Dify docker directory
DIFY_DIR="$SCRIPT_DIR/dify_source"
if [ ! -d "$DIFY_DIR" ]; then
    echo "📦 Cloning official Dify repository..."
    git clone --depth 1 https://github.com/langgenius/dify.git "$DIFY_DIR"
fi

cd "$DIFY_DIR/docker"

if [ ! -f ".env" ]; then
    cp .env.example .env
fi

echo "🐳 Starting Dify Docker containers in the background..."
docker compose up -d

echo "============================================================"
echo "🌐 Dify is ready! Open in your browser:"
echo "👉 http://localhost"
echo "============================================================"
echo "To import your workflows:"
echo "1. Go to Studio -> Create from DSL file"
echo "2. Select any .yml file from dify_workflows/flows/"
echo "============================================================"
