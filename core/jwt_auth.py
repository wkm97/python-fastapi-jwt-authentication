from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from pydantic import BaseModel

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 0.1
REFRESH_TOKEN_EXPIRE_MINUTES = 10

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: str
    refresh_token: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserInDB(User):
    hashed_password: str

class JwtAuthentication:
    def __init__(self):
        self.issuer = "DST_BI jwt authenticator"

    def get_user(self, username:str):
        if username in fake_users_db:
            user_dict = fake_users_db[username]
            return UserInDB(**user_dict)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"iss": self.issuer, "exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_refresh = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_refresh
    
    def refresh_access_token(self, token:str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authorized to Access the server",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_expired_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Refresh Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get('sub')
            return self.create_access_token(data={"sub": username})
        except ExpiredSignatureError:
            raise token_expired_exception
        except JWTError:
            raise credentials_exception
    
    def get_payload(self, token:str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_expired_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Access Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise token_expired_exception
        except JWTError:
            raise credentials_exception
    
    def validate_access_token(self, token:str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        token_expired_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Access Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return True
        except ExpiredSignatureError:
            raise token_expired_exception
        except JWTError:
            raise credentials_exception
            