import { useMemo, useState } from "react";
import type { AnalysisResponse, FlaggedClause, Severity } from "../types/analysis";
import SeverityBadge from "./SeverityBadge";

const highlightColors: Record<Severity, { bg: string; border: string }> = {
  red: { bg: "bg-red-50 border-red-300", border: "border-l-red-500" },
  yellow: { bg: "bg-amber-50 border-amber-300", border: "border-l-amber-500" },
  green: { bg: "bg-emerald-50 border-emerald-300", border: "border-l-emerald-500" },
};

interface TextSegment {
  text: string;
  clause: FlaggedClause | null;
}

function normalizeWhitespace(s: string): string {
  return s.replace(/\s+/g, " ").trim();
}

function buildSegments(
  leaseText: string,
  clauses: FlaggedClause[]
): TextSegment[] {
  const matches: { start: number; end: number; clause: FlaggedClause }[] = [];

  for (const clause of clauses) {
    let idx = leaseText.indexOf(clause.original_clause_text);

    if (idx === -1) {
      const normalizedClause = normalizeWhitespace(clause.original_clause_text);
      const normalizedLease = normalizeWhitespace(leaseText);
      const normalizedIdx = normalizedLease.indexOf(normalizedClause);

      if (normalizedIdx !== -1) {
        let origPos = 0;
        let normPos = 0;
        while (normPos < normalizedIdx && origPos < leaseText.length) {
          if (/\s/.test(leaseText[origPos])) {
            while (origPos < leaseText.length && /\s/.test(leaseText[origPos])) origPos++;
            normPos++;
          } else {
            origPos++;
            normPos++;
          }
        }
        const startPos = origPos;

        let matchLen = 0;
        let scanPos = startPos;
        const clauseNormLen = normalizedClause.length;
        while (matchLen < clauseNormLen && scanPos < leaseText.length) {
          if (/\s/.test(leaseText[scanPos])) {
            while (scanPos < leaseText.length && /\s/.test(leaseText[scanPos])) scanPos++;
            matchLen++;
          } else {
            scanPos++;
            matchLen++;
          }
        }

        matches.push({ start: startPos, end: scanPos, clause });
        continue;
      }
    }

    if (idx !== -1) {
      matches.push({ start: idx, end: idx + clause.original_clause_text.length, clause });
    }
  }

  matches.sort((a, b) => a.start - b.start);

  const filtered: typeof matches = [];
  let lastEnd = 0;
  for (const m of matches) {
    if (m.start >= lastEnd) {
      filtered.push(m);
      lastEnd = m.end;
    }
  }

  const segments: TextSegment[] = [];
  let pos = 0;
  for (const m of filtered) {
    if (m.start > pos) {
      segments.push({ text: leaseText.slice(pos, m.start), clause: null });
    }
    segments.push({ text: leaseText.slice(m.start, m.end), clause: m.clause });
    pos = m.end;
  }
  if (pos < leaseText.length) {
    segments.push({ text: leaseText.slice(pos), clause: null });
  }

  return segments;
}

/** Detect if a line looks like a section heading (e.g., "1. RENT PAYMENT", "RESIDENTIAL LEASE AGREEMENT") */
function isHeading(line: string): boolean {
  const trimmed = line.trim();
  if (!trimmed) return false;
  // Numbered section: "1. SOMETHING" or "10. SOMETHING"
  if (/^\d{1,2}\.\s+[A-Z]/.test(trimmed)) return true;
  // ALL CAPS line that's short enough to be a heading
  if (trimmed === trimmed.toUpperCase() && trimmed.length > 3 && trimmed.length < 80 && /[A-Z]/.test(trimmed)) return true;
  return false;
}

/** Detect sub-items like (a), (b), (1), (2) */
function isSubItem(line: string): boolean {
  return /^\s*\([a-z0-9]\)/.test(line);
}

