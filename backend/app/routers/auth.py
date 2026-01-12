from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from ..models import User, UserCreate, UserLogin, AuthResponse, Token
from ..database import users, user_passwords
from ..auth_utils import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = users.get(email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    if user.email in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    user_passwords[user.email] = hashed_password
    
    # Create new user
    new_user_id = len(users) + 1
    new_user = User(
        id=new_user_id,
        email=user.email,
        full_name=user.full_name
    )
    users[user.email] = new_user
    
    access_token = create_access_token(data={"sub": user.email})
    return {"token": access_token, "user": new_user}

@router.post("/login", response_model=AuthResponse)
async def login(user_credentials: UserLogin):
    user = users.get(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    hashed_password = user_passwords.get(user_credentials.email)
    if not verify_password(user_credentials.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"token": access_token, "user": user}

@router.post("/forgot-password")
async def forgot_password(email_data: dict):
    # Mock implementation
    return {"message": "Password reset email sent"}
