import { useState } from "react";
import type { AnalysisResponse } from "./types/analysis";
import { analyzeLease, getDemoAnalysis } from "./services/api";
import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import AnalysisResults from "./components/AnalysisResults";
import ErrorMessage from "./components/ErrorMessage";

type AppState =
  | { status: "idle" }
  | { status: "analyzing" }
  | { status: "success"; data: AnalysisResponse }
  | { status: "error"; message: string };

function App() {
  const [state, setState] = useState<AppState>({ status: "idle" });

  const handleFile = async (file: File) => {
    setState({ status: "analyzing" });
    try {
      const data = await analyzeLease(file);
      setState({ status: "success", data });
    } catch (e) {
      setState({
        status: "error",
        message: e instanceof Error ? e.message : "An unexpected error occurred",
      });
    }
  };

  const handleDemo = async () => {
    setState({ status: "analyzing" });
    try {
      const data = await getDemoAnalysis();
      setState({ status: "success", data });
    } catch (e) {
      setState({
        status: "error",
        message: e instanceof Error ? e.message : "An unexpected error occurred",
      });
    }
  };

  const reset = () => setState({ status: "idle" });

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="mx-auto max-w-4xl px-6 py-8">
        {state.status === "idle" && (
          <UploadSection
            onFileSelected={handleFile}
            onDemoClick={handleDemo}
            isLoading={false}
          />
        )}

        {state.status === "analyzing" && (
          <div className="text-center py-16">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600 mb-4" />
            <p className="text-gray-600 font-medium">
              Analyzing your lease against the RTA...
            </p>
            <p className="text-sm text-gray-400 mt-1">
              This typically takes 15-30 seconds
            </p>
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