function ClausePopover({ clause, onClose }: { clause: FlaggedClause; onClose: () => void }) {
  return (
    <div className="my-3 p-4 rounded-lg border border-gray-200 bg-white shadow-lg text-sm">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-2">
          <SeverityBadge severity={clause.severity} />
          <span className="font-semibold text-gray-800">{clause.violation_type}</span>
        </div>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600 text-lg leading-none px-1"
        >
          &times;
        </button>
      </div>
      <div className="space-y-2">
        <p>
          <span className="font-medium text-gray-700">RTA Reference:</span>{" "}
          <span className="text-blue-700 font-medium">{clause.rta_section}</span>
        </p>
        <p className="text-gray-600 leading-relaxed">{clause.explanation}</p>
        {clause.standard_lease_comparison && (
          <div className="mt-2 rounded-lg bg-blue-50 border border-blue-200 p-3">
            <p className="text-xs font-semibold text-blue-800 mb-1">
              Ontario Standard Lease (Form 2229E)
            </p>
            <p className="text-blue-700 text-xs leading-relaxed">
              {clause.standard_lease_comparison}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/** Format a plain text segment into structured paragraphs */
function FormattedText({ text }: { text: string }) {
  const lines = text.split("\n");
  const elements: React.ReactNode[] = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) {
      // Skip excessive blank lines
      continue;
    }

    if (isHeading(trimmed)) {
      elements.push(
        <h3 key={i} className="font-bold text-gray-900 text-base mt-6 mb-2 tracking-tight">
          {trimmed}
        </h3>
      );
    } else if (isSubItem(trimmed)) {
      elements.push(
        <p key={i} className="pl-6 text-gray-700 leading-relaxed mb-1">
          {trimmed}
        </p>
      );
    } else {
      elements.push(
        <p key={i} className="text-gray-700 leading-relaxed mb-2">
          {trimmed}
        </p>
      );
    }
  }

  return <>{elements}</>;
}

/** Format highlighted clause text */
function FormattedClauseText({ text }: { text: string }) {
  const lines = text.split("\n");
  const elements: React.ReactNode[] = [];

  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    if (!trimmed) continue;

    if (isSubItem(trimmed)) {
      elements.push(
        <p key={i} className="pl-6 leading-relaxed mb-1">{trimmed}</p>
      );
    } else {
      elements.push(
        <p key={i} className="leading-relaxed mb-1">{trimmed}</p>
      );
    }
  }

  return <>{elements}</>;
}

export default function DocumentView({ data }: { data: AnalysisResponse }) {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);

  const segments = useMemo(
    () => buildSegments(data.lease_text, data.flagged_clauses),
    [data.lease_text, data.flagged_clauses]
  );

  let highlightIndex = -1;

  return (
    <div className="rounded-lg border border-gray-200 bg-white shadow-sm overflow-hidden">
      {/* Header bar */}
      <div className="flex items-center gap-3 px-8 py-3 bg-gray-50 border-b border-gray-200">
        <span className="text-xs text-gray-500">Click highlighted sections to see details</span>
        <div className="flex gap-3 ml-auto">
          <span className="flex items-center gap-1.5 text-xs text-gray-600">
            <span className="inline-block w-3 h-3 rounded-sm bg-red-100 border border-red-300" />
            Illegal
          </span>
          <span className="flex items-center gap-1.5 text-xs text-gray-600">
            <span className="inline-block w-3 h-3 rounded-sm bg-amber-100 border border-amber-300" />
            Problematic
          </span>
          <span className="flex items-center gap-1.5 text-xs text-gray-600">
            <span className="inline-block w-3 h-3 rounded-sm bg-emerald-100 border border-emerald-300" />
            Notable
          </span>
        </div>
      </div>

      {/* Document body */}
      <div className="px-12 py-8 max-w-none" style={{ fontFamily: "'Georgia', 'Times New Roman', serif" }}>
        {segments.map((seg, i) => {
          if (!seg.clause) {
            return <FormattedText key={i} text={seg.text} />;
          }

          highlightIndex++;
          const thisIdx = highlightIndex;
          const isExpanded = expandedIdx === thisIdx;
          const colors = highlightColors[seg.clause.severity];

          return (
            <div key={i}>
              <div
                className={`rounded-md border ${colors.bg} border-l-4 ${colors.border} px-4 py-3 my-3 cursor-pointer transition-all hover:shadow-sm ${
                  isExpanded ? "ring-2 ring-blue-300" : ""
                }`}
                onClick={() => setExpandedIdx(isExpanded ? null : thisIdx)}
              >
                <FormattedClauseText text={seg.text} />
              </div>
              {isExpanded && (
                <ClausePopover
                  clause={seg.clause}
                  onClose={() => setExpandedIdx(null)}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
