---
name: flowise-workflows
description: Generate Flowise AI workflows — chatflows, agentflows (V1 and V2), and multi-agent systems. Produces importable JSON files, step-by-step build instructions, and visual diagrams. Includes pre-built templates for common patterns (RAG, chatbot, multi-agent supervisor, API integration) and custom workflow generation from user descriptions. Use this skill whenever the user mentions Flowise, chatflows, agentflows, visual AI workflow builders, LangChain visual builders, no-code AI agent builders, or wants to create AI agent pipelines that can be imported into Flowise. Also trigger when the user asks for help designing node-based AI workflows, connecting LLMs with tools/memory/vector stores visually, or building sequential/multi-agent systems with a drag-and-drop interface.
---

# Flowise Workflow Generator

Generate production-ready Flowise workflows as importable JSON, with step-by-step guidance and visual diagrams.

## Overview

Flowise is an open-source visual AI workflow builder. Workflows are stored as JSON containing `nodes` and `edges`. This skill produces:

1. **Importable JSON files** — ready to load via Flowise's "Load Chatflow" feature
2. **Step-by-step instructions** — how to build the workflow manually in the Flowise UI
3. **Visual diagrams** — Mermaid or SVG diagrams showing node connections and data flow

## Before You Start

Read the appropriate reference files based on what the user needs:

- **Always read first**: `references/json-structure.md` — the JSON schema for Flowise chatflows
- **For node selection**: `references/nodes.md` — catalog of available nodes by category
- **For templates**: `references/templates.md` — pre-built workflow patterns
- **For AgentFlow V2**: `references/agentflow-v2.md` — V2-specific nodes and patterns

## Workflow Types

### Chatflows (LangChain-based)
The original Flowise workflow type. Chains together LangChain components: Chat Models, Prompts, Memory, Tools, Vector Stores, Document Loaders, Embeddings, and Output Parsers. Best for straightforward LLM pipelines like RAG, conversational chatbots, and simple tool-using agents.

### AgentFlow V1 — Sequential Agents (Legacy)
Built on LangGraph. Uses specialized nodes: Start, Agent, LLM, Tool, Condition, State, Loop, and End. Workflows form a directed cyclic graph (DCG). Good for multi-step agentic workflows with conditional logic.

### AgentFlow V2 (Current)
The latest architecture. Natively-built standalone nodes with explicit workflow orchestration. Supports agent-to-agent communication, human-in-the-loop with checkpoints, shared Flow State, streaming, MCP tools, and sub-flow execution. Preferred for new multi-agent systems.

## Generation Process

### Step 1: Understand the User's Goal

Ask clarifying questions if needed:
- What is the workflow supposed to accomplish?
- Which LLM provider (OpenAI, Anthropic, Google, local models)?
- Does it need memory/conversation history?
- Does it need RAG (document retrieval)?
- Does it need external tool access (APIs, web search, etc.)?
- Single agent or multi-agent?
- Should it match a known template, or is it fully custom?

### Step 2: Select Workflow Type

| Use Case | Recommended Type |
|---|---|
| Simple chatbot, RAG, translation | Chatflow |
| Multi-step agent with tool use | AgentFlow V2 |
| Multi-agent supervisor/worker | AgentFlow V2 |
| Legacy compatibility | AgentFlow V1 (Sequential) |

### Step 3: Design the Node Graph

Read `references/nodes.md` to select appropriate nodes. Design the connections (edges) between them. Every workflow needs:

- **An entry point** — Chatflows start from the chain/agent node; AgentFlows use a Start node
- **An LLM** — ChatOpenAI, ChatAnthropic, ChatGoogleGenerativeAI, etc.
- **An output** — The final response node

Common additions:
- **Memory** — BufferMemory, WindowBufferMemory, Redis, Postgres, Zep, etc.
- **Tools** — CustomTool, SerpAPI, Calculator, RequestsGet, MCP tools
- **Vector Store + Embeddings** — For RAG pipelines
- **Document Loaders** — PDF, CSV, text files, web scraping
- **Output Parsers** — Structured JSON output

### Step 4: Generate the JSON

Read `references/json-structure.md` for the exact JSON schema. Generate valid Flowise chatflow JSON with:

- Unique `id` for each node (use format like `node_0`, `node_1`, etc.)
- Correct `data.name` matching Flowise's registered component names exactly
- Proper `data.type` matching the node category
- `data.inputs` with the right parameter names and connection references
- `edges` connecting outputs to inputs with proper `sourceHandle` and `targetHandle`

The JSON must be a complete, self-contained chatflow object with a `nodes` array and `edges` array.

**Critical**: Node `data.name` values must exactly match Flowise's internal component registry names. Refer to `references/nodes.md` for the canonical list.

### Step 5: Write Build Instructions

Provide clear step-by-step instructions for building the same workflow manually:

1. Start each step with which node to drag from which category
2. Specify exact configuration values (model name, temperature, prompts)
3. Describe which output handle connects to which input handle
4. Note where credentials need to be configured
5. End with "Save and test"

### Step 6: Generate Visual Diagram

Create a Mermaid diagram or SVG showing the workflow architecture:

```
graph LR
    A[ChatOpenAI] --> C[ConversationChain]
    B[BufferMemory] --> C
    C --> D[Response]
```

For complex workflows, use a top-down layout (`graph TD`) and color-code node types.

## Output Format

For every workflow generation, deliver all three outputs:

### 1. JSON File
Save as `.json` in the outputs directory. The file should be directly importable into Flowise.

### 2. Build Instructions
Write clear, numbered steps in markdown. Include screenshots descriptions where helpful.

### 3. Visual Diagram
Generate a Mermaid diagram showing the node graph. For complex flows, also generate an SVG using the visualizer tool.

## Template Selection

When the user's request matches a common pattern, start from a template (see `references/templates.md`) and customize. Common templates:

- **Simple Chatbot** — LLM + Memory + ConversationChain
- **RAG Q&A** — Document Loader + Text Splitter + Embeddings + Vector Store + Retrieval QA Chain
- **Tool Agent** — LLM + Tools + Agent (OpenAI Function Agent or ReAct)
- **Multi-Agent Supervisor** — Start → Supervisor Agent → Worker Agents → End
- **API Integration** — Agent + HTTP/Custom Tools for external API calls
- **Conversational RAG** — RAG + Conversation Memory for follow-up questions

## Key Conventions

### Node ID Format
Use descriptive IDs: `chatOpenAI_0`, `bufferMemory_0`, `conversationChain_0`

### Credential Placeholders
Never include real API keys. Use empty credential references that the user fills in after import:
```json
"credential": ""
```

### Position Layout
Space nodes on the canvas for readability:
- Left-to-right flow for simple chains
- Top-to-bottom for complex multi-branch flows  
- ~300px horizontal spacing, ~150px vertical spacing between nodes

### Parameter Defaults
Use sensible defaults unless the user specifies otherwise:
- Temperature: 0.7 for creative, 0 for factual/deterministic
- Model: gpt-4o (or user's preferred provider)
- Max Tokens: 2048
- Memory window: 5 messages for WindowBufferMemory

## Error Prevention

- Validate that every edge connects a real output handle to a real input handle
- Ensure no orphan nodes (every node must be connected)
- Verify that required inputs are either connected or have default values
- Check that node names match Flowise's component registry exactly
- For RAG flows, ensure embedding dimensions match between the embedding model and vector store

## Delivering the Output

1. Generate the JSON file and save to `/mnt/user-data/outputs/`
2. Present the file using `present_files`
3. Include the build instructions and diagram in the conversation response
4. If the workflow is complex, also generate a Mermaid or SVG diagram using the visualizer
