from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Any, List
from pathlib import Path
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile

from app.api import deps
from app.core import security
from app.core.database import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.models.user import User
from app.models.job import Job
from app.models.application import Application
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.schemas.token import Token
from app.schemas.job import JobRead
from app.core import config

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(
    *,
    session: Session = Depends(get_session),
    user_in: UserCreate,
) -> Any:
    """
    Register a new user.
    """
    user = session.exec(select(User).where(User.email == user_in.email)).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    
    user_obj = User.model_validate(
        user_in, update={"password_hash": security.get_password_hash(user_in.password)}
    )
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    return user_obj

@router.post("/login", response_model=Token)
def login_user(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    
    # We store role in token to distinguish
    access_token_expires = security.settings.ACCESS_TOKEN_EXPIRE_MINUTES
    return {
        "access_token": security.create_access_token(
            user.id, role="user"
        ),
        "token_type": "bearer",
    }

@router.post("/upload-cv", response_model=UserRead)
def upload_cv(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user),
    file: UploadFile = File(...),
) -> Any:
    """
    Upload CV for the current user.
    """
    upload_dir = Path(config.settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_location = upload_dir / f"user_{current_user.id}_{file.filename}"
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    current_user.cv_path = str(file_location)
    current_user.is_verified = True # Assume uploading CV verifies profile
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.get("/jobs", response_model=List[JobRead])
def list_jobs(
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List available jobs for users to apply.
    """
    return session.exec(select(Job).offset(skip).limit(limit)).all()

@router.post("/apply/{job_id}")
def apply_for_job(
    job_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Apply for a specific job.
    """
    # Check if job exists
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    # Check if already applied
    existing_application = session.exec(
        select(Application)
        .where(Application.user_id == current_user.id)
        .where(Application.job_id == job_id)
    ).first()
    
    if existing_application:
        raise HTTPException(status_code=400, detail="Already applied for this job")
        
    application = Application(user_id=current_user.id, job_id=job_id)
    session.add(application)
    session.commit()
    session.refresh(application)
    return {"message": "Application submitted successfully", "application_id": application.id}
