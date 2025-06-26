from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

# ====================
# Login Info Schemas
# ====================
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Literal['student', 'admin']

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


# ====================
# Quiz Schemas
# ====================
class QuizBase(BaseModel):
    title: str
    description: str
    time_limit: int  # in minutes
    created_by: str

class QuizCreate(QuizBase):
    pass

class QuizResponse(QuizBase):
    id: int

    class Config:
        from_attributes = True

# ====================
# Question Schemas
# ====================
class QuestionBase(BaseModel):
    
    question: str
    A: str
    B: str
    C: str
    D: str
    correct: Literal['A', 'B', 'C', 'D']

class QuestionCreate(QuestionBase):
    quiz_id: int

class QuestionResponse(QuestionBase):
    id: int
    quiz_id: int

    class Config:
        from_attributes = True


# ====================
# Result Schemas
# ====================
class ResultBase(BaseModel):
    username: str
    quiz_id: int
    score: int
    total_questions: int
    submitted_at: Optional[datetime]

class ResultCreate(ResultBase):
    pass

class ResultResponse(ResultBase):
    id: int

    class Config:
        from_attributes = True

class LeaderboardEntry(BaseModel):
    username: str
    score: int
    total_questions: int
    submitted_at: datetime

    class Config:
        form_attributes = True