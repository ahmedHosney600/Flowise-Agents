#!/bin/bash
# -----------------------------------------------------------------------------
# Langflow 1-Click Launcher for Video Storytelling Workflows
# Automatically activates the workspace .venv and runs Langflow on port 7860
# -----------------------------------------------------------------------------

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR" && pwd)"

echo "============================================================"
echo "🚀 Starting Langflow Video Storytelling Studio..."
echo "============================================================"

# Check virtual environment
if [ -d "$ROOT_DIR/.venv" ]; then
    echo "✓ Activating virtual environment: $ROOT_DIR/.venv"
    source "$ROOT_DIR/.venv/bin/activate"
else
    echo "⚠️ .venv not found. Creating Python 3.12 environment via uv..."
    if command -v uv >/dev/null 2>&1; then
        uv venv --python 3.12 "$ROOT_DIR/.venv"
        source "$ROOT_DIR/.venv/bin/activate"
        uv pip install langflow openai
    else
        python3 -m venv "$ROOT_DIR/.venv"
        source "$ROOT_DIR/.venv/bin/activate"
        pip install langflow openai
    fi
fi

# Test local Gemini proxy connectivity
PROXY_URL="http://localhost:4981/openai/v1/models"
echo "🔍 Checking gemini-web-to-api proxy at $PROXY_URL..."
if curl -s --connect-timeout 3 "$PROXY_URL" > /dev/null; then
    echo "🟢 SUCCESS: Connected to gemini-web-to-api proxy on port 4981!"
else
    echo "⚠️ WARNING: Proxy not reachable at http://localhost:4981. Ensure 'go run cmd/server/main.go' is running."
fi

# Run validation on flow JSONs
echo "📋 Validating workflows..."
python "$SCRIPT_DIR/scripts/validate_flows.py"

echo "============================================================"
echo "🌐 Launching Langflow UI on http://localhost:7860"
echo "============================================================"

# Configure SSRF protection to allow local model proxy (localhost:4981)
export LANGFLOW_SSRF_ALLOWED_HOSTS="127.0.0.1,localhost,0.0.0.0,::1"
export LANGFLOW_SSRF_PROTECTION_ENABLED="false"

# Start Langflow server
python -m langflow run --port 7860 --host 0.0.0.0
