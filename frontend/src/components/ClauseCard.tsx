import type { FlaggedClause } from "../types/analysis";
import SeverityBadge from "./SeverityBadge";

const borderColors = {
  red: "border-l-red-500",
  yellow: "border-l-yellow-500",
  green: "border-l-green-500",
};

export default function ClauseCard({ clause, isHebrew }: { clause: FlaggedClause; isHebrew: boolean }) {
  const cardBg = isHebrew ? "bg-[#f7f9fd] border-[#c5d4ec]" : "bg-white border-gray-200";
  const stdLeaseBg = isHebrew ? "bg-[#e8eef8] border-[#0038A8]/20" : "bg-blue-50 border-blue-200";
  const stdLeaseTitle = isHebrew ? "text-[#0038A8]" : "text-blue-800";
  const stdLeaseText = isHebrew ? "text-[#0038A8]/80" : "text-blue-700";

  return (
    <div
      className={`rounded-lg border border-l-4 ${borderColors[clause.severity]} ${cardBg} p-5 shadow-sm`}
    >
      <div className="flex items-center gap-3 mb-3">
        <SeverityBadge severity={clause.severity} />
        <span className="text-sm font-semibold text-gray-700">
          {clause.violation_type}
        </span>
      </div>

      <blockquote className="border-l-2 border-gray-300 pl-4 py-2 mb-4 text-sm text-gray-600 italic bg-gray-50 rounded-r" dir="ltr">
        "{clause.original_clause_text}"
      </blockquote>

      <div className="space-y-2 text-sm">
        <p>
          <span className="font-medium text-gray-700">{isHebrew ? "הפניה לחוק:" : "RTA Reference:"}</span>{" "}
          <span className={isHebrew ? "text-[#0038A8] font-medium" : "text-blue-700"}>{clause.rta_section}</span>
        </p>
        <p className="text-gray-600 leading-relaxed">{clause.explanation}</p>

        {clause.standard_lease_comparison && (
          <div className={`mt-3 rounded-lg border p-3 ${stdLeaseBg}`}>
            <p className={`text-xs font-semibold mb-1 ${stdLeaseTitle}`}>
              {isHebrew ? "חוזה שכירות סטנדרטי של אונטריו (טופס 2229E)" : "Ontario Standard Lease (Form 2229E)"}
            </p>
            <p className={`text-xs leading-relaxed ${stdLeaseText}`}>
              {clause.standard_lease_comparison}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
