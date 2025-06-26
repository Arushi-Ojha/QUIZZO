
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Quiz
from schemas import QuizResponse

router = APIRouter(
    prefix="/public",
    tags=["Public Quizzes"]
)

@router.get("/latest-quizzes", response_model=list[QuizResponse])
def get_latest_quizzes(db: Session = Depends(get_db)):
    latest_quizzes = db.query(Quiz).order_by(Quiz.id.desc()).limit(4).all()
    return latest_quizzes
