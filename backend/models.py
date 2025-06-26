from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('student', 'admin'), nullable=False)

    results = relationship("Result", back_populates="user")

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    time_limit = Column(Integer, nullable=False)
    created_by = Column(String(255))

    questions = relationship("Question", back_populates="quiz")
    results = relationship("Result", back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question = Column(Text, nullable=False)
    A = Column(Text)
    B = Column(Text)
    C = Column(Text)
    D = Column(Text)
    correct = Column(Enum('A', 'B', 'C', 'D'), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  
    username = Column(String(255))  
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Integer)
    total_questions = Column(Integer)
    submitted_at = Column(DateTime)

    user = relationship("User", back_populates="results")
    quiz = relationship("Quiz", back_populates="results")

