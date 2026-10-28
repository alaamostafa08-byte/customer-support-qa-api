from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from groq import Groq, APIError, RateLimitError, APITimeoutError
import os
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Initialize FastAPI and Groq Client
app = FastAPI(title="AI Customer Support Q&A API")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 3. Input Validation Model
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The user's question to the support assistant")

# 4. System Prompt
SYSTEM_PROMPT = """You are a helpful and professional customer support assistant. 
Answer the user's questions accurately based strictly on our company policies. 
If you don't know the answer, politely ask the user to contact human support."""

@app.post("/api/ask")
async def ask_question(request: QueryRequest):
    # Basic input validation for empty or whitespace-only strings
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty or whitespace.")

    try:
        # 5. Integration with Groq Chat Completions API
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", # Fast and capable Groq model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.question}
            ],
            temperature=0.3,
            max_tokens=300,
            timeout=10.0
        )
        
        return {"answer": response.choices[0].message.content}

    # 6. Error Handling tailored for Groq
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
    
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="Request to the AI provider timed out. Please try again.")
    
    except APIError as e:
        # Handles other Groq API errors
        raise HTTPException(status_code=502, detail=f"AI Provider error: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected internal server error occurred.")
    