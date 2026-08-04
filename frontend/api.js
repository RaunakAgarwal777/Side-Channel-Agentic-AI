/**
 * api.js
 * Talks to the local backend (FastAPI). Swap MOCK_MODE off once
 * backend/api.py exposes a real /analyze endpoint.
 */

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
export const MOCK_MODE = import.meta.env.VITE_MOCK_MODE !== "false";

export async function runAnalysis(query) {
  if (MOCK_MODE) return null; // dashboard.jsx handles the mock trace itself

  const res = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error(`Analysis failed: ${res.status}`);
  return res.json(); // { trace: [...], risk_score, verdict }
}

export async function getHistory() {
  if (MOCK_MODE) return [];
  const res = await fetch(`${BASE_URL}/history`);
  if (!res.ok) throw new Error("Failed to load history");
  return res.json();
}
