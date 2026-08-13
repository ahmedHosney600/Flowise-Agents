# Flowise Node Catalog

Canonical list of Flowise component nodes organized by category. Use the `name` field exactly as shown — it must match Flowise's internal registry.

## Table of Contents
1. [Chat Models](#chat-models)
2. [Chains](#chains)
3. [Agents](#agents)
4. [Memory](#memory)
5. [Tools](#tools)
6. [Vector Stores](#vector-stores)
7. [Embeddings](#embeddings)
8. [Document Loaders](#document-loaders)
9. [Text Splitters](#text-splitters)
10. [Output Parsers](#output-parsers)
11. [Prompts](#prompts)
12. [Retrievers](#retrievers)
13. [AgentFlow V1 Nodes](#agentflow-v1-nodes)
14. [AgentFlow V2 Nodes](#agentflow-v2-nodes)

---

## Chat Models

| name | label | baseClasses | Key Inputs |
|---|---|---|---|
| `chatOpenAI` | ChatOpenAI | ChatOpenAI, BaseChatModel, BaseLLM | modelName, temperature, credential |
| `chatAnthropic` | ChatAnthropic | ChatAnthropic, BaseChatModel, BaseLLM | modelName, temperature, credential |
| `chatGoogleGenerativeAI` | ChatGoogleGenerativeAI | ChatGoogleGenerativeAI, BaseChatModel, BaseLLM | modelName, temperature, credential |
| `azureChatOpenAI` | Azure ChatOpenAI | AzureChatOpenAI, BaseChatModel, BaseLLM | modelName, temperature, credential |
| `chatOllama` | ChatOllama | ChatOllama, BaseChatModel, BaseLLM | baseUrl, modelName, temperature |
| `chatMistralAI` | ChatMistralAI | ChatMistralAI, BaseChatModel, BaseLLM | modelName, temperature, credential |
| `chatGroq` | ChatGroq | ChatGroq, BaseChatModel, BaseLLM | modelName, temperature, credential |
| `chatCohere` | ChatCohere | ChatCohere, BaseChatModel, BaseLLM | modelName, temperature, credential |
| `chatHuggingFace` | ChatHuggingFace | ChatHuggingFace, BaseChatModel, BaseLLM | modelName, temperature, credential |
| `chatLocalAI` | ChatLocalAI | ChatLocalAI, BaseChatModel, BaseLLM | basePath, modelName, temperature |

## Chains

| name | label | baseClasses | Key Inputs (Anchors) |
|---|---|---|---|
| `conversationChain` | Conversation Chain | ConversationChain, LLMChain, BaseChain | model (BaseChatModel), memory (BaseMemory) |
| `llmChain` | LLM Chain | LLMChain, BaseChain | model (BaseChatModel), prompt (BasePromptTemplate) |
| `retrievalQAChain` | Retrieval QA Chain | RetrievalQAChain, BaseChain | model (BaseChatModel), vectorStoreRetriever (BaseRetriever) |
| `conversationalRetrievalQAChain` | Conversational Retrieval QA Chain | ConversationalRetrievalQAChain, BaseChain | model (BaseChatModel), vectorStoreRetriever (BaseRetriever), memory (BaseMemory) |
| `sqlDatabaseChain` | Sql Database Chain | SqlDatabaseChain, BaseChain | model (BaseChatModel), database |
| `apiChain` | API Chain | APIChain, BaseChain | model (BaseChatModel), apiUrl, apiDocs |
| `multiPromptChain` | Multi Prompt Chain | MultiPromptChain, BaseChain | model (BaseChatModel), promptNames, promptDescriptions, promptTemplates |

## Agents

| name | label | baseClasses | Key Inputs (Anchors) |
|---|---|---|---|
| `openAIFunctionAgent` | OpenAI Function Agent | AgentExecutor, BaseChain | model (BaseChatModel), tools (Tool[]), memory (BaseMemory) |
| `conversationalAgent` | Conversational Agent | AgentExecutor, BaseChain | model (BaseChatModel), tools (Tool[]), memory (BaseMemory) |
| `openAIAssistant` | OpenAI Assistant | OpenAIAssistant | credential, assistantId |
| `reactAgentChat` | ReAct Agent Chat | AgentExecutor, BaseChain | model (BaseChatModel), tools (Tool[]), memory (BaseMemory) |
| `toolAgent` | Tool Agent | AgentExecutor, BaseChain | model (BaseChatModel), tools (Tool[]) |
| `csvAgent` | CSV Agent | AgentExecutor, BaseChain | model (BaseChatModel), csvFile |
| `autoGPT` | AutoGPT | AutoGPT | model (BaseChatModel), tools (Tool[]), vectorStoreRetriever (BaseRetriever) |

## Memory

| name | label | baseClasses | Key Inputs |
|---|---|---|---|
| `bufferMemory` | Buffer Memory | BufferMemory, BaseChatMemory, BaseMemory | sessionId |
| `bufferWindowMemory` | Buffer Window Memory | BufferWindowMemory, BaseChatMemory, BaseMemory | k (window size), sessionId |
| `conversationSummaryMemory` | Conversation Summary Memory | ConversationSummaryMemory, BaseChatMemory, BaseMemory | model (BaseChatModel), sessionId |
| `zepMemory` | Zep Memory | ZepMemory, BaseChatMemory, BaseMemory | baseURL, sessionId, credential |
| `redisBackedChatMemory` | Redis-Backed Chat Memory | RedisBackedChatMemory, BaseChatMemory, BaseMemory | baseURL, sessionId, credential |
| `postgresBackedChatMemory` | Postgres Chat Memory | PostgresChatMemory, BaseChatMemory, BaseMemory | credential, sessionId |
| `dynamoDb` | DynamoDB Chat Memory | DynamoDBChatMemory, BaseChatMemory, BaseMemory | tableName, partitionKey, credential |

## Tools

| name | label | baseClasses | Key Inputs |
|---|---|---|---|
| `customTool` | Custom Tool | CustomTool, Tool | toolName, toolDescription, javascriptFunction |
| `serpAPI` | Serp API | SerpAPI, Tool | credential |
| `braveSearchAPI` | BraveSearch API | BraveSearchAPI, Tool | credential |
| `calculator` | Calculator | Calculator, Tool | — |
| `requestsGet` | Requests Get | RequestsGet, Tool | url, headers |
| `requestsPost` | Requests Post | RequestsPost, Tool | url, headers, body |
| `readFile` | Read File | ReadFileTool, Tool | basePath |
| `writeFile` | Write File | WriteFileTool, Tool | basePath |
| `webBrowser` | Web Browser | WebBrowser, Tool | model (BaseChatModel), embeddings (Embeddings) |
| `chainTool` | Chain Tool | ChainTool, Tool | chain (BaseChain), toolName, toolDescription |
| `retrieverTool` | Retriever Tool | RetrieverTool, Tool | retriever (BaseRetriever), toolName, toolDescription |
| `openAPIToolkit` | OpenAPI Toolkit | OpenAPIToolkit, Tool | openAPISpec, model (BaseChatModel) |
| `mcpTool` | MCP Tool | MCPTool, Tool | mcpServerConfig |

## Vector Stores

| name | label | baseClasses | Key Inputs (Anchors) |
|---|---|---|---|
| `inMemoryVectorStore` | In-Memory Vector Store | InMemoryVectorStore, VectorStore | embeddings (Embeddings), documents (Document[]) |
| `pinecone` | Pinecone | Pinecone, VectorStore | embeddings (Embeddings), credential, indexName |
| `chroma` | Chroma | Chroma, VectorStore | embeddings (Embeddings), collectionName |
| `faiss` | Faiss | Faiss, VectorStore | embeddings (Embeddings), basePath |
| `qdrant` | Qdrant | Qdrant, VectorStore | embeddings (Embeddings), credential, qdrantServerUrl, collectionName |
| `weaviate` | Weaviate | Weaviate, VectorStore | embeddings (Embeddings), credential, weaviateScheme, weaviateHost, className |
| `supabase` | Supabase | Supabase, VectorStore | embeddings (Embeddings), credential, tableName, queryName |
| `pgvector` | PGVector | PGVector, VectorStore | embeddings (Embeddings), credential, tableName |
| `milvus` | Milvus | Milvus, VectorStore | embeddings (Embeddings), milvusServerUrl, collectionName |

## Embeddings

| name | label | baseClasses | Key Inputs |
|---|---|---|---|
| `openAIEmbedding` | OpenAI Embeddings | OpenAIEmbeddings, Embeddings | modelName, credential |
| `azureOpenAIEmbedding` | Azure OpenAI Embeddings | AzureOpenAIEmbeddings, Embeddings | credential, deploymentName |
| `cohereEmbedding` | Cohere Embeddings | CohereEmbeddings, Embeddings | modelName, credential |
| `googleGenerativeAIEmbedding` | Google Generative AI Embeddings | GoogleGenerativeAIEmbeddings, Embeddings | modelName, credential |
| `huggingFaceInferenceEmbedding` | HuggingFace Inference Embeddings | HuggingFaceInferenceEmbeddings, Embeddings | modelName, credential |
| `ollamaEmbedding` | Ollama Embeddings | OllamaEmbeddings, Embeddings | baseUrl, modelName |

## Document Loaders

| name | label | baseClasses | Key Inputs |
|---|---|---|---|
| `pdfFile` | Pdf File | PDFLoader, Document | pdfFile |
| `textFile` | Text File | TextFileLoader, Document | txtFile |
| `csvFile` | Csv File | CSVLoader, Document | csvFile |
| `jsonFile` | Json File | JSONLoader, Document | jsonFile |
| `docxFile` | Docx File | DocxLoader, Document | docxFile |
| `webCrawler` | Web Crawler | WebCrawler, Document | url, limit |
| `cheerioWebScraper` | Cheerio Web Scraper | CheerioWebScraper, Document | url, selector |
| `playwrightWebScraper` | Playwright Web Scraper | PlaywrightWebScraper, Document | url |
| `puppeteerWebScraper` | Puppeteer Web Scraper | PuppeteerWebScraper, Document | url |
| `notionDb` | Notion Database | NotionDBLoader, Document | credential, databaseId |
| `confluence` | Confluence | ConfluenceLoader, Document | credential, baseUrl, spaceKey |
| `githubLoader` | Github | GithubLoader, Document | credential, repoLink, branch |
| `s3FileLoader` | S3 File Loader | S3FileLoader, Document | credential, bucketName, key |
| `airtable` | Airtable | AirtableLoader, Document | credential, baseId, tableId |

## Text Splitters

| name | label | baseClasses | Key Inputs |
|---|---|---|---|
| `recursiveCharacterTextSplitter` | Recursive Character Text Splitter | RecursiveCharacterTextSplitter, TextSplitter | chunkSize, chunkOverlap |
| `characterTextSplitter` | Character Text Splitter | CharacterTextSplitter, TextSplitter | chunkSize, chunkOverlap, separator |
| `tokenTextSplitter` | Token Text Splitter | TokenTextSplitter, TextSplitter | chunkSize, chunkOverlap, encodingName |
| `markdownTextSplitter` | Markdown Text Splitter | MarkdownTextSplitter, TextSplitter | chunkSize, chunkOverlap |
| `htmlToMarkdownTextSplitter` | HtmlToMarkdown Text Splitter | HtmlToMarkdownTextSplitter, TextSplitter | chunkSize, chunkOverlap |
| `codeTextSplitter` | Code Text Splitter | CodeTextSplitter, TextSplitter | chunkSize, chunkOverlap, language |

## Output Parsers

| name | label | baseClasses | Key Inputs |
|---|---|---|---|
| `structuredOutputParser` | Structured Output Parser | StructuredOutputParser, BaseOutputParser | jsonSchema |
| `customListOutputParser` | Custom List Output Parser | CustomListOutputParser, BaseOutputParser | separator, length |
| `csvOutputParser` | CSV Output Parser | CSVOutputParser, BaseOutputParser | — |
| `advancedStructuredOutputParser` | Advanced Structured Output Parser | AdvancedStructuredOutputParser, BaseOutputParser | zodSchema |

## Prompts

| name | label | baseClasses | Key Inputs |
|---|---|---|---|
| `promptTemplate` | Prompt Template | PromptTemplate, BaseStringPromptTemplate, BasePromptTemplate | template, inputVariables |
| `chatPromptTemplate` | Chat Prompt Template | ChatPromptTemplate, BaseChatPromptTemplate, BasePromptTemplate | systemMessage, humanMessage |
| `fewShotPromptTemplate` | Few Shot Prompt Template | FewShotPromptTemplate, BaseStringPromptTemplate, BasePromptTemplate | examples, examplePrompt, prefix, suffix |

## Retrievers

| name | label | baseClasses | Key Inputs (Anchors) |
|---|---|---|---|
| `vectorStoreRetriever` | Vector Store Retriever | VectorStoreRetriever, BaseRetriever | vectorStore (VectorStore), topK |
| `contextualCompressionRetriever` | Contextual Compression Retriever | ContextualCompressionRetriever, BaseRetriever | baseRetriever (BaseRetriever), baseCompressor |
| `multiQueryRetriever` | Multi Query Retriever | MultiQueryRetriever, BaseRetriever | vectorStore (VectorStore), model (BaseChatModel) |
| `hyde` | Hypothetical Document Embeddings | HyDE, BaseRetriever | vectorStore (VectorStore), model (BaseChatModel) |

## AgentFlow V1 Nodes (Sequential Agents — Legacy)

| name | label | Purpose |
|---|---|---|
| `seqStart` | Start | Entry point; defines initial state and inputs |
| `seqAgent` | Agent Node | LLM-powered agent that can use tools |
| `seqLLMNode` | LLM Node | LLM processing without tool access |
| `seqToolNode` | Tool Node | Executes tools from agent's tool_calls |
| `seqCondition` | Condition Node | Routes flow based on conditions (if/else) |
| `seqConditionAgent` | Condition Agent Node | Agent-based routing |
| `seqState` | State Node | Defines custom shared state |
| `seqLoop` | Loop Node | Repeats a sequence |
| `seqEnd` | End Node | Terminal node |

## AgentFlow V2 Nodes (Current)

| name | label | Purpose | Key Inputs |
|---|---|---|---|
| `agentFlowV2Start` | Start | Entry point; triggers workflow | Input variables |
| `agentFlowV2LLM` | LLM | LLM text generation | Messages, model config, output schema |
| `agentFlowV2Agent` | Agent | Autonomous agent with tools | Tools, Document Stores, model config |
| `agentFlowV2Tool` | Tool | Deterministic tool execution | Tool selection, input arguments |
| `agentFlowV2Condition` | Condition | Conditional branching | Conditions list (if/else if/else) |
| `agentFlowV2HumanInput` | Human Input | Pause for user input | Prompt message |
| `agentFlowV2Iteration` | Iteration (Loop) | Loop over arrays | Array source, loop body |
| `agentFlowV2HTTP` | HTTP Request | Make HTTP calls | URL, method, headers, body |
| `agentFlowV2CustomJS` | Custom JavaScript | Execute JS code | Code, input variables |
| `agentFlowV2End` | End | Terminal node | Output value |
| `agentFlowV2ExecuteFlow` | Execute Flow | Run sub-flow | Flow ID, input, override config |
| `agentFlowV2SetVariable` | Set Variable | Update flow state | Variable name, value |

### V2 Data Passing
Nodes in V2 reference outputs from previous nodes using the syntax: `{{ nodeId.data.instance }}` or via the Flow State (`$flow.state`).
