// frontend/src/components/HealthRecordPage.jsx
import React from "react";
import {
  Container,
  Paper,
  Typography,
  Box,
  Grid,
  Divider,
  Chip,
  Button,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useRecord } from "./RecordContext";
import { jsPDF } from "jspdf";

const HealthRecordPage = () => {
  const { record } = useRecord();
  const navigate = useNavigate();

  if (!record) {
    return (
      <Container maxWidth="md">
        <Box sx={{ mt: 6, textAlign: "center" }}>
          <Typography variant="h5" gutterBottom>
            No health record yet
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
            Generate a note from a transcript on the main page first.
          </Typography>
          <Button variant="contained" onClick={() => navigate("/")}>
            Go back to transcript
          </Button>
        </Box>
      </Container>
    );
  }

  const {
    patient_name,
    dob,
    mrn,
    encounter_datetime,
    chief_complaint,
    hpi,
    assessment,
    plan,
    icd10_codes = [],
  } = record;

  const safePatientName = patient_name || "patient";
  const fileSafeName = safePatientName
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

  const handleDownloadJson = () => {
    const blob = new Blob([JSON.stringify(record, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `health-record-${fileSafeName || "encounter"}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadPdf = () => {
    const doc = new jsPDF({
      orientation: "portrait",
      unit: "pt",
      format: "letter",
    });

    const marginLeft = 40;
    let y = 50;

    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.text("Encounter Note", marginLeft, y);
    y += 25;

    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.text(
      `Patient: ${patient_name || "Unknown"}    DOB: ${dob || "—"}    MRN: ${
        mrn || "—"
      }`,
      marginLeft,
      y
    );
    y += 15;
    doc.text(`Encounter: ${encounter_datetime || "Not specified"}`, marginLeft, y);
    y += 20;

    const addSection = (title, text) => {
      doc.setFont("helvetica", "bold");
      doc.setFontSize(12);
      doc.text(title, marginLeft, y);
      y += 14;

      doc.setFont("helvetica", "normal");
      doc.setFontSize(10);

      const textLines = doc.splitTextToSize(text || "—", 520);
      textLines.forEach((line) => {
        if (y > 750) {
          doc.addPage();
          y = 50;
        }
        doc.text(line, marginLeft, y);
        y += 12;
      });

      y += 8;
    };

    addSection("Chief Complaint", chief_complaint);
    addSection("History of Present Illness", hpi);
    addSection("Assessment", assessment);
    addSection("Plan", plan);

    // ICD-10
    doc.setFont("helvetica", "bold");
    doc.setFontSize(12);
    if (y > 750) {
      doc.addPage();
      y = 50;
    }
    doc.text("ICD-10 Codes (Suggested)", marginLeft, y);
    y += 14;
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);

    if (!icd10_codes.length) {
      doc.text("None suggested.", marginLeft, y);
    } else {
      icd10_codes.forEach((c) => {
        if (y > 750) {
          doc.addPage();
          y = 50;
        }
        doc.text(`${c.code} — ${c.description}`, marginLeft, y);
        y += 12;
      });
    }

    doc.save(`health-record-${fileSafeName || "encounter"}.pdf`);
  };

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          mb: 3,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 2,
          flexWrap: "wrap",
        }}
      >
        <Typography variant="h4">Encounter Note</Typography>

        <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
          <Button variant="outlined" onClick={handleDownloadJson}>
            Download JSON
          </Button>
          <Button variant="outlined" onClick={handleDownloadPdf}>
            Download PDF
          </Button>
          <Button
            variant="contained"
            color="secondary"
            disabled
            title="Future: send directly into FHIR/EHR"
          >
            Send to EHR (coming soon)
          </Button>
        </Box>
      </Box>

      <Paper
        elevation={3}
        sx={{
          p: 4,
          borderRadius: 3,
          backgroundColor: "background.paper",
        }}
      >
        {/* Header info */}
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="text.secondary">
              Patient
            </Typography>
            <Typography variant="body1">
              {patient_name || "Unknown patient"}
            </Typography>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Typography variant="subtitle2" color="text.secondary">
              DOB
            </Typography>
            <Typography variant="body1">{dob || "—"}</Typography>
          </Grid>
          <Grid item xs={6} sm={3}>
            <Typography variant="subtitle2" color="text.secondary">
              MRN
            </Typography>
            <Typography variant="body1">{mrn || "—"}</Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="subtitle2" color="text.secondary">
              Encounter Date/Time
            </Typography>
            <Typography variant="body1">
              {encounter_datetime || "Not specified"}
            </Typography>
          </Grid>
        </Grid>

        <Divider sx={{ my: 2 }} />

        {/* Chief complaint */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Chief Complaint
          </Typography>
          <Typography variant="body1">
            {chief_complaint ||
              "Not captured. (Will be extracted from transcript.)"}
          </Typography>
        </Box>

        {/* HPI */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            History of Present Illness
          </Typography>
          <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
            {hpi || "Not available."}
          </Typography>
        </Box>

        {/* Assessment & Plan */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              Assessment
            </Typography>
            <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
              {assessment || "Pending physician review."}
            </Typography>
          </Grid>
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom>
              Plan
            </Typography>
            <Typography variant="body1" sx={{ whiteSpace: "pre-wrap" }}>
              {plan || "Pending physician review."}
            </Typography>
          </Grid>
        </Grid>

        {/* ICD-10 codes */}
        <Box sx={{ mb: 1 }}>
          <Typography variant="h6" gutterBottom>
            ICD-10 Codes (Suggested)
          </Typography>
          {icd10_codes.length === 0 ? (
            <Typography variant="body2" color="text.secondary">
              None suggested yet. Model can populate this from the transcript.
            </Typography>
          ) : (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1 }}>
              {icd10_codes.map((c, idx) => (
                <Chip
                  key={`${c.code}-${idx}`}
                  label={`${c.code} — ${c.description}`}
                  size="small"
                />
              ))}
            </Box>
          )}
        </Box>
      </Paper>
    </Container>
  );
};

export default HealthRecordPage;