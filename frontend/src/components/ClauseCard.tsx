import type { FlaggedClause } from "../types/analysis";
import SeverityBadge from "./SeverityBadge";

const borderColors = {
  red: "border-l-red-500",
  yellow: "border-l-yellow-500",
  green: "border-l-green-500",
};

export default function ClauseCard({ clause }: { clause: FlaggedClause }) {
  return (
    <div
      className={`rounded-lg border border-gray-200 border-l-4 ${borderColors[clause.severity]} bg-white p-5 shadow-sm`}
    >
      <div className="flex items-center gap-3 mb-3">
        <SeverityBadge severity={clause.severity} />
        <span className="text-sm font-semibold text-gray-700">
          {clause.violation_type}
        </span>
      </div>

      <blockquote className="border-l-2 border-gray-300 pl-4 py-2 mb-4 text-sm text-gray-600 italic bg-gray-50 rounded-r">
        "{clause.original_clause_text}"
      </blockquote>

      <div className="space-y-2 text-sm">
        <p>
          <span className="font-medium text-gray-700">RTA Reference:</span>{" "}
          <span className="text-blue-700">{clause.rta_section}</span>
        </p>
        <p className="text-gray-600 leading-relaxed">{clause.explanation}</p>
      </div>
    </div>
  );
}
