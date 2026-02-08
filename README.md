# 🐞 Bug Tracker API

A production-style backend system for managing projects, issues, team collaboration and issue tracking workflows.

Built with **FastAPI**, **PostgreSQL**, **JWT (RS256)** authentication, **RBAC**, and fully **Dockerized**.

---

## 🚀 Features

- User registration & login
- JWT authentication with RS256 asymmetric signing
- Role-Based Access Control (RBAC): admin / manager / developer / reporter
- Project CRUD operations
- Issue lifecycle management (create → assign → comment → close)
- Comment system on issues
- Strict ownership & permission enforcement
- Database migrations with Alembic
- Docker + Docker Compose setup

---

## 🧱 Tech Stack

| Layer            | Technology             |
|------------------|------------------------|
| API Framework    | FastAPI                |
| ORM              | SQLAlchemy 2.x         |
| Database         | PostgreSQL             |
| Migrations       | Alembic                |
| Authentication   | JWT (RS256)            |
| Containerization | Docker / Docker Compose|

---

## 🏗️ Project Structure

```
app/
├── api/            → routes, endpoints, dependencies
├── core/           → config, security, jwt utils
├── db/             → database session & engine
├── models/         → SQLAlchemy ORM models
├── services/       → business logic layer (extensible)
├── schemas/        → Pydantic models for request/response
└── main.py         → application entry point
```

Authentication & authorization are cleanly handled using **FastAPI dependency injection**.

---

## 🐳 Run with Docker (Recommended)

### Prerequisites
- Docker
- Docker Compose

### Start the application

```bash
# Build and start all services
docker compose up --build
```

API will be available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 💻 Run Locally (without Docker)

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Create and configure `.env` file

```env
# Example .env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/bugtracker
SECRET_KEY=your-very-long-random-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

3. Run database migrations

```bash
# Apply all migrations
alembic upgrade head
```

4. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

---

## 🔐 Authentication Flow

1. Register a new user  
   `POST /auth/register`

2. Login to receive tokens  
   `POST /auth/login`

3. Use the **access token** in requests:

```
Authorization: Bearer <access_token>
```

Swagger UI supports the `Authorize` button — paste the token there.

---

## 👥 Roles & Permissions

| Action             | Admin | Manager | Developer | Reporter |
|--------------------|-------|---------|-----------|----------|
| Create project     | ✅    | ✅      | ❌        | ❌       |
| Delete project     | ✅    | ❌      | ❌        | ❌       |
| Create issue       | ✅    | ✅      | ✅        | ✅       |
| Assign issue       | ✅    | ✅      | ❌        | ❌       |
| Comment on issue   | ✅    | ✅      | ✅        | ✅       |
| Close issue        | ✅    | ✅      | ❌        | ❌       |

---

## 🧪 Quick Example Workflow

1. Create an admin user
2. Login as admin
3. Create a new project
4. Create an issue in that project
5. Assign the issue to a developer
6. Developer adds comments
7. Manager / Admin closes the issue

---

## 🧠 Key Design Decisions

- **RS256** JWT → secure asymmetric signing (public key can be shared)
- Authorization enforced via **FastAPI dependencies** (clean & reusable)
- **Ownership checks** derived from JWT claims — never trust client input
- **Alembic** for reproducible, versioned database migrations
- Dockerized setup → consistent environments across development & review
- Layered architecture → easy to extend with new features

---

## 🔮 Future Improvements / Roadmap

- Pagination & filtering for lists
- Full-text search for issues
- Email notifications (issue assigned, commented, closed…)
- File/image attachments on issues & comments
- Rate limiting & better error handling
- Structured logging + observability (OpenTelemetry?)
- Automated tests (unit + integration)
- CI/CD pipeline

---