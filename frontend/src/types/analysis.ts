export type Severity = "red" | "yellow" | "green";

export interface FlaggedClause {
  original_clause_text: string;
  violation_type: string;
  severity: Severity;
  rta_section: string;
  explanation: string;
  standard_lease_comparison: string;
}

export interface AnalysisResponse {
  flagged_clauses: FlaggedClause[];
  summary: string;
  lease_text: string;
}
