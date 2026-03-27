import { useState } from "react";
import type { AnalysisResponse, Severity } from "../types/analysis";
import Disclaimer from "./Disclaimer";
import ClauseCard from "./ClauseCard";
import DocumentView from "./DocumentView";

const severityOrder: Record<Severity, number> = { red: 0, yellow: 1, green: 2 };

type ViewMode = "cards" | "document";

export default function AnalysisResults({
  data,
  onReset,
}: {
  data: AnalysisResponse;
  onReset: () => void;
}) {
  const [view, setView] = useState<ViewMode>("cards");

  const sorted = [...data.flagged_clauses].sort(
    (a, b) => severityOrder[a.severity] - severityOrder[b.severity]
  );

  const counts = {
    red: sorted.filter((c) => c.severity === "red").length,
    yellow: sorted.filter((c) => c.severity === "yellow").length,
    green: sorted.filter((c) => c.severity === "green").length,
  };

  const hasLeaseText = data.lease_text && data.lease_text.trim().length > 0;

  return (
    <div className="space-y-6">
      <Disclaimer />

      <div className="rounded-lg bg-white border border-gray-200 p-5 shadow-sm">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Summary</h2>
        <p className="text-sm text-gray-600 leading-relaxed">{data.summary}</p>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex gap-4">
          <div className="flex items-center gap-2 text-sm">
            <span className="inline-block w-3 h-3 rounded-full bg-red-500" />
            <span className="text-gray-700">{counts.red} Illegal</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="inline-block w-3 h-3 rounded-full bg-yellow-500" />
            <span className="text-gray-700">{counts.yellow} Problematic</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="inline-block w-3 h-3 rounded-full bg-green-500" />
            <span className="text-gray-700">{counts.green} Notable</span>
          </div>
        </div>

        {hasLeaseText && (
          <div className="flex rounded-lg border border-gray-300 overflow-hidden text-sm">
            <button
              onClick={() => setView("cards")}
              className={`px-4 py-1.5 font-medium transition-colors ${
                view === "cards"
                  ? "bg-gray-900 text-white"
                  : "bg-white text-gray-600 hover:bg-gray-50"
              }`}
            >
              Card View
            </button>
            <button
              onClick={() => setView("document")}
              className={`px-4 py-1.5 font-medium transition-colors ${
                view === "document"
                  ? "bg-gray-900 text-white"
                  : "bg-white text-gray-600 hover:bg-gray-50"
              }`}
            >
              Document View
            </button>
          </div>
        )}
      </div>

      {sorted.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No problematic clauses found. This lease appears compliant with the
          RTA.
        </div>
      ) : view === "cards" ? (
        <div className="space-y-4">
          {sorted.map((clause, i) => (
            <ClauseCard key={i} clause={clause} />
          ))}
        </div>
      ) : (
        <DocumentView data={data} />
      )}

      <div className="text-center pt-4">
        <button
          onClick={onReset}
          className="rounded-lg bg-gray-900 px-6 py-2.5 text-sm font-medium text-white hover:bg-gray-800 transition-colors"
        >
          Analyze Another Lease
        </button>
      </div>
    </div>
  );
}
