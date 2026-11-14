from fastapi import FastAPI
app=FastAPI(
    title="Nexora-AI Software Enigeering Copilot",
    description="AI-powered software engineering assistant",
    version="1.0.0"
)
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