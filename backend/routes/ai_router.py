from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Quiz, Question, User
from schemas import QuizInput
from ai import generate_quiz_questions

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

    questions = await generate_quiz_questions(data.title, data.description, data.level)

    if not questions:
        raise HTTPException(status_code=500, detail="Failed to generate questions. Please try again later.")

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
    return {"message": "Quiz and questions generated successfully", "quiz_id": quiz.id}
