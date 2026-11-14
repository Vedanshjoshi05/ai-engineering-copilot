from fastapi import FastAPI

from app.routes.github import router as github_router



app=FastAPI(
    title="Nexora-AI Software Enigeering Copilot",
    description="AI-powered software engineering assistant",
    version="1.0.0"
)
app.include_router(github_router)
@app.get("/")
def home():
    return {
        "message":"Welcome to Nexora-AI Software Enigeering Copilot",
        "status":"success"
    }
@app.get("/health")
def health_check():
    return {
        "status":"healthy"
    }