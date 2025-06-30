from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from typing import List
from database import SessionLocal, engine, verify_connection
import models
import schemas
from auth import router as auth_router
from routes import ai_router
from google_auth import router as google_auth_router
from starlette.middleware.sessions import SessionMiddleware
from routes import quizzes
from routes.leaderboard import router as leaderboard_router
from routes import submissions
from routes import questions
from routes import submissions
from routes import publicQuizzes
from google_auth import router as google_auth_router

DATABASE_URL = os.getenv("DATABASE_URL")
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://quizzeria-world.netlify.app"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.add_middleware(SessionMiddleware, secret_key="493290581729-21f4h57r8kjunc8bvrmtk4qr3htv0plb.apps.googleusercontent.com")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

if os.getenv("RAILWAY_STATIC_FRONTEND") != "false" and os.path.isdir(FRONTEND_DIR):
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

@app.on_event("startup")
def startup_event():
    print("🚀 Starting FastAPI app...")
    verify_connection()
    models.Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(google_auth_router)
app.include_router(submissions.router)
app.include_router(questions.router)
app.include_router(submissions.router)
app.include_router(leaderboard_router)
app.include_router(quizzes.router)
app.include_router(publicQuizzes.router)
app.include_router(ai_router.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/role-by-email/{email}")
def get_role_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"role": user.role}

@app.get("/username-by-email/{email}")
def get_username_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username}


@app.get("/user-id-by-username/{username}")
def get_user_id_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id}

@app.post("/quizzes/", response_model=schemas.QuizResponse)
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(get_db)):
    db_quiz = models.Quiz(**quiz.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@app.get("/quizzes/user/{username}", response_model=list[schemas.QuizResponse])
def get_quizzes_by_user(username: str, db: Session = Depends(get_db)):
    quizzes = db.query(models.Quiz).filter(models.Quiz.created_by == username).all()
    return quizzes

@app.post("/questions/", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@app.get("/questions/quiz/{quiz_id}", response_model=List[schemas.QuestionResponse])
def get_questions_for_quiz(quiz_id: int, db: Session = Depends(get_db)):
    return db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()


@app.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Question).get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"message": "Question deleted"}


@app.put("/questions/{question_id}", response_model=schemas.QuestionResponse)
def update_question(question_id: int, updated: schemas.QuestionCreate, db: Session = Depends(get_db)):
    question = db.query(models.Question).get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    for key, value in updated.dict().items():
        setattr(question, key, value)
    db.commit()
    db.refresh(question)
    return question



@app.post("/results/", response_model=schemas.ResultResponse)
def create_result(result: schemas.ResultCreate, db: Session = Depends(get_db)):
    db_result = models.Result(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result



@app.get("/quizzes/role/{username}")
def get_user_role(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"role": user.role}


@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
