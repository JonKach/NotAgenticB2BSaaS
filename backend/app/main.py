from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai_router

app = FastAPI(
    title="NotAgenticB2BSaaS API",
    description="Backend API for AI-powered B2B SaaS solution",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_router.router, prefix="/api/ai", tags=["AI"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to NotAgenticB2BSaaS API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
