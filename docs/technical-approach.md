# Technical Approach: RAG Chatbot using n8n

This document outlines the architecture and technical strategy used to implement a Retrieval-Augmented Generation (RAG) based chatbot workflow inside n8n.

---

## 🔧 Key Components

### 1. **Webhook Input**
- Exposes an HTTP POST endpoint (`/webhook`).
- Accepts raw JSON with a `query` field.
- Initiates the chatbot response flow.

---

### 2. **Input Validation (Code3)**
- Extracts `query` from `body.query`.
- Converts to lowercase and trims whitespace.
- Throws error if query is missing or empty.

---

### 3. **Context Retrieval (HTTP Request1)**
- Sends POST request to a locally hosted RAG backend (`/search`).
- Receives:
  ```json
  {
    "documents": [ ... ],
    "ids": [ ... ]
  }
  ```

---

### 4. **Prompt Creation (Code4)**
- Constructs a structured prompt:
  ```
  You are a helpful FAQ chatbot...
  Context: [doc1, doc2, ...]
  Query: ...
  Answer:
  ```

---

### 5. **Response Generation (Generation Node1)**
- Sends the prompt to Mistral’s chat completions API.
- Includes model config:
  - Model: `mistral-small-latest`
  - `max_tokens`: 500
  - `temperature`: 0.7

---

### 6. **Output Formatting (Code5)**
- Extracts generated answer from `choices[0].message.content`.
- Attaches `Source Documents: ID1, ID2, ...`
- Sets `success: true` or `error: true` flags.

---

### 7. **Control Flow with Switch**
- Switch1 checks `error === true` or `error === false`.
- Routes accordingly:
  - Error → logs + error response
  - Success → log + send final webhook response

---

### 8. **Logging and File Writing (Code6 + File Write)**
- Uses a `Code` node to convert logs to base64-encoded text.
- Writes logs as binary using `Read/Write File` node to `logs/chatbot.log`.

---

## 🧠 Design Considerations

- **Fail-safes**: Every node is wrapped with proper checks for missing values or malformed data.
- **Debuggability**: Switch and logging give full traceability.
- **Extensibility**: Can plug in Pinecone, Qdrant, Weaviate, etc., for scalable document storage.

---

## 🚀 Future Enhancements

- Support chat history with vector context.
- Add UI for manual QA uploads.
- Integrate vector store like Qdrant.
- Add user feedback logging (e.g., was this helpful?)

---

## 🧩 Stack

- **n8n**: Automation + logic orchestration
- **Python RAG Backend**: Document retrieval
- **Mistral API**: Language generation
- **File-based Logs**: Simple, extensible logging