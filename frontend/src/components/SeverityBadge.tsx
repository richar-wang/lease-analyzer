import type { Severity } from "../types/analysis";

const config: Record<Severity, { bg: string; text: string; label: string }> = {
  red: { bg: "bg-red-100", text: "text-red-800", label: "Illegal / Unenforceable" },
  yellow: { bg: "bg-yellow-100", text: "text-yellow-800", label: "Potentially Problematic" },
  green: { bg: "bg-green-100", text: "text-green-800", label: "Worth Noting" },
};

export default function SeverityBadge({ severity }: { severity: Severity }) {
  const c = config[severity];
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${c.bg} ${c.text}`}
    >
      {c.label}
    </span>
  );
}
