import type { AnalysisResponse } from "../types/analysis";

export async function analyzeLease(file: File): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/api/analyze", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Analysis failed" }));
    throw new Error(err.detail || "Analysis failed");
  }

  return res.json();
}

export async function getDemoAnalysis(): Promise<AnalysisResponse> {
  const res = await fetch("/api/demo");

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Demo analysis failed" }));
    throw new Error(err.detail || "Demo analysis failed");
  }

  return res.json();
}
