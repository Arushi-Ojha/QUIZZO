from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("/quiz/{quiz_id}", response_model=List[schemas.QuestionResponse])
def get_questions_for_quiz(quiz_id: int, db: Session = Depends(get_db)):
    questions = db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this quiz.")
    return questions
