# 🔄 Flowise Workflow Generator — Claude Skill

A Claude skill that generates production-ready [Flowise AI](https://flowiseai.com/) workflows — importable JSON files, step-by-step build instructions, and visual diagrams.

## ✨ What It Does

Describe what you want your AI workflow to do, and this skill generates:

1. **Importable JSON** — Load directly into Flowise via *Settings → Load Chatflow*
2. **Step-by-step instructions** — How to build the same workflow manually in the Flowise UI
3. **Visual diagrams** — Mermaid/SVG showing node connections and data flow

## 🧩 Supported Workflow Types

| Type | Description |
|---|---|
| **Chatflows** | LangChain-based chains — RAG, chatbots, Q&A, translation |
| **AgentFlow V2** | Latest multi-agent architecture with human-in-the-loop, MCP tools, streaming |
| **AgentFlow V1** | Legacy Sequential Agents (LangGraph-based) |

## 📦 Pre-Built Templates

Comes with 10 ready-to-customize templates:

- 💬 Simple Chatbot (LLM + Memory)
- 📄 RAG Q&A (Document → Vector Store → Retrieval Chain)
- 🔁 Conversational RAG (RAG + follow-up questions)
- 🛠️ Tool Agent (OpenAI Function Agent + tools)
- 👥 Multi-Agent Supervisor (V2 — Supervisor → Workers)
- 🌐 API Integration Agent
- 🕸️ Web Scraping RAG
- 📑 PDF Q&A
- 🗃️ SQL Database Agent
- 🙋 Human-in-the-Loop (V2 — approval gates)

## 📂 Skill Structure

```
flowise-workflows/
├── SKILL.md                          # Main skill instructions
└── references/
    ├── json-structure.md             # Flowise JSON schema & examples
    ├── nodes.md                      # 100+ node catalog by category
    ├── templates.md                  # 10 pre-built workflow patterns
    └── agentflow-v2.md              # V2 architecture deep dive
```

## 🚀 Installation

### Option 1: Upload as a Custom Skill in Claude

1. Download this repo as a `.zip`
2. In Claude, go to **Settings → Skills**
3. Upload the skill folder

### Option 2: Use with Claude Code

Place the `flowise-workflows/` folder in your skills directory:

```bash
# Clone this repo
git clone https://github.com/drdshivajiraju-ctrl/flowise-workflows-skill.git

# Copy to your skills directory
cp -r flowise-workflows-skill/flowise-workflows /path/to/your/skills/
```

## 💡 Example Prompts

Once the skill is installed, try prompts like:

- *"Create a Flowise RAG chatbot for my PDF documents using OpenAI"*
- *"Build a multi-agent workflow where a supervisor delegates to research and writing agents"*
- *"Generate a Flowise chatflow that connects to my REST API with conversation memory"*
- *"Make a Flowise workflow for a customer support bot with web search and human approval"*

## 🔗 Resources

- [Flowise Documentation](https://docs.flowiseai.com/)
- [Flowise GitHub](https://github.com/FlowiseAI/Flowise)
- [AgentFlow V2 Docs](https://docs.flowiseai.com/using-flowise/agentflowv2)

## 📄 License

MIT — free to use, modify, and distribute.

## 🤝 Contributing

PRs welcome! If you'd like to add new templates, update node catalogs, or improve the skill instructions, feel free to open a pull request.
# flowise-workflows-skill
