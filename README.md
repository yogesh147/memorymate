# 🧠 MemoryMate

> A private memory layer for your relationships.

MemoryMate helps friends remember important things from conversations,
notes, screenshots, PDFs, and plans.

## Features

- 🧠 AI-powered memory search
- 👥 Friend Mode
- 🔎 Semantic retrieval
- 📚 Source references
- 📤 Upload conversations
- 🗑️ Delete memories
- 🔐 Local/open-weight AI support
- 🗄️ PostgreSQL + pgvector
- 🚀 Render-ready backend

## Stack

- React
- Vite
- FastAPI
- PostgreSQL
- pgvector
- Gemma
- Ollama
- Sentence Transformers
- Docker
- Render

## Local Setup

### 1. Clone

```bash
git clone YOUR_REPOSITORY_URL
cd memorymate
```

### 2. Start backend
cd backend

python -m venv .venv

#### For macOS/Linux -   source .venv/bin/activate

#### For Windows -     .venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload

Backend: http://localhost:8000

API documentation: http://localhost:8000/docs

###  3. Start frontend

Open another terminal:

cd frontend

npm install

npm run dev

Frontend: http://localhost:5173

### 4. docker compose up db -d