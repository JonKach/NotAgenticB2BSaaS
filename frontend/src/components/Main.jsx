// frontend/src/components/Main.jsx
import React, { useState, useRef } from "react";
import {
  Container,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useRecord } from "./RecordContext";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const Main = () => {
  // transcript is managed in RecordContext
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const navigate = useNavigate();
  const { record, setRecord, transcript: ctxTranscript, setTranscript, generateRecord } = useRecord();

  const handleSeePreview = async () => {
    setError("");
    try {
      setLoading(true);
      if (!record) {
        if (!ctxTranscript) {
          setError("No transcript available to generate a preview.");
          return;
        }
        await generateRecord(ctxTranscript);
      }
      navigate("/record");
    } catch (err) {
      console.error("See preview error:", err);
      setError("Failed to generate preview.");
    } finally {
      setLoading(false);
    }
  };

  const uploadAudio = async (audioBlob) => {
    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.wav");

    try {
      const response = await fetch(`${API_BASE}/process-audio`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed with status: ${response.status}`);
      }

      const result = await response.json();
      console.log("Upload successful:", result);
      // Expect backend to return { transcript: "..." } or similar
      const transcriptText = result.transcript || result.transcription || result.text || "";
      if (transcriptText) {
        // store transcript in context
        setTranscript(transcriptText);
        // generate the health record using context helper
        try {
          setLoading(true);
          await generateRecord(transcriptText);
        } catch (err) {
          console.error("Error generating health record:", err);
          setError("Failed to generate health record from transcript.");
        } finally {
          setLoading(false);
        }
      }
    } catch (err) {
      console.error("Error uploading audio:", err);
      setError(`Error uploading audio: ${err.message}`);
    } finally {
      setIsUploading(false);
    }
  };
 // ---------------------------


 const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
        const url = URL.createObjectURL(audioBlob);
        setAudioUrl(url);
        uploadAudio(audioBlob);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
      setError("Could not access microphone. Please allow permissions.");
    }
 };


 const stopRecording = () => {
   if (mediaRecorderRef.current) {
     mediaRecorderRef.current.stop();
     setIsRecording(false);
     mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
   }
 };


 const handleRecordingToggle = () => {
   if (isRecording) {
     stopRecording();
   } else {
     startRecording();
   }
 };


 // Helper text for the button
  const getButtonText = () => {
    if (isUploading) return "Uploading...";
    if (isRecording) return "Stop Recording";
    return "Start Recording";
  };
  

  return (
    <Container maxWidth="lg">
      {/* Hero section with record button under header/subtitle */}
      <Box sx={{ textAlign: "center", mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          MedScribe
        </Typography>
        <Typography variant="h5" color="text.secondary" gutterBottom>
          Turn doctor–patient conversations into structured EHR-ready notes.
        </Typography>

        {/* Record button directly under header/subtitle */}
        <Box sx={{ mt: 2 }}>
          <Button
            variant="contained"
            size="large"
            onClick={handleRecordingToggle}
            disabled={isUploading}ß
            sx={{ mb: 1 }}
          >
            {isUploading ? (
              <>
                <CircularProgress size={20} sx={{ mr: 1 }} />
                {getButtonText()}
              </>
            ) : (
              getButtonText()
            )}
          </Button>

          {/* Ready status and audio preview under the record button */}
          <Box sx={{ mt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              {isRecording ? "Recording... Click the button again to stop." : "Ready to record."}
            </Typography>
            {audioUrl && (
              <Box sx={{ mt: 1 }}>
                <audio controls src={audioUrl} />
              </Box>
            )}
          </Box>

          {/* See Preview button (navigates to /record). Disabled until a record exists. */}
          <Box sx={{ mt: 2 }}>
            <Button variant="outlined" onClick={handleSeePreview} disabled={isUploading || loading}>
              {loading ? (
                <>
                  <CircularProgress size={16} sx={{ mr: 1 }} /> Generating…
                </>
              ) : (
                "See Preview"
              )}
            </Button>
          </Box>
        </Box>

        <Typography variant="body1" color="text.secondary" sx={{ mt: 3 }}>
          Record, transcribe, and auto-generate encounter notes with ICD-10
          suggestions — in seconds, not hours.
        </Typography>
      </Box>

      {/* Feature cards */}
      <Grid container spacing={3} sx={{ mb: 6 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Record &amp; Transcribe
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Capture clinician–patient conversations with high-accuracy AI
                transcription.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                AI-Generated EHR Notes
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Structured notes following clinical SOAP style with ICD-10
                hints.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Download &amp; Integrate
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Export EHR-ready content and plug into your EMR when accounts
                are live.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Spacer area (recording UI is integrated above) */}
      <Box sx={{ mb: 4 }} />

      {error && (
        <Box sx={{ mb: 2 }}>
          <Alert severity="error">{error}</Alert>
        </Box>
      )}

      {/* no generate button — recording uploads automatically */}
    </Container>
  );
};

export default Main;