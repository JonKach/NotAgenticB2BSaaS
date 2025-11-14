from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai_router
from fastapi import HTTPException
import httpx

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

@app.post("/process-transcript")
async def process_transcript(payload: str):
    """
    Accepts a transcript string in the JSON body, sends it to a placeholder AI API,
    and returns the AI response.
    """

    transcript = payload

    if not transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")

    # Placeholder AI API endpoint (replace with real one)
    AI_API_URL = "https://api.placeholder-ai.com/v1/generate"

    # Example payload for the AI API
    data = {
        "model": "demo-model",
        "input": transcript
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            ai_response = await client.post(AI_API_URL, json=data)

        ai_response.raise_for_status()
        ai_output = ai_response.json()

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"AI API error: {str(e)}")

    return {
        "input_transcript": transcript,
        "ai_output": ai_output
    }