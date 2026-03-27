import type { AnalysisResponse } from "../types/analysis";

export type StatusCallback = (message: string) => void;

function getHeaders(): Record<string, string> {
  const code = sessionStorage.getItem("access_code");
  return code ? { "X-Access-Code": code } : {};
}

function parseSSE(
  reader: ReadableStreamDefaultReader<Uint8Array>,
  onStatus: StatusCallback
): Promise<AnalysisResponse> {
  return new Promise((resolve, reject) => {
    const decoder = new TextDecoder();
    let buffer = "";

    function read() {
      reader.read().then(({ done, value }) => {
        if (done) {
          reject(new Error("Connection closed before analysis completed."));
          return;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        let currentEvent = "";
        for (const line of lines) {
          if (line.startsWith("event: ")) {
            currentEvent = line.slice(7).trim();
          } else if (line.startsWith("data: ")) {
            const data = JSON.parse(line.slice(6));
            if (currentEvent === "status") {
              onStatus(data.message);
            } else if (currentEvent === "result") {
              resolve(data as AnalysisResponse);
              return;
            } else if (currentEvent === "error") {
              reject(new Error(data.message));
              return;
            }
          }
        }

        read();
      });
    }

    read();
  });
}

export async function checkConfig(): Promise<{ requires_code: boolean }> {
  const res = await fetch("/api/config");
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
