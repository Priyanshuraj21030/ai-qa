from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List, Optional
from pydantic import BaseModel
import sqlite3

from .database import init_db, get_db
from .models import Question
from .ai_service import get_ai_response

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int
    total_pages: int

@app.on_event("startup")
async def startup():
    init_db()

@app.post("/ask")
@limiter.limit("5/minute")  # Limit to 5 requests per minute per IP
async def ask_question(
    request: Request,
    question_req: QuestionRequest,
    remote_addr: str = Depends(get_remote_address)
):
    if not question_req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    if len(question_req.question) > 1000:
        raise HTTPException(status_code=400, detail="Question too long")
    
    try:
        # Get AI response
        answer = await get_ai_response(question_req.question)
        
        # Store in database
        db = get_db()
        question = Question(question=question_req.question, answer=answer)
        question.save(db)
        db.close()  # Make sure to close the database connection
        
        return {"answer": answer}
    except Exception as e:
        print(f"Error in ask_question: {str(e)}")  # Add debug logging
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    remote_addr: str = Depends(get_remote_address)
):
    try:
        db = get_db()
        total = Question.count_all(db)
        questions = Question.get_paginated(db, page, page_size)
        total_pages = (total + page_size - 1) // page_size
        
        return PaginatedResponse(
            items=[q.to_dict() for q in questions],  # Convert Question objects to dicts
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except Exception as e:
        print(f"History error: {str(e)}")  # Add debug logging
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 