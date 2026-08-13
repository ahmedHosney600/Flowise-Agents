# Flowise Workflow Templates

Pre-built patterns for common use cases. Use these as starting points and customize based on user requirements.

## Table of Contents
1. [Simple Chatbot](#1-simple-chatbot)
2. [RAG Q&A](#2-rag-qa)
3. [Conversational RAG](#3-conversational-rag)
4. [Tool Agent (OpenAI Function)](#4-tool-agent)
5. [Multi-Agent Supervisor (V2)](#5-multi-agent-supervisor-v2)
6. [API Integration Agent](#6-api-integration-agent)
7. [Web Scraping RAG](#7-web-scraping-rag)
8. [PDF Q&A](#8-pdf-qa)
9. [SQL Database Agent](#9-sql-database-agent)
10. [Human-in-the-Loop Agent (V2)](#10-human-in-the-loop-v2)

---

## 1. Simple Chatbot

**Use when**: User wants a basic conversational AI with memory.

**Nodes**:
- `chatOpenAI` → `conversationChain` ← `bufferMemory`

**Mermaid**:
```
graph LR
    A[ChatOpenAI] --> C[Conversation Chain]
    B[Buffer Memory] --> C
```

**Key config**:
- Model: gpt-4o (or user preference)
- Temperature: 0.7
- System message: customize per use case

---

## 2. RAG Q&A

**Use when**: User wants to ask questions about their documents (no conversation memory).

**Nodes**:
- `pdfFile` → `recursiveCharacterTextSplitter` → `openAIEmbedding` + `inMemoryVectorStore` → `retrievalQAChain` ← `chatOpenAI`

**Mermaid**:
```
graph TD
    A[PDF File] --> B[Text Splitter]
    B --> D[In-Memory Vector Store]
    C[OpenAI Embeddings] --> D
    D --> E[Retrieval QA Chain]
    F[ChatOpenAI] --> E
```

**Key config**:
- Chunk size: 1000, Overlap: 200
- Embedding model: text-embedding-3-small
- Top K retrieval: 4

---

## 3. Conversational RAG

**Use when**: User wants RAG with follow-up question support.

**Nodes**:
- Document Loader → Text Splitter → Embeddings + Vector Store → `conversationalRetrievalQAChain` ← `chatOpenAI` + `bufferMemory`

**Mermaid**:
```
graph TD
    A[Document Loader] --> B[Text Splitter]
    B --> D[Vector Store]
    C[Embeddings] --> D
    D --> E[Conversational Retrieval QA Chain]
    F[ChatOpenAI] --> E
    G[Buffer Memory] --> E
```

**Key config**:
- Same as RAG Q&A plus:
- Memory: bufferMemory or bufferWindowMemory (k=5)
- Return source documents: true (optional)

---

## 4. Tool Agent

**Use when**: User wants an agent that can use external tools (search, calculator, APIs).

**Nodes**:
- `chatOpenAI` → `openAIFunctionAgent` ← `bufferMemory` + tools[]

**Mermaid**:
```
graph LR
    A[ChatOpenAI] --> D[OpenAI Function Agent]
    B[Buffer Memory] --> D
    C1[SerpAPI] --> D
    C2[Calculator] --> D
    C3[Custom Tool] --> D
```

**Key config**:
- Model: gpt-4o (function calling required)
- System message: describe agent's purpose
- Tools: add based on use case

---

## 5. Multi-Agent Supervisor (V2)

**Use when**: User wants multiple specialized agents coordinated by a supervisor.

**Nodes (AgentFlow V2)**:
- `agentFlowV2Start` → `agentFlowV2Agent` (Supervisor) → `agentFlowV2Condition` → Worker Agents → `agentFlowV2End`

**Mermaid**:
```
graph TD
    A[Start] --> B[Supervisor Agent]
    B --> C{Condition: Route}
    C -->|Research| D[Research Agent]
    C -->|Write| E[Writer Agent]
    C -->|Done| F[End]
    D --> B
    E --> B
```

**Key config**:
- Supervisor system prompt: define delegation rules
- Worker agents: each with specialized tools and system prompts
- Flow State: track task status and outputs
- Condition: route based on supervisor's decision

---

## 6. API Integration Agent

**Use when**: User wants to connect an agent to external REST APIs.

**Nodes**:
- `chatOpenAI` → `openAIFunctionAgent` ← `customTool` (with HTTP calls)

Or with AgentFlow V2:
- `agentFlowV2Start` → `agentFlowV2Agent` → `agentFlowV2HTTP` → `agentFlowV2End`

**Custom Tool example** (JavaScript function):
```javascript
const fetch = require('node-fetch');
const response = await fetch('https://api.example.com/data', {
  method: 'GET',
  headers: { 'Authorization': 'Bearer ' + $vars.apiKey }
});
const data = await response.json();
return JSON.stringify(data);
```

---

## 7. Web Scraping RAG

**Use when**: User wants to build a knowledge base from web pages.

**Nodes**:
- `cheerioWebScraper` → `recursiveCharacterTextSplitter` → `openAIEmbedding` + Vector Store → `retrievalQAChain` ← `chatOpenAI`

**Mermaid**:
```
graph TD
    A[Cheerio Web Scraper] --> B[Text Splitter]
    B --> D[Vector Store]
    C[OpenAI Embeddings] --> D
    D --> E[Retrieval QA Chain]
    F[ChatOpenAI] --> E
```

**Key config**:
- URL: target website
- Selector: CSS selector for content area (optional)
- Chunk size: 1500, Overlap: 200

---

## 8. PDF Q&A

**Use when**: User wants to chat with PDF documents specifically.

Same as RAG Q&A template but uses `pdfFile` document loader. For multiple PDFs, chain multiple `pdfFile` nodes into the same text splitter, or use a folder-based loader.

---

## 9. SQL Database Agent

**Use when**: User wants to query databases using natural language.

**Nodes**:
- `chatOpenAI` → `sqlDatabaseChain` ← database connection

**Mermaid**:
```
graph LR
    A[ChatOpenAI] --> B[SQL Database Chain]
    C[Database] --> B
```

**Key config**:
- Database type: MySQL, PostgreSQL, SQLite, etc.
- Connection URL: database connection string
- Include/exclude tables as needed

---

## 10. Human-in-the-Loop (V2)

**Use when**: User wants agent workflows that pause for human approval before sensitive actions.

**Nodes (AgentFlow V2)**:
- `agentFlowV2Start` → `agentFlowV2Agent` → `agentFlowV2HumanInput` → `agentFlowV2Tool` → `agentFlowV2End`

**Mermaid**:
```
graph TD
    A[Start] --> B[Agent]
    B --> C[Human Input: Approve?]
    C -->|Yes| D[Execute Tool]
    C -->|No| E[End - Cancelled]
    D --> F[End - Complete]
```

**Key config**:
- Human Input prompt: describe what needs approval
- Agent tools: mark sensitive tools with "Require Human Input" flag
- Checkpoints: enabled for long-running workflows

---

## Customization Guide

When adapting templates:

1. **Swap LLM provider**: Replace `chatOpenAI` with `chatAnthropic`, `chatGoogleGenerativeAI`, `chatOllama`, etc. Update credential accordingly.

2. **Swap vector store**: Replace `inMemoryVectorStore` with `pinecone`, `chroma`, `qdrant`, `pgvector`, etc. Ensure embedding dimensions match.

3. **Add memory**: Any chain or agent can accept a memory node. Use `bufferMemory` for simple cases, `bufferWindowMemory` (k=5) for long conversations, or persistent memory (Redis, Postgres) for production.

4. **Add tools**: Agents can accept multiple tools. Connect each tool node to the agent's tools input.

5. **System prompts**: Customize the system message to define behavior, persona, and constraints.

6. **Production considerations**:
   - Use persistent memory (Redis/Postgres) instead of buffer memory
   - Use managed vector stores (Pinecone/Qdrant) instead of in-memory
   - Set appropriate rate limits and max token values
   - Enable analytics for monitoring
