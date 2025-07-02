import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# Load Firebase credentials only once
cred = credentials.Certificate("app/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="firebase")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        decoded = firebase_auth.verify_id_token(token)
        return decoded["uid"]
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )
