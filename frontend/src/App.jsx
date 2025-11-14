// frontend/src/App.jsx
import React from "react";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { Box } from "@mui/material";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import theme from "./theme/theme";
import NavBar from "./components/NavBar";
import Main from "./components/Main";
import Footer from "./components/Footer";
import HealthRecordPage from "./components/HealthRecordPage";
import { RecordProvider } from "./components/RecordContext";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <RecordProvider>
          <Box
            sx={{
              minHeight: "100vh",
              display: "flex",
              flexDirection: "column",
              backgroundColor: "background.default",
            }}
          >
            <NavBar />
            <Box component="main" sx={{ flexGrow: 1, py: 4 }}>
              <Routes>
                <Route path="/" element={<Main />} />
                <Route path="/record" element={<HealthRecordPage />} />
              </Routes>
            </Box>
            <Footer />
          </Box>
        </RecordProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;