from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
import google.auth.transport.requests
import google.oauth2.id_token
from google_auth_oauthlib.flow import Flow
import os
import json
from models import User
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
REDIRECT_URI = "https://triumphant-commitment-production.up.railway.app/auth/google/callback"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_SECRET_JSON = os.getenv("GOOGLE_CLIENT_SECRET_JSON")
if not GOOGLE_CLIENT_SECRET_JSON:
    raise RuntimeError("Missing GOOGLE_CLIENT_SECRET_JSON environment variable")

@router.get("/auth/google/login")
def login_via_google():
    flow = Flow.from_client_config(
        json.loads(GOOGLE_CLIENT_SECRET_JSON),
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"
        ],
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(prompt='consent')
    return RedirectResponse(url=authorization_url)

@router.get("/auth/google/callback")
def auth_google_callback(request: Request, db: Session = Depends(get_db)):
    state = request.query_params.get("state")
    if not state:
        return {"error": "Missing state in query"}

    flow = Flow.from_client_config(
        json.loads(GOOGLE_CLIENT_SECRET_JSON),
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"
        ],
        state=state,
        redirect_uri=REDIRECT_URI
    )

    flow.fetch_token(authorization_response=str(request.url))

    credentials = flow.credentials
    request_session = google.auth.transport.requests.Request()

    id_info = google.oauth2.id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=request_session,
        audience=GOOGLE_CLIENT_ID,
    )

    email = id_info.get("email")
    user = db.query(User).filter(User.email == email).first()

    FRONTEND_URL = "https://quizzeria-world.netlify.app/login"
    if user:
        return RedirectResponse(url=f"{FRONTEND_URL}?email={email}")
    else:
        return RedirectResponse(url=f"{FRONTEND_URL}?error=not_registered")
