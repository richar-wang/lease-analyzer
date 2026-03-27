import { useEffect, useState } from "react";
import type { AnalysisResponse } from "./types/analysis";
import { analyzeLease, checkConfig, getDemoAnalysis } from "./services/api";
import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import AnalysisResults from "./components/AnalysisResults";
import ErrorMessage from "./components/ErrorMessage";

type AppState =
  | { status: "loading" }
  | { status: "auth"; hint: string }
  | { status: "idle" }
  | { status: "analyzing"; stepMessage: string }
  | { status: "success"; data: AnalysisResponse }
  | { status: "error"; message: string };

const steps = [
  { key: "extracting", label: "Extract text" },
  { key: "rendering", label: "Render pages" },
  { key: "analyzing", label: "Analyze with Claude" },
  { key: "complete", label: "Done" },
];

function StepIndicator({ currentStep }: { currentStep: string }) {
  const activeIndex = steps.findIndex((s) => s.key === currentStep);

  return (
    <div className="flex items-center justify-center gap-2 mb-6">
      {steps
        .filter((s) => s.key !== "rendering" || currentStep === "rendering")
        .map((step, i) => {
          const stepIndex = steps.indexOf(step);
          const isActive = stepIndex === activeIndex;
          const isDone = stepIndex < activeIndex;

          return (
            <div key={step.key} className="flex items-center gap-2">
              {i > 0 && (
                <div
                  className={`w-8 h-0.5 ${isDone ? "bg-blue-600" : "bg-gray-300"}`}
                />
              )}
              <div className="flex items-center gap-1.5">
                <div
                  className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
                    isDone
                      ? "bg-blue-600 text-white"
                      : isActive
                        ? "bg-blue-100 text-blue-700 ring-2 ring-blue-600"
                        : "bg-gray-200 text-gray-500"
                  }`}
                >
                  {isDone ? "\u2713" : i + 1}
                </div>
                <span
                  className={`text-xs ${isActive ? "text-blue-700 font-medium" : "text-gray-500"}`}
                >
                  {step.label}
                </span>
              </div>
            </div>
          );
        })}
    </div>
  );
}

function AccessCodeScreen({ hint, onSubmit }: { hint: string; onSubmit: () => void }) {
  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!code.trim()) {
      setError("Please enter your answer.");
      return;
    }
    sessionStorage.setItem("access_code", code.trim());
    setError("");
    onSubmit();
  };

  return (
    <div className="text-center py-16">
      <h2 className="text-lg font-semibold text-gray-900 mb-2">
        Access Code Required
      </h2>
      {hint ? (
        <p className="text-sm text-gray-600 mb-6 italic">"{hint}"</p>
      ) : (
        <p className="text-sm text-gray-500 mb-6">
          Enter the access code to use the lease analyzer.
        </p>
      )}
      <form onSubmit={handleSubmit} className="inline-flex flex-col gap-3 w-72">
        <input
          type="text"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Your answer (one word)"
          className="rounded-lg border border-gray-300 px-4 py-2.5 text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          autoFocus
        />
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button
          type="submit"
          className="rounded-lg bg-gray-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-gray-800 transition-colors"
        >
          Continue
        </button>
      </form>
    </div>
  );
}

function App() {
  const [state, setState] = useState<AppState>({ status: "loading" });

  useEffect(() => {
    checkConfig().then((config) => {
      if (config.requires_code && !sessionStorage.getItem("access_code")) {
        setState({ status: "auth", hint: config.access_hint || "" });
      } else {
        setState({ status: "idle" });
      }
    }).catch(() => {
      setState({ status: "idle" });
    });
  }, []);

  const onStatus = (message: string) => {
    setState((prev) =>
      prev.status === "analyzing" ? { ...prev, stepMessage: message } : prev
    );
  };

  const getStepKey = (message: string) => {
    if (message.includes("Extracting")) return "extracting";
    if (message.includes("Rendering") || message.includes("Scanned")) return "rendering";
    if (message.includes("Analyzing")) return "analyzing";
    if (message.includes("complete")) return "complete";
    return "extracting";
  };

  const handleFile = async (file: File) => {
    setState({ status: "analyzing", stepMessage: "Starting..." });
    try {
      const data = await analyzeLease(file, onStatus);
      setState({ status: "success", data });
    } catch (e) {
      const msg = e instanceof Error ? e.message : "An unexpected error occurred";
      if (msg.includes("access code")) {
        sessionStorage.removeItem("access_code");
        setState({ status: "auth", hint: "" });
      } else {
        setState({ status: "error", message: msg });
      }
    }
  };

  const handleDemo = async () => {
    setState({ status: "analyzing", stepMessage: "Starting..." });
    try {
      const data = await getDemoAnalysis(onStatus);
      setState({ status: "success", data });
    } catch (e) {
      const msg = e instanceof Error ? e.message : "An unexpected error occurred";
      if (msg.includes("access code")) {
        sessionStorage.removeItem("access_code");
        setState({ status: "auth", hint: "" });
      } else {
        setState({ status: "error", message: msg });
      }
    }
  };

  const reset = () => setState({ status: "idle" });

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="mx-auto max-w-4xl px-6 py-8">
        {state.status === "loading" && (
          <div className="text-center py-16 text-gray-400">Loading...</div>
        )}

        {state.status === "auth" && (
          <AccessCodeScreen hint={state.hint} onSubmit={() => setState({ status: "idle" })} />
        )}

        {state.status === "idle" && (
          <UploadSection
            onFileSelected={handleFile}
            onDemoClick={handleDemo}
            isLoading={false}
          />
        )}

        {state.status === "analyzing" && (
          <div className="text-center py-16">
            <StepIndicator currentStep={getStepKey(state.stepMessage)} />
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600 mb-4" />
            <p className="text-gray-600 font-medium">{state.stepMessage}</p>
          </div>
        )}

        {state.status === "error" && (
          <ErrorMessage message={state.message} onRetry={reset} />
        )}

        {state.status === "success" && (
          <AnalysisResults data={state.data} onReset={reset} />
        )}
      </main>
    </div>
  );
}

export default App;
