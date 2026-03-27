import { useMemo, useState } from "react";
import type { AnalysisResponse, FlaggedClause, Severity } from "../types/analysis";
import SeverityBadge from "./SeverityBadge";

const highlightColors: Record<Severity, { bg: string; border: string }> = {
  red: { bg: "bg-red-100", border: "border-red-400" },
  yellow: { bg: "bg-yellow-100", border: "border-yellow-400" },
  green: { bg: "bg-green-100", border: "border-green-400" },
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
  // Find all clause positions in the text
  const matches: { start: number; end: number; clause: FlaggedClause }[] = [];

  for (const clause of clauses) {
    // Try exact match first
    let idx = leaseText.indexOf(clause.original_clause_text);

    // If not found, try normalized whitespace matching
    if (idx === -1) {
      const normalizedClause = normalizeWhitespace(clause.original_clause_text);
      const normalizedLease = normalizeWhitespace(leaseText);
      const normalizedIdx = normalizedLease.indexOf(normalizedClause);

      if (normalizedIdx !== -1) {
        // Map back to original text position by counting chars
        let origPos = 0;
        let normPos = 0;
        // Find start
        while (normPos < normalizedIdx && origPos < leaseText.length) {
          if (/\s/.test(leaseText[origPos])) {
            // Consume all whitespace in original
            while (origPos < leaseText.length && /\s/.test(leaseText[origPos])) origPos++;
            normPos++; // single space in normalized
          } else {
            origPos++;
            normPos++;
          }
        }
        const startPos = origPos;

        // Find end
        let matchLen = 0;
        let scanPos = startPos;
        const clauseNormLen = normalizedClause.length;
        while (matchLen < clauseNormLen && scanPos < leaseText.length) {
          if (/\s/.test(leaseText[scanPos])) {
            while (scanPos < leaseText.length && /\s/.test(leaseText[scanPos])) scanPos++;
            matchLen++; // single space
          } else {
            scanPos++;
            matchLen++;
          }
        }

        idx = startPos;
        matches.push({ start: startPos, end: scanPos, clause });
        continue;
      }
    }

    if (idx !== -1) {
      matches.push({
        start: idx,
        end: idx + clause.original_clause_text.length,
        clause,
      });
    }
  }

  // Sort by position
  matches.sort((a, b) => a.start - b.start);

  // Remove overlaps (keep earlier match)
  const filtered: typeof matches = [];
  let lastEnd = 0;
  for (const m of matches) {
    if (m.start >= lastEnd) {
      filtered.push(m);
      lastEnd = m.end;
    }
  }

  // Build segments
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

function ClausePopover({ clause }: { clause: FlaggedClause }) {
  return (
    <div className="mt-2 mb-3 ml-2 p-4 rounded-lg border border-gray-200 bg-white shadow-lg text-sm animate-in">
      <div className="flex items-center gap-2 mb-2">
        <SeverityBadge severity={clause.severity} />
        <span className="font-semibold text-gray-700">
          {clause.violation_type}
        </span>
      </div>
      <p className="mb-2">
        <span className="font-medium text-gray-700">RTA Reference:</span>{" "}
        <span className="text-blue-700">{clause.rta_section}</span>
      </p>
      <p className="text-gray-600 leading-relaxed">{clause.explanation}</p>
    </div>
  );
}

export default function DocumentView({ data }: { data: AnalysisResponse }) {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);

  const segments = useMemo(
    () => buildSegments(data.lease_text, data.flagged_clauses),
    [data.lease_text, data.flagged_clauses]
  );

  // Track which highlight we're on for click toggling
  let highlightIndex = -1;

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <div className="flex items-center gap-3 mb-4 pb-3 border-b border-gray-100">
        <span className="text-xs text-gray-500">Click highlighted text to see details</span>
        <div className="flex gap-3 ml-auto">
          <span className="flex items-center gap-1 text-xs">
            <span className="inline-block w-3 h-2 rounded-sm bg-red-200 border border-red-400" />
            Illegal
          </span>
          <span className="flex items-center gap-1 text-xs">
            <span className="inline-block w-3 h-2 rounded-sm bg-yellow-200 border border-yellow-400" />
            Problematic
          </span>
          <span className="flex items-center gap-1 text-xs">
            <span className="inline-block w-3 h-2 rounded-sm bg-green-200 border border-green-400" />
            Notable
          </span>
        </div>
      </div>
      <div className="font-mono text-sm leading-relaxed whitespace-pre-wrap text-gray-800">
        {segments.map((seg, i) => {
          if (!seg.clause) {
            return <span key={i}>{seg.text}</span>;
          }

          highlightIndex++;
          const thisIdx = highlightIndex;
          const isExpanded = expandedIdx === thisIdx;
          const colors = highlightColors[seg.clause.severity];

          return (
            <span key={i}>
              <mark
                className={`${colors.bg} border-b-2 ${colors.border} cursor-pointer rounded-sm px-0.5 transition-all hover:opacity-80 ${
                  isExpanded ? "ring-2 ring-blue-400" : ""
                }`}
                onClick={() => setExpandedIdx(isExpanded ? null : thisIdx)}
              >
                {seg.text}
              </mark>
              {isExpanded && <ClausePopover clause={seg.clause} />}
            </span>
          );
        })}
      </div>
    </div>
  );
}
