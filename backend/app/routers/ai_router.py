from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

class AIRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class AIResponse(BaseModel):
    response: str
    model: str
    tokens_used: Optional[int] = None

@router.post("/generate", response_model=AIResponse)
async def generate_ai_response(request: AIRequest):
    """
    Generate AI response based on the provided prompt.
    This endpoint will call external AI APIs.
    """
    try:
        result = await ai_service.generate_response(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_available_models():
    """
    List available AI models.
    """
    return {
        "models": [
            {"id": "gpt-4", "name": "GPT-4", "provider": "OpenAI"},
            {"id": "claude-3", "name": "Claude 3", "provider": "Anthropic"},
            {"id": "gemini-pro", "name": "Gemini Pro", "provider": "Google"}
        ]
    }

@router.get("/status")
async def get_ai_service_status():
    """
    Check the status of AI service.
    """
    return {
        "status": "operational",
        "message": "AI service is ready to handle requests"
    }
