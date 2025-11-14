import React from 'react';
import { Container, Typography, Box, Button, Grid, Card, CardContent } from '@mui/material';

const Main = () => {
  return (
    <Box sx={{ flexGrow: 1, py: 8 }}>
      <Container maxWidth="lg">
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h2" component="h1" gutterBottom>
            Welcome to MedScribe
          </Typography>
          <Typography variant="h5" color="text.secondary" paragraph>
            AI-powered medical documentation for clinicians
          </Typography>
          <Button variant="contained" size="large" sx={{ mt: 2 }}>
            Start Recording
          </Button>
        </Box>

        <Grid container spacing={4} sx={{ mt: 4 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom>
                  Record & Transcribe
                </Typography>
                <Typography color="text.secondary">
                  Capture clinician-patient conversations with high-accuracy AI transcription.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom>
                  AI-Generated EHR Notes
                </Typography>
                <Typography color="text.secondary">
                  Structured, doctor-formatted notes with differential diagnoses and ICD-10 codes.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom>
                  Download & Integrate
                </Typography>
                <Typography color="text.secondary">
                  Clean, downloadable EHR-ready documents with accurate extractions.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Main;
