import jwt
from typing import Generator, Optional
from fastapi import Depends
from sqlmodel import Session, select
from database.db import engine
from database.models.user import User
from core.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"



def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    """Get the current authenticated user or None if not authenticated."""
    if not token:
        return None
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None
        
    user = db.exec(select(User).where(User.id == user_id)).first()
    return user