from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from apis.deps import get_db
from database.models.user import User
from schemas.auth import (
    UserSignupRequest, UserLoginRequest,
    UserResponse, TokenResponse,
    SignupResponse
)
from core.security import get_password_hash, verify_password, create_access_token
from utils.rate_limiter import limiter
from utils.constants import constants
from apis.deps import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(constants.SLOW_RATE_LIMIT)
async def signup(request: Request, user_data: UserSignupRequest, db: Session = Depends(get_db)):
    existing_user = db.exec(select(User).where(User.username == user_data.username.lower())).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    user = User(
        username=user_data.username.lower(),
        email=user_data.email,
        full_name=user_data.full_name,
        password=get_password_hash(user_data.password),
        is_active=True,
        is_staff=False,
        is_superuser=False
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return SignupResponse(
        user=UserResponse.model_validate(user),
        token=TokenResponse(
            access_token=access_token,
        )
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit(constants.SLOW_RATE_LIMIT)
async def login(request: Request, login_data: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.exec(select(User).where((User.username == login_data.username.lower()) | (User.email == login_data.username))).first()
    
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"},)
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})    
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Optional[User] = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return UserResponse.model_validate(current_user)
