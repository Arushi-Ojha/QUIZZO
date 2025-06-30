# routers/ai_route.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Quiz, Question, User
from schemas import QuizCreate
from ai import generate_quiz_questions
from uuid import uuid4
from datetime import datetime
from schemas import QuizCreate, QuizResponse, QuizInput
from pydantic import BaseModel

router = APIRouter()

@router.post("/ai/generate_quiz/")
async def generate_quiz(data: QuizInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.created_by).first()
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can generate quizzes")

    quiz = Quiz(
        title=data.title,
        description=data.description,
        time_limit=data.time_limit,
        created_by=data.created_by
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    # AI question generation
    questions = await generate_quiz_questions(data.title, data.description, data.level)

    for q in questions:
        db.add(Question(
            quiz_id=quiz.id,
            question=q['question'],
            A=q['A'],
            B=q['B'],
            C=q['C'],
            D=q['D'],
            correct=q['correct']
        ))

    db.commit()
    return {"message": "Quiz generated successfully", "quiz_id": quiz.id}
