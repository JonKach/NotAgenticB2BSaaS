import os
from typing import Optional
import httpx
from dotenv import load_dotenv
from .ai_validator import AIValidator

load_dotenv()

class AIService:
    """
    Service for handling AI API calls.
    This is where external AI API integrations will be implemented.
    """
    
    def __init__(self):
        self.api_key = os.getenv("AI_API_KEY", "")
        self.base_url = os.getenv("AI_API_BASE_URL", "")
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = 1000,
        temperature: Optional[float] = 0.7
    ) -> dict:
        """
        Generate AI response from the provided prompt.
        
        Args:
            prompt: The input prompt for the AI
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0-1)
        
        Returns:
            dict: Response containing AI-generated text and metadata
        """
        
        # Placeholder implementation
        # In production, this would call actual AI APIs (OpenAI, Anthropic, etc.)
        
        # Example structure for when API is integrated:
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         f"{self.base_url}/completions",
        #         headers={"Authorization": f"Bearer {self.api_key}"},
        #         json={
        #             "prompt": prompt,
        #             "max_tokens": max_tokens,
        #             "temperature": temperature
        #         }
        #     )
        #     return response.json()
        
        # For now, return a mock response
        response = {
            "response": f"AI response to: {prompt[:50]}...",
            "model": "mock-model-v1",
            "tokens_used": len(prompt.split())
        }

        # Run validation/sanitization using AIValidator before returning
        try:
            validator = AIValidator()
            validation_report = await validator.validate(response)
            # attach validation report alongside the AI response
            response["validation"] = validation_report
        except Exception:
            # never fail the AI service if validator has an issue; return response without validation
            response["validation"] = {"error": "validation_failed"}

        return response
    
    async def call_external_ai_api(self, endpoint: str, payload: dict) -> dict:
        """
        Generic method to call external AI APIs.
        
        Args:
            endpoint: The API endpoint to call
            payload: The request payload
        
        Returns:
            dict: Response from the AI API
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
