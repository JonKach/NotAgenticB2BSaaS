from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ai_router
from fastapi import HTTPException
import httpx
import os


from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import aiofiles


import assemblyai as aai


os.makedirs("uploads", exist_ok=True)


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