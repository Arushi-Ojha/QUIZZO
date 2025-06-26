from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/results", tags=["Results"])



@router.post("/", response_model=schemas.ResultResponse)
def submit_result(result: schemas.ResultCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == result.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing = db.query(models.Result).filter(
        models.Result.user_id == user.id,
        models.Result.quiz_id == result.quiz_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Result already submitted for this quiz")

    db_result = models.Result(
    user_id=user.id,
    username=result.username,
    quiz_id=result.quiz_id,
    score=result.score,
    total_questions=result.total_questions,
    submitted_at=result.submitted_at
)


    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result



@router.get("/{user_id}/{quiz_id}", response_model=schemas.ResultResponse)
def get_result(user_id: int, quiz_id: int, db: Session = Depends(get_db)):
    

    result = db.query(models.Result).filter(
        models.Result.user_id == user_id,
        models.Result.quiz_id == quiz_id
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return result
