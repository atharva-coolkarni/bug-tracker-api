from fastapi import FastAPI

app = FastAPI(title="Bug Tracker API")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
