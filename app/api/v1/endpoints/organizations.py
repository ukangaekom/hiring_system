from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Any

from app.api import deps
from app.core import security
from app.core.database import get_session
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationRead
from app.schemas.token import Token

router = APIRouter()

@router.post("/register", response_model=OrganizationRead)
def register_organization(
    *,
    session: Session = Depends(get_session),
    org_in: OrganizationCreate,
) -> Any:
    """
    Register a new organization.
    """
    org = session.exec(select(Organization).where(Organization.email == org_in.email)).first()
    if org:
        raise HTTPException(
            status_code=400,
            detail="An organization with this email already exists.",
        )
    
    org_obj = Organization.model_validate(
        org_in, update={"password_hash": security.get_password_hash(org_in.password)}
    )
    session.add(org_obj)
    session.commit()
    session.refresh(org_obj)
    return org_obj

@router.post("/login", response_model=Token)
def login_organization(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login for organizations.
    """
    org = session.exec(select(Organization).where(Organization.email == form_data.username)).first()
    if not org or not security.verify_password(form_data.password, org.password_hash):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )
    
    # We'll need to handle the token generation consistently
    return {
         "access_token": security.create_access_token(
            org.id, role="organization"
        ),
        "token_type": "bearer",
    }

from app.models.job import Job
from app.models.application import Application
from app.models.user import User
from app.schemas.job import JobCreate, JobRead
from app.models.organization import Organization
from typing import List

@router.post("/jobs", response_model=JobRead)
def create_job(
    *,
    session: Session = Depends(get_session),
    job_in: JobCreate,
    current_org: Organization = Depends(deps.get_current_organization),
) -> Any:
    """
    Create a new job posting.
    """
    job = Job.model_validate(job_in, update={"organization_id": current_org.id})
    session.add(job)
    session.commit()
    session.refresh(job)
    return job

@router.get("/jobs", response_model=List[JobRead])
def read_jobs(
    session: Session = Depends(get_session),
    current_org: Organization = Depends(deps.get_current_organization),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve jobs created by the current organization.
    """
    return session.exec(
        select(Job).where(Job.organization_id == current_org.id).offset(skip).limit(limit)
    ).all()

@router.get("/applications/{application_id}/cv")
def download_applicant_cv(
    *,
    session: Session = Depends(get_session),
    application_id: int,
    current_org: Organization = Depends(deps.get_current_organization),
) -> Any:
    """
    Download the CV for a specific job application.
    Only the organization that posted the job can download the CV.
    """
    application = session.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    job = session.get(Job, application.job_id)
    if not job or job.organization_id != current_org.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this CV."
        )
    
    user = session.get(User, application.user_id)
    if not user or not user.cv_path:
        raise HTTPException(status_code=404, detail="CV not found for this applicant")
    
    return FileResponse(user.cv_path)

