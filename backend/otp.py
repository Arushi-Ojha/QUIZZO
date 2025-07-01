from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import random
import smtplib
from email.message import EmailMessage
from database import get_db
from schemas import UserCreate
from auth import create_user  

router = APIRouter(prefix="/auth", tags=["Authentication"])


SENDER_EMAIL = "arushiojha100@gmail.com"
APP_PASSWORD = "your-app-password"

otp_store = {}

class EmailRequest(BaseModel):
    email: EmailStr

class SignupWithOtp(UserCreate):
    otp: str

@router.post("/send-otp")
def send_otp(request: EmailRequest):
    otp = str(random.randint(100000, 999999))
    otp_store[request.email] = otp

    msg = EmailMessage()
    msg.set_content(f"Your QUIZZERIA signup OTP is: {otp}")
    msg["Subject"] = "Your OTP for QUIZZERIA Signup"
    msg["From"] = SENDER_EMAIL
    msg["To"] = request.email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {e}")

    return {"detail": "OTP sent to email"}

@router.post("/verify-otp-and-signup")
def verify_otp_and_signup(data: SignupWithOtp, db: Session = Depends(get_db)):
    stored_otp = otp_store.get(data.email)
    if not stored_otp or stored_otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    del otp_store[data.email]

    return create_user(data, db)
