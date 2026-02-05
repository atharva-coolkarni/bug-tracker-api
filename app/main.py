from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.projects import router as project_router


app = FastAPI(title="Bug Tracker API")

app.include_router(auth_router)
app.include_router(project_router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
