# 🎬 Dify Video Storytelling & Multi-Agent Pipelines

This directory contains the production-grade **Dify DSL YAML** conversion of all 3 video storytelling pipelines, replacing Flowise with native Dify conversation state variables, assigner nodes, and deterministic branching.

---

## 📁 Directory Structure

```
dify_workflows/
├── flows/
│   ├── 00_video_preplanning_pipeline.yml     # Storyboard & Creative Strategy Workflow (26 Nodes, 25 Edges)
│   ├── 01_post_production_execution_flow.yml # A-Roll/B-Roll/SFX/Color Execution Workflow (28 Nodes, 27 Edges)
│   └── 02_speed_ramp_viral_flow.yml          # Speed Ramp & Viral Effects Workflow (20 Nodes, 19 Edges)
├── scripts/
│   ├── convert_flowise_to_dify.py            # Automated Flowise-to-Dify converter
│   └── validate_dify_dsl.py                  # Dify DSL YAML schema validator
├── run_dify.sh                               # 1-Click launcher for local Dify instance (Docker)
└── README.md                                 # Documentation & setup guide
```

---

## 🚀 How to Launch Dify (1 Click)

### Step 1: Ensure `gemini-web-to-api` Proxy is Running
Make sure your Gemini proxy is running on port 4981:
```bash
# In your gemini-web-to-api directory
go run cmd/server/main.go
```

### Step 2: Start Dify
From this workspace, run:
```bash
./dify_workflows/run_dify.sh
```
Then open **`http://localhost`** in your browser. (First-time launch will ask you to create an admin account).

---

## ⚙️ How to Connect `gemini-web-to-api` in Dify

1. In Dify, click your **Profile icon** (top right) $\rightarrow$ **Settings**.
2. Go to **Model Provider** $\rightarrow$ Click **OpenAI-API-compatible** $\rightarrow$ **Add Model**.
3. Configure the fields:
   * **Model Type**: `LLM`
   * **Model Name**: `gemini-2.0-flash`
   * **Server URL**: `http://host.docker.internal:4981/openai/v1` *(if using Docker)* or `http://localhost:4981/openai/v1`
   * **API Key**: `not-needed` (or any string)
4. Click **Save**.

---

## 📥 How to Import Your Flows into Dify (1 Click)

1. Go to the **Studio** tab in Dify.
2. Click **Create from DSL file** (or **Import DSL**).
3. Select any of the converted workflows from `dify_workflows/flows/`:
   * `00_video_preplanning_pipeline.yml`
   * `01_post_production_execution_flow.yml`
   * `02_speed_ramp_viral_flow.yml`
4. The complete multi-agent pipeline will load with all 20–28 nodes, conversation state variables, and prompt templates!
5. Click **Preview / Run** in the top right to start running your workflows!

---

## 🧠 Why Dify State Management Outperforms Flowise

1. **Persistent Conversation Variables**: State variables (`critique_grade`, `revision_count`, `storyboard`, etc.) are backed by database storage — eliminating Flowise's VM2 sandbox state loss.
2. **Dedicated Variable Assigner Nodes**: Explicit visual nodes commit LLM outputs to state cleanly (`assigned_variable_selector: [conversation, critique_grade]`).
3. **Native If-Else Branching**: Real boolean conditions (`critique_grade contains "A"`) that route with 100% reliability.
4. **Zero Tool-Calling Schema Crashes**: Compatible with any OpenAI-compatible API proxy without LangChain Zod parser failures.
