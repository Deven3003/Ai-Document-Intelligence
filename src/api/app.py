from fastapi import FastAPI

app =FastAPI (
    title="AI Document Inteligence API",
    description="Enterprise knowledge and Document Intelligence platform",
    version="0.1.0"

)

@app.get("/health")
def health_check():
    return{
        "status":"healthy",
        "service":"api is working"
    }