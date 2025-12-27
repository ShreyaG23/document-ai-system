from fastapi import FastAPI
from src.api.routes import router


app = FastAPI(
    title="Document AI System",
    version = "1.0.0",
    description = "upload doc, extract texts, summarize translate and QA"
)

#health check 
@app.get("/health")
def health_check():
    return {"status": "running", "message": "Document AI System API is live!"}

app.include_router(router)