export type Severity = "red" | "yellow" | "green";

export interface FlaggedClause {
  original_clause_text: string;
  violation_type: string;
  severity: Severity;
  rta_section: string;
  explanation: string;
}

export interface AnalysisResponse {
  flagged_clauses: FlaggedClause[];
  summary: string;
}
