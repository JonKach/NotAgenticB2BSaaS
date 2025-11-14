# backend/app/routers/clinical_router.py
from datetime import datetime
import json
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


class TranscriptPayload(BaseModel):
    transcript: str


@router.post("/health-record")
async def transcript_to_health_record(payload: TranscriptPayload) -> Dict[str, Any]:
    """
    Takes a raw clinician–patient transcript and returns a structured
    health record JSON object suitable for rendering in the UI.
    """
    transcript = payload.transcript.strip()
    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript cannot be empty")

    # Prompt that your real AI model will eventually follow
    prompt = f"""
You are an EHR scribe. Given the following doctor–patient conversation
transcript, create a structured JSON object with the fields:

- patient_name (string or null)
- dob (string or null)
- mrn (string or null)
- encounter_datetime (ISO 8601 string)
- chief_complaint (string)
- hpi (string)
- assessment (string)
- plan (string)
- icd10_codes: list of objects with fields:
    - code (string)
    - description (string)

Return **ONLY** valid JSON, no explanations or markdown.

Transcript:
{transcript}
"""

    # Call your AI service (currently mocked in AIService)
    ai_result = await ai_service.generate_response(prompt=prompt)

    # ai_result["response"] is currently just "AI response to: ...".
    # If in the future it’s already JSON, we’ll parse it.
    raw_response = ai_result.get("response", "")

    record: Dict[str, Any]
    try:
        # Try to interpret AI response as JSON (future, real model)
        record = json.loads(raw_response)
    except Exception:
        # Fallback demo structure so your frontend can still work today
        record = {
            "patient_name": "Demo Patient",
            "dob": None,
            "mrn": None,
            "encounter_datetime": datetime.utcnow().isoformat() + "Z",
            "chief_complaint": "Auto-derived from transcript (demo)",
            "hpi": transcript,
            "assessment": raw_response or "AI assessment placeholder",
            "plan": "Follow standard of care. This is demo content only.",
            "icd10_codes": [
                {
                    "code": "R69",
                    "description": "Illness, unspecified (demo placeholder)",
                }
            ],
        }

    return {
        "record": record,
        "raw_ai": ai_result,  # you can ignore this on the frontend if you want
    }

