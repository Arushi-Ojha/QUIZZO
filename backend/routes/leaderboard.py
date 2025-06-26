from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter()

@router.get("/leaderboard/{quiz_id}", response_model=list[schemas.LeaderboardEntry])
def get_leaderboard(quiz_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(models.Result)
        .filter(models.Result.quiz_id == quiz_id)
        .order_by(models.Result.score.desc())
        .all()
    )

    return results
