# Simple RAG Application

A simple Retrieval-Augmented Generation (RAG) application that allows users to query a knowledge base and receive generated answers. The application uses a hybrid retrieval approach combining **BM25 keyword search** and **vector similarity search** to retrieve relevant documents, followed by a **local language model** to generate responses.

The project contains:
- A **Streamlit frontend** for user interaction
- A **FastAPI backend** for handling API requests and RAG pipeline execution
- A **local LLM** for answer generation without relying on external APIs

---

## Architecture Overview

```
                    User Query
                        |
                        v
              +----------------+
              | Streamlit UI   |
              +----------------+
                        |
                        v
              +----------------+
              | FastAPI Backend|
              +----------------+
                        |
                        v
             +-------------------+
             | Retrieval Pipeline|
             +-------------------+
                /            \
               /              \
              v                v
        BM25 Search       Vector Search
              \              /
               \            /
                v          v
              Hybrid Retrieval
                    |
                    v
             Context Generation
                    |
                    v
              Local LLM Model
                    |
                    v
              Generated Answer
```

---

## Features

- Query-based document retrieval
- Hybrid search using:
  - BM25 lexical search
  - Vector similarity search
- Local LLM inference for response generation
- FastAPI backend API
- Streamlit interactive frontend
- Fully local deployment (no external LLM API dependency)

---

## Project Structure

```
Simple-RAG-Application/
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── retriever.py         # BM25 + Vector retrieval logic
│   │   ├── llm.py               # Local model integration
│   │   ├── embeddings.py        # Embedding generation
│   │   └── utils.py             # Helper functions
│   │
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── app.py                   # Streamlit application
│   ├── requirements.txt
│
├── data/
│   └── documents/               # Input documents
│
├── models/
│   └── local_model/             # Local LLM files
│
├── README.md
└── .gitignore
```

---

# How It Works

## 1. User Query

The user enters a question through the Streamlit interface.

Example:

```
"What is the refund policy?"
```

---

## 2. Hybrid Retrieval

The query is processed using two retrieval methods:

### BM25 Search

BM25 retrieves documents based on keyword matching and lexical similarity.

Advantages:
- Good for exact keyword matches
- Works well with structured text

---

### Vector Search

Vector search converts queries and documents into embeddings and retrieves semantically similar content.

Advantages:
- Understands meaning beyond exact words
- Handles natural language queries

---

## 3. Context Creation

The retrieved documents from both BM25 and vector search are combined to create relevant context.

---

## 4. Local LLM Generation

The retrieved context is passed to a locally hosted language model which generates the final answer.

No external API calls are required.

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd Simple-RAG-Application
```

---

# Backend Setup

Navigate to backend:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend will start at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

# Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run app.py
```

Frontend will start at:

```
http://localhost:8501
```

---

# API Usage

## Query Endpoint

### Request

```
POST /query
```

Example:

```json
{
    "question": "Explain the document"
}
```

Response:

```json
{
    "answer": "Generated response from local model"
}
```

---

# Technologies Used

## Backend

- FastAPI
- Python
- BM25 Retrieval
- Vector Search
- Embedding Models
- Local LLM Inference

## Frontend

- Streamlit

## AI Components

- Hybrid Retrieval Pipeline
- Local Language Model
- Embedding-based Semantic Search

---

# Configuration

Update model and retrieval settings according to your environment.

Example:

```
MODEL_PATH=/models/local_model
VECTOR_DB_PATH=/data/vector_store
TOP_K=5
```

---

# Future Improvements

- Add document upload support
- Add conversation history
- Improve reranking strategy
- Add authentication
- Add support for multiple document formats
- Add evaluation metrics for retrieval quality

---

# License

This project is for educational and research purposes.
