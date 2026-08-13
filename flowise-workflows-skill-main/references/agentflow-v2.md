# AgentFlow V2 Reference

Detailed reference for Flowise AgentFlow V2 architecture, nodes, Flow State, and workflow patterns.

## Architecture Overview

AgentFlow V2 uses natively-built standalone nodes with explicit workflow orchestration. Key features:
- **Agent-to-agent communication** — Supervisor delegates to workers, workers return results
- **Human-in-the-loop** — Execution pauses at checkpoints, resumes after human input
- **Shared Flow State** — Data exchange between any nodes via `$flow.state`
- **Streaming** — SSE for real-time LLM response streaming
- **MCP Tools** — Model Context Protocol tools as first-class citizens
- **Sub-flows** — Execute other chatflows/agentflows as nodes

## Flow State

Flow State is a shared data structure accessible by all nodes. Define it in the Start node and reference/update it anywhere.

### Defining State (Start Node)
```json
{
  "state": {
    "task_status": "pending",
    "results": [],
    "current_step": 0
  }
}
```

### Reading State
In any node's configuration, reference state with: `$flow.state.task_status`

### Updating State
Use the Set Variable node or LLM/Agent nodes with output-to-state mapping.

## Node Details

### Start Node (`agentFlowV2Start`)
- **Purpose**: Entry point for the workflow
- **Outputs**: User's input message, any defined input variables
- **Config**: Input variables (name, type), Flow State definition
- **Usage**: Every V2 workflow must begin with exactly one Start node

### LLM Node (`agentFlowV2LLM`)
- **Purpose**: Generate text or structured JSON using an LLM
- **Inputs**: Messages/Input from previous nodes or state, chat model config
- **Outputs**: Plain text or structured JSON (based on Output Schema)
- **Config**: 
  - Model selection (provider + model name)
  - System message / prompt
  - Temperature, max tokens
  - JSON Structured Output Schema (optional)
  - Return Response As: User or Assistant message
- **When to use**: Direct LLM calls without tool access. Use for text generation, classification, summarization, data extraction.

### Agent Node (`agentFlowV2Agent`)
- **Purpose**: Autonomous agent with reasoning, planning, tool use
- **Inputs**: Messages/Input, tools, document stores, knowledge bases
- **Outputs**: Agent's final response after reasoning cycle
- **Config**:
  - Model selection
  - System message
  - Tools: registered Flowise tools (each can have "Require Human Input" flag)
  - Document Stores: pre-configured knowledge sources with descriptions
  - Vector Embeddings: external vector stores
  - Max Iterations: limit reasoning cycles
- **When to use**: When the workflow needs dynamic decision-making, tool selection, or multi-step reasoning.

### Tool Node (`agentFlowV2Tool`)
- **Purpose**: Deterministic tool execution (no LLM reasoning)
- **Inputs**: Tool selection, input arguments (mapped from prior outputs or state)
- **Outputs**: Tool execution result
- **Config**: 
  - Tool selection (dropdown of registered tools)
  - Input Arguments: map each param to a value or variable
- **When to use**: When you know exactly which tool to run at a specific point. Unlike Agent nodes, this doesn't involve LLM decision-making.

### Condition Node (`agentFlowV2Condition`)
- **Purpose**: Route workflow based on conditions
- **Inputs**: Output from previous node
- **Outputs**: Multiple branches (if/else if/else)
- **Config**: Condition list with comparison operators
- **Conditions can check**: Previous node output, Flow State values, string matching, numeric comparison
- **When to use**: Branching logic — route to different agents/tools based on classification, user input, or state.

### Human Input Node (`agentFlowV2HumanInput`)
- **Purpose**: Pause execution for human interaction
- **Inputs**: Context from previous node
- **Outputs**: Human's response
- **Config**: Prompt message displayed to the user
- **When to use**: Approval gates, clarification requests, human oversight of agent actions. Checkpoints are saved, so the flow survives app restarts.

