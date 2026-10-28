# AI Customer Support Q&A API

A REST API that answers customer support questions using Llama 3.1 on Groq, built with FastAPI.

## Features
- `POST /api/ask` endpoint that returns an AI-generated answer
- Request validation with Pydantic (empty or whitespace-only questions are rejected)
- Error handling for rate limits (429), timeouts (504), provider errors (502) and unexpected failures (500)
- Configurable system prompt that keeps answers professional and escalates unknown questions to human support
- API keys loaded from environment variables

## Tech Stack
Python, FastAPI, Groq API (`llama-3.1-8b-instant`), Pydantic, python-dotenv, Uvicorn

## Setup

```bash
git clone https://github.com/alaamostafa08-byte/customer-support-qa-api.git
cd customer-support-qa-api
python -m venv venv
venv\Scripts\activate        # on macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`) and add your key from https://console.groq.com:

```
GROQ_API_KEY=your_groq_api_key_here
```

Run the server:

```bash
uvicorn main:app --reload
```

Interactive docs are available at http://127.0.0.1:8000/docs

## Usage

Request:

```bash
curl -X POST http://127.0.0.1:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How can I reset my password?"}'
```

Response (example):

```json
{
  "answer": "You can reset your password from the login page by selecting 'Forgot password'..."
}
```

## Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Empty or whitespace-only question |
| 429 | Groq rate limit exceeded |
| 502 | Error from the AI provider |
| 504 | AI provider request timed out |
| 500 | Unexpected server error |

## Roadmap
- Ground answers in company documents using retrieval (RAG) with a vector database
- Add conversation history and automated tests