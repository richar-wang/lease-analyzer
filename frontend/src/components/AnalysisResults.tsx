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
  isHebrew,
}: {
  data: AnalysisResponse;
  onReset: () => void;
  isHebrew: boolean;
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

  const activeBtn = isHebrew ? "bg-[#0038A8] text-white" : "bg-gray-900 text-white";
  const resetBtn = isHebrew
    ? "bg-[#0038A8] text-white hover:bg-[#002d8a]"
    : "bg-gray-900 text-white hover:bg-gray-800";

  return (
    <div className="space-y-6">
      <Disclaimer isHebrew={isHebrew} />

      <div className={`rounded-lg border p-5 shadow-sm ${isHebrew ? "bg-[#f7f9fd] border-[#c5d4ec]" : "bg-white border-gray-200"}`}>
        <h2 className="text-lg font-semibold text-gray-900 mb-2">
          {isHebrew ? "סיכום" : "Summary"}
        </h2>
        <p className="text-sm text-gray-600 leading-relaxed">{data.summary}</p>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex gap-4">
          <div className="flex items-center gap-2 text-sm">
            <span className="inline-block w-3 h-3 rounded-full bg-red-500" />
            <span className="text-gray-700">{counts.red} {isHebrew ? "לא חוקי" : "Illegal"}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="inline-block w-3 h-3 rounded-full bg-yellow-500" />
            <span className="text-gray-700">{counts.yellow} {isHebrew ? "חשוד" : "Suspect"}</span>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span className="inline-block w-3 h-3 rounded-full bg-green-500" />
            <span className="text-gray-700">{counts.green} {isHebrew ? "ראוי לציון" : "Notable"}</span>
          </div>
        </div>

        {hasLeaseText && (
          <div className={`flex rounded-lg border overflow-hidden text-sm ${isHebrew ? "border-[#0038A8]/30" : "border-gray-300"}`}>
            <button
              onClick={() => setView("cards")}
              className={`px-4 py-1.5 font-medium transition-colors ${
                view === "cards"
                  ? activeBtn
                  : "bg-white text-gray-600 hover:bg-gray-50"
              }`}
            >
              {isHebrew ? "תצוגת כרטיסים" : "Card View"}
            </button>
            <button
              onClick={() => setView("document")}
              className={`px-4 py-1.5 font-medium transition-colors ${
                view === "document"
                  ? activeBtn
                  : "bg-white text-gray-600 hover:bg-gray-50"
              }`}
            >
              {isHebrew ? "תצוגת מסמך" : "Document View"}
            </button>
          </div>
        )}
      </div>

      {sorted.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          {isHebrew
            ? "לא נמצאו סעיפים בעייתיים. החוזה נראה תקין."
            : "No problematic clauses found. This lease appears compliant with the RTA."}
        </div>
      ) : view === "cards" ? (
        <div className="space-y-4">
          {sorted.map((clause, i) => (
            <ClauseCard key={i} clause={clause} isHebrew={isHebrew} />
          ))}
        </div>
      ) : (
        <DocumentView data={data} />
      )}

      <div className="text-center pt-4">
        <button
          onClick={onReset}
          className={`rounded-lg px-6 py-2.5 text-sm font-medium transition-colors ${resetBtn}`}
        >
          {isHebrew ? "נתח חוזה נוסף" : "Analyze Another Lease"}
        </button>
      </div>
    </div>
  );
}
