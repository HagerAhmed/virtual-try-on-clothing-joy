from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from ..models import User, UserCreate, UserLogin, AuthResponse, Token
from ..database import users, user_passwords
from ..auth_utils import verify_password, get_password_hash, create_access_token, decode_access_token, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    Raises 401 if token is invalid or expired.
    """
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
    except JWTError as e:
        # Check if token is expired
        if "expired" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise credentials_exception
    
    user = users.get(email)
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user.
    This endpoint is used to verify the token and get user details.
    """
    return current_user

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    """
    Create a new user account and return authentication token.
    """
    if user.email in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password strength
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
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
    
    # Create and return token directly
    access_token = create_access_token(data={"sub": user.email})
    return {"token": access_token, "user": new_user}

@router.post("/login", response_model=AuthResponse)
async def login(user_credentials: UserLogin):
    """
    Authenticate user and return JWT token.
    """
    user = users.get(user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    hashed_password = user_passwords.get(user_credentials.email)
    if not hashed_password or not verify_password(user_credentials.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"token": access_token, "user": user}

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint (token invalidation handled on client side).
    """
    return {"message": "Successfully logged out"}

@router.post("/forgot-password")
async def forgot_password(email_data: dict):
    """
    Mock implementation for password reset.
    """
    return {"message": "Password reset email sent"}
