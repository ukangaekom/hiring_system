from fastapi import APIRouter
from app.api.v1.endpoints import users, organizations

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
# api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"]) # Will add later
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"]) # Not needed if login is in users/orgs