### Iteration Node (`agentFlowV2Iteration`)
- **Purpose**: Loop over array items
- **Inputs**: Array to iterate (from state or prior node output)
- **Outputs**: Individual items passed to loop body
- **Config**: Array source expression, loop body nodes
- **When to use**: Processing lists — sending emails to multiple recipients, creating multiple records, analyzing items in batch.

### HTTP Node (`agentFlowV2HTTP`)
- **Purpose**: Make HTTP requests to external APIs
- **Inputs**: Configuration + data from prior nodes
- **Outputs**: Response body
- **Config**: URL, Method (GET/POST/PUT/DELETE), Headers, Body, Query Params
- **URL variables**: Use `{{ variable }}` syntax for dynamic URLs
- **When to use**: Direct API calls without wrapping in a tool.

### Custom JavaScript Node (`agentFlowV2CustomJS`)
- **Purpose**: Execute custom JavaScript logic
- **Inputs**: Variables from prior nodes or state
- **Outputs**: Return value of the function
- **Config**: JavaScript code, input variable definitions
- **When to use**: Data transformation, custom logic, parsing, computation that doesn't fit standard nodes.

### Execute Flow Node (`agentFlowV2ExecuteFlow`)
- **Purpose**: Run another Chatflow or AgentFlow as a sub-flow
- **Inputs**: Input message, optional override config
- **Outputs**: Sub-flow's response
- **Config**: 
  - Select Flow: choose from existing flows
  - Input: data passed to the sub-flow
  - Override Config: JSON to override sub-flow settings
  - Base URL: for remote Flowise instances
  - Return Response As: User or Assistant message
- **When to use**: Modular workflow design — reuse existing flows as components.

### End Node (`agentFlowV2End`)
- **Purpose**: Terminal node, sends final output to user
- **Inputs**: Final value from prior node
- **Config**: Output value expression
- **When to use**: Every workflow branch should terminate with an End node.

### Set Variable Node (`agentFlowV2SetVariable`)
- **Purpose**: Update Flow State
- **Inputs**: Value from prior nodes
- **Config**: Variable name (key in state), value expression
- **When to use**: Persist intermediate results, counters, flags.

## Common Patterns

### Linear Pipeline
```
Start → LLM → End
```

### Branching
```
Start → LLM → Condition → [Branch A: Agent] → End
                        → [Branch B: Tool] → End
```

### Supervisor-Worker Loop
```
Start → Supervisor Agent → Condition (done?)
                               → No: Worker Agent → Supervisor Agent (loop)
                               → Yes: End
```

### Human Approval Gate
```
Start → Agent (proposes action) → Human Input → Condition (approved?)
                                                    → Yes: Tool (execute) → End
                                                    → No: End
```

### Iterative Processing
```
Start → LLM (generate list) → Iteration → HTTP (per item) → End
```

### Sub-flow Orchestration
```
Start → Condition (route) → Execute Flow A → End
                          → Execute Flow B → End
```

## V2 JSON Differences

AgentFlow V2 uses the same top-level JSON structure as Chatflows but with:
- `"type": "AGENTFLOW"` instead of `"CHATFLOW"`
- V2-specific node names (`agentFlowV2Start`, `agentFlowV2Agent`, etc.)
- Flow State definition in the Start node's `data.inputs`
- Node outputs reference previous nodes via `{{ previousNodeId }}` syntax

## Best Practices

1. **Start simple**: Begin with a linear flow and add complexity incrementally
2. **Use Flow State strategically**: Only for data that needs to cross branches or survive loops
3. **Keep JSON schemas simple**: Only define output schemas when downstream nodes need structured data
4. **Agent vs LLM**: Use Agent when tools are needed; use LLM for pure text processing
5. **Tool vs Agent-with-tool**: Use Tool node for deterministic execution; Agent node when the LLM should decide whether/how to use tools
6. **Human-in-the-loop**: Add for any action with real-world consequences (sending emails, making purchases, database writes)
7. **Error handling**: Use Condition nodes to check for errors and route to fallback paths
8. **Streaming**: Enable for user-facing responses to improve perceived latency
