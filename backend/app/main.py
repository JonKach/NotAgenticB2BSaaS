from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai_router
from fastapi import HTTPException
import httpx
import os
import google.generativeai as genai

from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse
import aiofiles


import assemblyai as aai
from .routers import clinical_router
from pydantic import BaseModel

class TranscriptPayload(BaseModel):
    transcript: str

os.makedirs("uploads", exist_ok=True)
genai.configure(api_key="AIzaSyB34b_kr7Cy9cic19q8YjbJ-QyRzyikqhM")


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
app.include_router(clinical_router.router, prefix="/api/clinical", tags=["Clinical"])


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




@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
   # Validate MIME type
   if file.content_type not in ["audio/wav", "audio/x-wav"]:
       raise HTTPException(
           status_code=400,
           detail="Invalid file type. Only .wav files are supported."
       )


   # Read file into memory
   audio_bytes = await file.read()


   # Optional: save uploaded file
   save_path = f"uploads/{file.filename}"
   async with aiofiles.open(save_path, "wb") as out_file:
       await out_file.write(audio_bytes)


   aai.settings.api_key = "590c01ff353e4117873acb850eab27e9"


   # audio_file = "./local_file.mp3"
   audio_file = save_path


   config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.universal)


   transcript = aai.Transcriber(config=config).transcribe(audio_file)


   if transcript.status == "error":
       raise RuntimeError(f"Transcription failed: {transcript.error}")


   print(transcript.text)
   # Temporary mock response
   result = {
       "message": transcript.text
   }


   return JSONResponse(content=result)

@app.post("/process-transcript")
async def process_transcript(text: str = Body(..., embed=False)):
   
    client = genai.GenerativeModel("gemini-2.5-flash")

    prompt = '''
    You are MedScribe-Reasoner, an AI clinical reasoning specialist. Your task is to take raw clinician–patient dialogue and produce accurate, formatted clinical note according to the doctor’s preferences.

Do not hallucinate. Do not invent findings, diagnoses, medications, or values not supported by the transcript. If information is missing, explicitly mark it as missing.

You will be given:
- transcript: the raw transcribed dialogue


Your tasks:

1. Extract info from the transcript:

2. Generate the final clinical note:
   - Follow the requested note_format strictly.
   - Apply doctor_preferences exactly.
   - Map extracted content into the ehr_field_schema fields.
   - The note must be polished, structured, and ready for inclusion in an EHR.

3. Output the final result strictly as one report that describes the EHR: 


No commentary outside the EHR. No extra text. Add "\n" new lines where appropriate for readability.
--- INPUTS ---
transcript: ${transcript}
'''

    response = client.generate_content(
        prompt + f"transcript: {text}",
    )   # Validate MIME type


    print(response.text)
    result = {
        "response": response.text
    }


    return JSONResponse(content=result)