# Flowise Chatflow JSON Structure

This document defines the JSON schema for Flowise chatflows. All workflows — chatflows, agentflows V1 and V2 — use this same top-level structure.

## Top-Level Schema

```json
{
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

When exported from Flowise, the file is wrapped in a chatflow object:

```json
{
  "id": "uuid-string",
  "name": "My Workflow",
  "flowData": "{\"nodes\":[...],\"edges\":[...]}",
  "deployed": false,
  "isPublic": false,
  "apikeyid": "",
  "chatbotConfig": "{}",
  "apiConfig": "{}",
  "analytic": "{}",
  "speechToText": "{}",
  "category": "",
  "type": "CHATFLOW",
  "createdDate": "2024-01-01T00:00:00.000Z",
  "updatedDate": "2024-01-01T00:00:00.000Z"
}
```

Note: `flowData` is a **stringified** JSON object. When generating for import via "Load Chatflow", provide the inner `{ "nodes": [...], "edges": [...] }` object directly — Flowise will wrap it.

For API creation via `POST /chatflows`, stringify the nodes/edges into `flowData`.

## Node Schema

```json
{
  "id": "chatOpenAI_0",
  "position": { "x": 400, "y": 200 },
  "type": "customNode",
  "data": {
    "id": "chatOpenAI_0",
    "label": "ChatOpenAI",
    "version": 6,
    "name": "chatOpenAI",
    "type": "ChatOpenAI",
    "baseClasses": ["ChatOpenAI", "BaseChatModel", "BaseLLM"],
    "category": "Chat Models",
    "description": "Wrapper around OpenAI large language models that use the Chat endpoint",
    "inputParams": [
      {
        "label": "Connect Credential",
        "name": "credential",
        "type": "credential",
        "credentialNames": ["chatOpenAIApi"]
      },
      {
        "label": "Model Name",
        "name": "modelName",
        "type": "options",
        "default": "gpt-4o"
      },
      {
        "label": "Temperature",
        "name": "temperature",
        "type": "number",
        "default": 0.9
      }
    ],
    "inputAnchors": [],
    "inputs": {
      "modelName": "gpt-4o",
      "temperature": "0.7",
      "credential": ""
    },
    "outputAnchors": [
      {
        "id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLLM",
        "name": "output",
        "label": "ChatOpenAI",
        "type": "ChatOpenAI | BaseChatModel | BaseLLM"
      }
    ],
    "outputs": {},
    "selected": false
  },
  "width": 300,
  "height": 525
}
```

### Key Node Fields

| Field | Description |
|---|---|
| `id` | Unique node ID. Convention: `componentName_index` (e.g., `chatOpenAI_0`) |
| `position` | `{ x, y }` canvas coordinates. Space nodes ~300px apart horizontally |
| `type` | Always `"customNode"` for Flowise nodes |
| `data.id` | Must match the outer `id` |
| `data.label` | Display name shown on canvas |
| `data.name` | **Critical**: Must exactly match Flowise's component registry name |
| `data.type` | The component's class name |
| `data.baseClasses` | Array of class types this node can output as |
| `data.category` | UI category (e.g., "Chat Models", "Memory", "Tools") |
| `data.inputs` | Key-value map of parameter values and connection references |
| `data.inputAnchors` | Defines which input connection points the node exposes |
| `data.outputAnchors` | Defines output connection points |
| `data.inputParams` | Parameter definitions (label, name, type, default) |

### Input Anchors

Input anchors define connection points where other nodes can connect:

```json
{
  "inputAnchors": [
    {
      "label": "Chat Model",
      "name": "model",
      "type": "BaseChatModel",
      "id": "conversationChain_0-input-model-BaseChatModel"
    },
    {
      "label": "Memory",
      "name": "memory",
      "type": "BaseMemory",
      "id": "conversationChain_0-input-memory-BaseMemory"
    }
  ]
}
```

The anchor ID format is: `{nodeId}-input-{paramName}-{type}`

### Output Anchors

```json
{
  "outputAnchors": [
    {
      "id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLLM",
      "name": "output",
      "label": "ChatOpenAI",
      "type": "ChatOpenAI | BaseChatModel | BaseLLM"
    }
  ]
}
```

The anchor ID format is: `{nodeId}-output-{paramName}-{typeList}`

## Edge Schema

```json
{
  "source": "chatOpenAI_0",
  "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLLM",
  "target": "conversationChain_0",
  "targetHandle": "conversationChain_0-input-model-BaseChatModel",
  "type": "buttonedge",
  "id": "chatOpenAI_0-chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLLM-conversationChain_0-conversationChain_0-input-model-BaseChatModel"
}
```

### Key Edge Fields

| Field | Description |
|---|---|
| `source` | ID of the source node |
| `sourceHandle` | Output anchor ID of the source node |
| `target` | ID of the target node |
| `targetHandle` | Input anchor ID of the target node |
| `type` | Always `"buttonedge"` |
| `id` | Concatenation: `{source}-{sourceHandle}-{target}-{targetHandle}` |

### Connection Type Matching

Edges can only connect if the source's output type matches (or is a parent class of) the target's input type. For example:

- `ChatOpenAI` (outputs `BaseChatModel`) → `ConversationChain` (accepts `BaseChatModel`) ✓
- `BufferMemory` (outputs `BaseMemory`) → `ConversationChain` (accepts `BaseMemory`) ✓
- `BufferMemory` (outputs `BaseMemory`) → `ConversationChain` (accepts `BaseChatModel`) ✗

## AgentFlow V2 Nodes

AgentFlow V2 uses the same JSON structure but has its own set of node types:

- `agentFlowV2Start` — Entry point, receives user input
- `agentFlowV2LLM` — LLM processing node
- `agentFlowV2Agent` — Autonomous agent with tool access
- `agentFlowV2Tool` — Deterministic tool execution
- `agentFlowV2Condition` — Conditional branching
- `agentFlowV2HumanInput` — Pause for human input
- `agentFlowV2Iteration` — Loop over arrays
- `agentFlowV2HTTP` — HTTP request node
- `agentFlowV2CustomJS` — Custom JavaScript execution
- `agentFlowV2End` — Terminal node
- `agentFlowV2ExecuteFlow` — Sub-flow execution

AgentFlow V2 workflows use `"type": "AGENTFLOW"` instead of `"CHATFLOW"`.

## Minimal Complete Example

A simple conversational chatbot with memory:

```json
{
  "nodes": [
    {
      "id": "chatOpenAI_0",
      "position": { "x": 100, "y": 200 },
      "type": "customNode",
      "data": {
        "id": "chatOpenAI_0",
        "label": "ChatOpenAI",
        "version": 6,
        "name": "chatOpenAI",
        "type": "ChatOpenAI",
        "baseClasses": ["ChatOpenAI", "BaseChatModel", "BaseLLM"],
        "category": "Chat Models",
        "inputs": {
          "modelName": "gpt-4o",
          "temperature": "0.7",
          "credential": ""
        },
        "outputAnchors": [
          {
            "id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLLM",
            "name": "output",
            "label": "ChatOpenAI",
            "type": "ChatOpenAI | BaseChatModel | BaseLLM"
          }
        ]
      }
    },
    {
      "id": "bufferMemory_0",
      "position": { "x": 100, "y": 500 },
      "type": "customNode",
      "data": {
        "id": "bufferMemory_0",
        "label": "Buffer Memory",
        "version": 2,
        "name": "bufferMemory",
        "type": "BufferMemory",
        "baseClasses": ["BufferMemory", "BaseChatMemory", "BaseMemory"],
        "category": "Memory",
        "inputs": {},
        "outputAnchors": [
          {
            "id": "bufferMemory_0-output-bufferMemory-BufferMemory|BaseChatMemory|BaseMemory",
            "name": "output",
            "label": "BufferMemory",
            "type": "BufferMemory | BaseChatMemory | BaseMemory"
          }
        ]
      }
    },
    {
      "id": "conversationChain_0",
      "position": { "x": 500, "y": 300 },
      "type": "customNode",
      "data": {
        "id": "conversationChain_0",
        "label": "Conversation Chain",
        "version": 3,
        "name": "conversationChain",
        "type": "ConversationChain",
        "baseClasses": ["ConversationChain", "LLMChain", "BaseChain"],
        "category": "Chains",
        "inputAnchors": [
          {
            "label": "Chat Model",
            "name": "model",
            "type": "BaseChatModel",
            "id": "conversationChain_0-input-model-BaseChatModel"
          },
          {
            "label": "Memory",
            "name": "memory",
            "type": "BaseMemory",
            "id": "conversationChain_0-input-memory-BaseMemory"
          }
        ],
        "inputs": {
          "model": "{{chatOpenAI_0.data.instance}}",
          "memory": "{{bufferMemory_0.data.instance}}",
          "systemMessagePrompt": ""
        },
        "outputAnchors": [
          {
            "id": "conversationChain_0-output-conversationChain-ConversationChain|LLMChain|BaseChain",
            "name": "output",
            "label": "ConversationChain",
            "type": "ConversationChain | LLMChain | BaseChain"
          }
        ]
      }
    }
  ],
  "edges": [
    {
      "source": "chatOpenAI_0",
      "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLLM",
      "target": "conversationChain_0",
      "targetHandle": "conversationChain_0-input-model-BaseChatModel",
      "type": "buttonedge",
      "id": "chatOpenAI_0-chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLLM-conversationChain_0-conversationChain_0-input-model-BaseChatModel"
    },
    {
      "source": "bufferMemory_0",
      "sourceHandle": "bufferMemory_0-output-bufferMemory-BufferMemory|BaseChatMemory|BaseMemory",
      "target": "conversationChain_0",
      "targetHandle": "conversationChain_0-input-memory-BaseMemory",
      "type": "buttonedge",
      "id": "bufferMemory_0-bufferMemory_0-output-bufferMemory-BufferMemory|BaseChatMemory|BaseMemory-conversationChain_0-conversationChain_0-input-memory-BaseMemory"
    }
  ]
}
```
