# Hiring System

A robust and scalable backend system designed to connect job seekers with organizations. This platform facilitates user registration, profile management, organization verification, and job application processes.

## 🚀 Features

-   **User Management**: Secure registration and login for job seekers.
-   **Organization Management**: Dedicated portal for companies to register and manage their profiles.
-   **Job Board**: (In Progress) Infrastructure for posting and managing job openings.
-   **Application Tracking**: (In Progress) System to track job applications.
-   **Profile Enhancements**:
    -   Detailed user profiles (Education, Experience, etc.).
    -   CV/Resume upload and management.
-   **Security**:
    -   Password hashing using Argon2.
    -   JWT-based authentication.
    -   Role-based access control (User vs. Organization).

## 🛠️ Tech Stack

-   **Language**: Python 3.10+
-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High performance, easy to learn, fast to code, ready for production.
-   **Database**: [PostgreSQL](https://www.postgresql.org/) - The World's Most Advanced Open Source Relational Database.
-   **ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) - SQL databases in Python, designed to simplify interacting with SQL databases.
-   **Containerization**: [Docker](https://www.docker.com/) & Docker Compose.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

-   [Python 3.10+](https://www.python.org/downloads/)
-   [Docker Desktop](https://www.docker.com/products/docker-desktop) (or Docker Engine + Compose)
-   [Git](https://git-scm.com/)

## ⚡ Getting Started

### 1. Clone the Repository

```bash
git clone <repository_url>
cd hiring_system
```

### 2. Environment Configuration

Create a `.env` file in the root directory. You can use the example below:

```bash
# .env
DATABASE_URL=postgresql://app_user:app_password@localhost:5432/edu_pro
SECRET_KEY=your_super_secret_key_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Database Setup

Start the PostgreSQL database using Docker Compose:

```bash
docker compose up -d db
```

This command starts a PostgreSQL container mapped to port `5432` with the credentials specified in `compose.yml`.

### 4. Install Dependencies

It is recommended to use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## 🏃 Running the Application

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## 📚 API Documentation

FastAPI provides automatic interactive documentation:

-   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) - Interactive exploration and testing of API endpoints.
-   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) - Alternative, clean documentation view.

## 📂 Project Structure

```
hiring_system/
├── app/
│   ├── api/            # API endpoints (v1)
│   ├── core/           # Configuration, Security, Database setup
│   ├── models/         # Database models (SQLModel)
│   ├── schemas/        # Pydantic schemas for verification/responses
│   └── main.py         # Application entry point
├── tests/              # Test suite
├── uploads/            # Directory for user uploaded files (CVs)
├── compose.yml         # Docker Compose configuration
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🗄️ Database Inspection

You can connect to the running PostgreSQL container to inspect tables directly:

```bash
docker exec -it hiringsystem psql -U app_user -d edu_pro
```

Common commands inside `psql`:
-   `\dt`: List tables
-   `\d table_name`: Describe table schema
-   `SELECT * FROM "user";`: Select all users (note the quotes for reserved keywords)