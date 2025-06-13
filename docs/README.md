# RAG Chatbot Workflow (n8n)

This project is an automated **RAG-based chatbot** workflow built in [n8n](https://n8n.io/). It uses **retrieval-augmented generation** to fetch relevant documents and generate conversational answers with source attribution.

---

## 📌 Features

- Accepts user queries via HTTP Webhook.
- Cleans and validates input text.
- Fetches relevant context from a local RAG backend (`/search` endpoint).
- Uses the **Mistral API** to generate responses.
- Formats and returns answers along with referenced document IDs.
- Logs responses with timestamps and statuses (success or error).
- Routes logic via Switch node for robust error handling.
- Returns response directly via webhook.

---

## 📂 Workflow Overview

1. **Webhook Node**: Receives incoming query (POST with JSON `{ query: "..." }`).
2. **Code3**: Sanitizes and validates the input query.
3. **HTTP Request1**: Calls a RAG backend to retrieve relevant documents and IDs.
4. **Code4**: Constructs a full prompt using the documents and query.
5. **Generation Node1**: Sends the prompt to Mistral’s chat completion API.
6. **Code5**: Parses the Mistral response and formats the final output.
7. **Switch1**: Determines whether the response is a success or error.
8. - If **success**:
   - `Code6`: Generates a log string and converts it to binary.
   - `Read/Write File`: Writes the log to `logs/chatbot.log`.
   - `Respond to Webhook1`: Sends the final chatbot response.
9. - If **error**:
   - `Error Response`: Prepares error message.
   - `Error Log` → `Error Webhook Response`: Logs and returns error.

---

## 🛠 Requirements

- n8n self-hosted or desktop version
- Python-based RAG backend running locally on `http://127.0.0.1:5000/search`
- Mistral API key (bearer token auth)
- Proper `logs` directory write access

---

## 🧪 Example Request

```bash
curl -X POST http://localhost:5678/webhook   -H "Content-Type: application/json"   -d '{"query": "What is retrieval-augmented generation?"}'
```

---

## 📁 Log Format

Each query is logged to `logs/chatbot.log` as:

```
2025-06-13T06:40:12.344Z: Query: what is rag, Response: ... , Status: SUCCESS
```

---

## ✅ Status

- ✅ Completed
- 🚀 Ready for extension with vector search engine, database, or user feedback tracking.