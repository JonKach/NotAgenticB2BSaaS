// frontend/src/components/RecordContext.jsx
import React, { createContext, useContext, useState, useCallback } from "react";

const RecordContext = createContext(null);

export const RecordProvider = ({ children }) => {
  const [record, setRecord] = useState(null);
  const [transcript, setTranscript] = useState("");
  const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  const generateRecord = useCallback(
    async (transcriptText) => {
      if (!transcriptText) return null;
      try {
        const res = await fetch(`${API_BASE}/api/clinical/health-record`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ transcript: transcriptText }),
        });
        if (!res.ok) throw new Error(`generateRecord failed: ${res.status}`);
        const data = await res.json();
        setRecord(data.record || null);
        return data.record || null;
      } catch (err) {
        console.error("generateRecord error:", err);
        throw err;
      }
    },
    [API_BASE]
  );

  return (
    <RecordContext.Provider
      value={{ record, setRecord, transcript, setTranscript, generateRecord }}
    >
      {children}
    </RecordContext.Provider>
  );
};

export const useRecord = () => {
  const ctx = useContext(RecordContext);
  if (!ctx) {
    throw new Error("useRecord must be used inside RecordProvider");
  }
  return ctx;
};