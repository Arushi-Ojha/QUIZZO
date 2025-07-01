import smtplib
from email.message import EmailMessage
import random
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

otp_store: Dict[str, str] = {}

SENDER_EMAIL = "arushiojha100@gmail.com"
APP_PASSWORD = "wlzr pnei jffr ompy"  

class EmailRequest(BaseModel):
    email: str

class SignupData(BaseModel):
    username: str
    email: str
    password: str
    role: str
    otp: str

@router.post("/auth/send-otp")
def send_otp(request: EmailRequest):
    otp = str(random.randint(100000, 999999))
    otp_store[request.email] = otp

    msg = EmailMessage()
    msg.set_content(f"Your OTP for QUIZZERIA signup is: {otp}")
    msg["Subject"] = "QUIZZERIA Signup OTP"
    msg["From"] = SENDER_EMAIL
    msg["To"] = request.email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {e}")

    return {"detail": "OTP sent successfully"}

@router.post("/auth/verify-otp-and-signup")
def verify_otp_and_signup(data: SignupData):
    stored_otp = otp_store.get(data.email)
    if not stored_otp or data.otp != stored_otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    del otp_store[data.email]

    return {"detail": "Signup successful"}
