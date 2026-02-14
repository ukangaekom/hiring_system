from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import pytest
from app.main import app
from app.core.database import get_session
from app.models.user import User
from app.models.organization import Organization
from app.models.job import Job
from app.models.application import Application
import io

# Setup in-memory database for testing
engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

def create_test_db():
    print(f"Creating tables. Metadata tables: {SQLModel.metadata.tables.keys()}")
    SQLModel.metadata.create_all(engine)

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

client = TestClient(app)

@pytest.fixture(name="session", autouse=True)
def session_fixture():
    create_test_db()
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

def test_full_hiring_flow():
    # 1. Register Organization
    org_data = {
        "email": "tech@corp.com", 
        "password": "password", 
        "name": "Tech Corp",
        "industry": "Software",
        "phone": "555-0199"
    }
    response = client.post("/api/v1/organizations/register", json=org_data)
    assert response.status_code == 200
    org_id = response.json()["id"]
    assert response.json()["industry"] == "Software"

    # 2. Login Organization
    login_data = {"username": "tech@corp.com", "password": "password"}
    response = client.post("/api/v1/organizations/login", data=login_data)
    assert response.status_code == 200
    org_token = response.json()["access_token"]
    org_headers = {"Authorization": f"Bearer {org_token}"}

    # 3. Create Job
    job_data = {
        "title": "Python Developer",
        "description": "Backend role",
        "requirements": "FastAPI knowledge",
        "department": "Engineering",
        "min_age": 21,
        "max_age": 40
    }
    response = client.post("/api/v1/organizations/jobs", json=job_data, headers=org_headers)
    assert response.status_code == 200
    job_id = response.json()["id"]
    assert response.json()["department"] == "Engineering"

    # 4. Register User
    user_data = {
        "email": "john@doe.com", 
        "password": "password", 
        "full_name": "John Doe",
        "gender": "Male",
        "phone": "1234567890"
    }
    response = client.post("/api/v1/users/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["gender"] == "Male"
    
    # 5. Login User
    login_data = {"username": "john@doe.com", "password": "password"}
    response = client.post("/api/v1/users/login", data=login_data)
    assert response.status_code == 200
    user_token = response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    # 6. List Jobs
    response = client.get("/api/v1/users/jobs", headers=user_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == "Python Developer"

    # 7. Upload CV
    # Mock file upload
    file_content = b"This is a fake CV."
    files = {"file": ("cv.pdf", file_content, "application/pdf")}
    response = client.post("/api/v1/users/upload-cv", files=files, headers=user_headers)
    assert response.status_code == 200
    assert response.json()["is_verified"] == True
    assert "cv.pdf" in response.json()["cv_path"]

    # 8. Apply for Job
    response = client.post(f"/api/v1/users/apply/{job_id}", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Application submitted successfully"
    application_id = response.json()["application_id"]

    # 9. Duplicate Application Check
    response = client.post(f"/api/v1/users/apply/{job_id}", headers=user_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Already applied for this job"

    # 10. Check Application Count (Organization viewpoint)
    response = client.get("/api/v1/organizations/jobs", headers=org_headers)
    assert response.status_code == 200
    # Find the job we created
    job_in_list = next(j for j in response.json() if j["id"] == job_id)
    assert job_in_list["application_count"] == 1

    # 11. Download Applicant CV (Organization viewpoint)
    response = client.get(f"/api/v1/organizations/applications/{application_id}/cv", headers=org_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content == b"This is a fake CV."

if __name__ == "__main__":
    # Allow running directly or via pytest
    try:
        test_full_hiring_flow()
        print("Test passed successfully!")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
