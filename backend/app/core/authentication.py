from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.database import init_db
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

get_db = init_db.get_db
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REGISTER_KEY = os.getenv("REGISTER_KEY")
ADMIN_ACCESS_TOKEN = os.getenv("ADMIN_ACCESS_TOKEN")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(http_authorization_credentials=Depends(reusable_oauth2), db: Session = Depends(get_db)):
    if http_authorization_credentials.credentials == ADMIN_ACCESS_TOKEN:
        return
    try:
        payload = jwt.decode(http_authorization_credentials.credentials,
                             SECRET_KEY, algorithms=[ALGORITHM])
        token_expires = datetime.fromtimestamp(payload.get('exp'))

        if datetime.utcnow() > token_expires:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token expired",
            )
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials",
        )
    
def validate_admin_token(http_authorization_credentials=Depends(reusable_oauth2), db: Session = Depends(get_db)):
    if http_authorization_credentials.credentials != ADMIN_ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials",
        )
    
def get_current_username(http_authorization_credentials=Depends(reusable_oauth2), db: Session = Depends(get_db)):
    if http_authorization_credentials.credentials == ADMIN_ACCESS_TOKEN:
        return "admin"
    payload = jwt.decode(http_authorization_credentials.credentials,
                         SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')

def validate_register_key(register_key):
    if register_key != REGISTER_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate register key",
        )