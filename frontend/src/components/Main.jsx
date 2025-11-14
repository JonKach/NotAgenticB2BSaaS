import React, { useState, useRef } from 'react';
import { Container, Typography, Box, Button, Grid, Card, CardContent } from '@mui/material';


const Main = () => {
 const [isRecording, setIsRecording] = useState(false);
 const [audioUrl, setAudioUrl] = useState(null);
 const [isUploading, setIsUploading] = useState(false); // New state for loading
  const mediaRecorderRef = useRef(null);
 const audioChunksRef = useRef([]);


 // --- NEW UPLOAD FUNCTION ---
 const uploadAudio = async (audioBlob) => {
   setIsUploading(true); // Start loading
  
   const formData = new FormData();
   formData.append('file', audioBlob, 'recording.wav');


   try {
     // Replace with your actual API endpoint
     const response = await fetch("http://localhost:8000/process-audio", {
       method: 'POST',
       body: formData,
     });


     if (!response.ok) {
       throw new Error(`Upload failed with status: ${response.status}`);
     } else {
       console.log(response.data);
     }


     const result = await response.json();
     console.log('Upload successful:', result);
     alert('Upload successful!');
    
   } catch (error) {
     console.error('Error uploading audio:', error);
     alert(`Error uploading audio: ${error.message}`);
   } finally {
     setIsUploading(false); // Stop loading, even if it failed
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
       if (event.data.size > 0) {
         audioChunksRef.current.push(event.data);
       }
     };


     mediaRecorder.onstop = () => {
       const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
       const url = URL.createObjectURL(audioBlob);
       setAudioUrl(url);
      
       // --- CALL THE UPLOAD FUNCTION ---
       uploadAudio(audioBlob);
     };


     mediaRecorder.start();
     setIsRecording(true);
    
   } catch (error) {
     console.error("Error accessing microphone:", error);
     alert("Could not access microphone. Please allow permissions.");
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
   if (isUploading) return 'Uploading...';
   if (isRecording) return 'Stop Recording';
   return 'Start Recording';
 };


 return (
   <Box sx={{ flexGrow: 1, py: 8 }}>
     <Container maxWidth="lg">
       <Box sx={{ textAlign: 'center', mb: 6 }}>
         {/* ... (Your Typography) ... */}
        
         <Button
           variant="contained"
           size="large"
           color={isRecording ? "error" : "primary"}
           sx={{ mt: 2 }}
           onClick={handleRecordingToggle}
           disabled={isUploading} // Disable button while uploading
         >
           {getButtonText()}
         </Button>


         {audioUrl && !isUploading && ( // Hide player while uploading
           <Box sx={{ mt: 4, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
             <audio controls src={audioUrl} />
             <Button variant="outlined" href={audioUrl} download="recording.wav">
               Download Recording
             </Button>
           </Box>
         )}
       </Box>


       {/* ... (Your Grid) ... */}


     </Container>
   </Box>
 );
};


export default Main;
