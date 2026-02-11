from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core import security
from app.core.config import settings
from app.core.database import get_session
from app.models.user import User
from app.models.organization import Organization
from app.schemas.token import TokenData

# We might need two generic token URLs in swagger, but for now let's point to user login
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login"
)

def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenData(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Check if subject is an ID (assuming user ID)
    # We might need to differentiate between user and org in the token
    # For now, let's assume if it's a user endpoint, we look for a user
    
    user = session.get(User, int(token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_organization(
    session: Session = Depends(get_session),
    token: str = Depends(reusable_oauth2) 
) -> Organization:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenData(**payload)
        # We can add a 'role' or 'type' claim to the token to be sure
        if token_data.role != "organization":
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not an organization",
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    org = session.get(Organization, int(token_data.sub))
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
