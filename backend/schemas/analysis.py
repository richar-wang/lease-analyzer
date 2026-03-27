from enum import Enum

from pydantic import BaseModel


class Severity(str, Enum):
    red = "red"
    yellow = "yellow"
    green = "green"


class FlaggedClause(BaseModel):
    original_clause_text: str
    violation_type: str
    severity: Severity
    rta_section: str
    explanation: str


class AnalysisResponse(BaseModel):
    flagged_clauses: list[FlaggedClause]
    summary: str
    lease_text: str = ""
