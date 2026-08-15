# 🎬 Langflow Video Storytelling & Multi-Agent Pipelines

This directory contains the production-grade **Langflow** conversion of all 3 video storytelling pipelines, completely replacing Flowise with Python-native components and deterministic state handling.

---

## 📁 Directory Structure

```

├── flows/
│   ├── 00_video_preplanning_pipeline.json     # Storyboard & Creative Strategy Flow
│   ├── 01_post_production_execution_flow.json # A-Roll/B-Roll/SFX/Color Execution Flow
│   └── 02_speed_ramp_viral_flow.json          # Speed Ramp & Viral Effects Flow
├── components/
│   └── critique_evaluator.py                  # Custom Python Audit Evaluator & Loop Guard
├── scripts/
│   ├── generate_langflow_flows.py             # Re-generates flows from prompt templates
│   ├── validate_flows.py                      # Automated structural validator for all flows
│   └── run_flow.py                            # Direct terminal runner using OpenAI proxy
├── run_langflow.sh                            # 1-Click launcher for Langflow UI (Port 7860)
└── README.md                                  # Documentation & user guide
```

---

## 🚀 How to Launch in 1 Click

### 1. Ensure `gemini-web-to-api` Proxy is Running
Make sure your Gemini proxy is running on port 4981:
```bash
# In your gemini-web-to-api directory
go run cmd/server/main.go
```

### 2. Start Langflow UI
From this workspace, run:
```bash
./run_langflow.sh
```
Or manually:
```bash
source .venv/bin/activate
python -m langflow run --port 7860
```
Open **`http://localhost:7860`** in your browser.

---

## 📥 How to Import Flows into Langflow UI

1. Open **`http://localhost:7860`**
2. Click the **"New Flow"** button in the top right $\rightarrow$ select **"Import Flow"**.
3. Choose any of the 3 converted flows from `flows/`:
   * `00_video_preplanning_pipeline.json`
   * `01_post_production_execution_flow.json`
   * `02_speed_ramp_viral_flow.json`
4. The visual canvas will load with all 8–11 agent nodes, prompts, connections, and the local `gemini-2.0-flash` proxy model pre-configured!
5. Click **"Playground"** or **"Run"** to execute the pipeline!

---

## ⚡ Direct Command-Line Execution

If you ever want to run a pipeline quickly from the terminal without opening the browser:
```bash
source .venv/bin/activate
python scripts/run_flow.py
```
This executes the 6-agent Speed Ramp pipeline sequentially against your local Gemini proxy and saves the master deliverable markdown file to `outputs/speed_ramp_viral_package.md`.

---

## 🛠️ Workflows Overview

### 1. `00_video_preplanning_pipeline.json`
* **Agent 01**: Creative Strategy Director (Hook angle, audience retention, narrative tension)
* **Agent 02**: Storyboard Designer (Visual shots, camera angles, shot duration)
* **Agent 03**: Pacing & Energy Map Designer (Cut frequency, cognitive load, drop alignments)
* **Agent 04**: Self-Critique & Auditor (Retention, narrative, and pacing QA)
* **Evaluator**: `CritiqueEvaluator` (Letter grade `A+`, `A`, `B`, `C`, `D` extraction & loop guard)
* **Agent 05**: Final Pre-Planning Package (Master production blueprint)

### 2. `01_post_production_execution_flow.json`
* **Agent 01**: A-Roll Assembly Editor (Dialogue & storyline)
* **Agent 02**: B-Roll & Visual Pacing (Cutaways and rhythm)
* **Agent 03**: Graphic Design & Motion GFX (Lower thirds and title overlays)
* **Agent 04**: Sound Design & SFX Mix (Audio balance, risers, and impact hits)
* **Agent 05**: Color & Delivery Specs (LUTs and master exports)
* **Agent 06**: Self-Critique & Auditor (Quality assurance check)
* **Agent 07**: Final Execution Package (Timeline master plan)

### 3. `02_speed_ramp_viral_flow.json`
* **Agent 01**: Clip Arrangement Designer (Beat grid mapping and in/out points)
* **Agent 02**: Speed Ramp Designer (Graph editor curves, bezier handles, freeze frames)
* **Agent 03**: Viral Effects & Transitions (Turbulent displace, glow hits, masking)
* **Agent 04**: Sound Design & Finishing (Drop impacts, whooshes, and shopping list)
* **Agent 05**: Self-Critique & Auditor (Beat sync QA, curve physics, loop-ability)
* **Evaluator**: `CritiqueEvaluator` (Letter grade `A+`, `A`, `B`, `C`, `D` extraction)
* **Agent 06**: Final Viral Edit Package (Full editor cheatsheet)

---

## 🧠 Why Langflow Outperforms Flowise

1. **Deterministic State Handling**: Data is passed as structured Python objects rather than brittle VM2 sandbox strings.
2. **Zero Schema Crashes**: Compatible with any OpenAI-compatible API base URL (`gemini-web-to-api`) without crashing on LangChain tool-calling schemas.
3. **Easy AI Customization**: All flows and custom Python components are 100% transparent, editable, and modular.
