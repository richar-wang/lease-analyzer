import type { AnalysisResponse } from "../types/analysis";

export type StatusCallback = (message: string) => void;

export interface Language {
  code: string;
  name: string;
}

function getHeaders(): Record<string, string> {
  const headers: Record<string, string> = {};
  const code = sessionStorage.getItem("access_code");
  if (code) headers["X-Access-Code"] = code;
  const lang = sessionStorage.getItem("language");
  if (lang) headers["X-Language"] = lang;
  return headers;
}

function parseSSE(
  reader: ReadableStreamDefaultReader<Uint8Array>,
  onStatus: StatusCallback
): Promise<AnalysisResponse> {
  return new Promise((resolve, reject) => {
    const decoder = new TextDecoder();
    let buffer = "";
    let settled = false;

    function processEvents() {
      const parts = buffer.split("\n\n");
      buffer = parts.pop() || "";

      for (const part of parts) {
        if (settled) return;

        let eventType = "";
        let eventData = "";

        for (const line of part.split("\n")) {
          if (line.startsWith("event: ")) {
            eventType = line.slice(7).trim();
          } else if (line.startsWith("data: ")) {
            eventData += line.slice(6);
          }
        }

        if (!eventType || !eventData) continue;

        try {
          const data = JSON.parse(eventData);
          if (eventType === "status") {
            onStatus(data.message);
          } else if (eventType === "result") {
            settled = true;
            resolve(data as AnalysisResponse);
            return;
          } else if (eventType === "error") {
            settled = true;
            reject(new Error(data.message));
            return;
          }
        } catch {
          // JSON parse failed — likely incomplete data, skip
        }
      }
    }

    function read() {
      if (settled) return;

      reader.read().then(({ done, value }) => {
        if (settled) return;

        if (done) {
          buffer += "\n\n";
          processEvents();
          if (!settled) {
            reject(new Error("Connection closed before analysis completed."));
          }
          return;
        }

        buffer += decoder.decode(value, { stream: true });
        processEvents();

        if (!settled) read();
      }).catch((err) => {
        if (!settled) {
          settled = true;
          reject(err);
        }
      });
    }

    read();
  });
}

export async function checkConfig(): Promise<{ requires_code: boolean; access_hint: string }> {
  const res = await fetch("/api/config");
  return res.json();
}

export async function fetchLanguages(): Promise<Language[]> {
  const res = await fetch("/api/languages");
  return res.json();
}

export async function analyzeLease(
  file: File,
  onStatus: StatusCallback
): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/api/analyze", {
    method: "POST",
    body: formData,
    headers: getHeaders(),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Analysis failed" }));
    throw new Error(err.detail || "Analysis failed");
  }

  return parseSSE(res.body!.getReader(), onStatus);
}

export async function getDemoAnalysis(
  onStatus: StatusCallback
): Promise<AnalysisResponse> {
  const res = await fetch("/api/demo", {
    headers: getHeaders(),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Demo analysis failed" }));
    throw new Error(err.detail || "Demo analysis failed");
  }

  return parseSSE(res.body!.getReader(), onStatus);
}
