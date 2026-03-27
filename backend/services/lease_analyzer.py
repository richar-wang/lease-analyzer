import json

import anthropic

from config import settings
from rta.prompt_builder import build_system_prompt, build_user_prompt
from schemas.analysis import AnalysisResponse

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


ANALYSIS_TOOL = {
    "name": "report_lease_analysis",
    "description": "Report the results of the lease analysis as structured data.",
    "input_schema": {
        "type": "object",
        "properties": {
            "flagged_clauses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "original_clause_text": {
                            "type": "string",
                            "description": "The exact text of the clause from the lease",
                        },
                        "violation_type": {
                            "type": "string",
                            "description": "Category of the violation (e.g., 'Illegal Deposit', 'No-Pet Clause', 'Unauthorized Entry')",
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["red", "yellow", "green"],
                        },
                        "rta_section": {
                            "type": "string",
                            "description": "The specific RTA section(s) this clause violates",
                        },
                        "explanation": {
                            "type": "string",
                            "description": "Plain-language explanation of why this clause is problematic and what the tenant's rights actually are",
                        },
                    },
                    "required": [
                        "original_clause_text",
                        "violation_type",
                        "severity",
                        "rta_section",
                        "explanation",
                    ],
                },
            },
            "summary": {
                "type": "string",
                "description": "A brief overall summary of the lease analysis",
            },
        },
        "required": ["flagged_clauses", "summary"],
    },
}


def _call_claude(system_prompt: str, user_content) -> AnalysisResponse:
    """Shared Claude API call. user_content can be a string or a list of content blocks."""
    if not settings.anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not configured. Set it in the .env file.")

    try:
        response = _get_client().messages.create(
            model=settings.claude_model,
            max_tokens=settings.claude_max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
            tools=[ANALYSIS_TOOL],
            tool_choice={"type": "tool", "name": "report_lease_analysis"},
        )
    except anthropic.RateLimitError:
        raise RuntimeError("Analysis service is temporarily busy. Please try again in a moment.")
    except anthropic.APITimeoutError:
        raise RuntimeError("Analysis took too long. Please try again.")
    except anthropic.APIError as e:
        raise RuntimeError(f"Analysis service error: {e.message}")

    for block in response.content:
        if block.type == "tool_use":
            return AnalysisResponse(**block.input)

    raise RuntimeError("Analysis service returned an unexpected format.")


async def analyze_lease(lease_text: str) -> AnalysisResponse:
    """Analyze lease from extracted text."""
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(lease_text)
    return _call_claude(system_prompt, user_prompt)


async def analyze_lease_images(page_images: list[dict]) -> AnalysisResponse:
    """Analyze lease from page images (scanned PDFs). Uses Claude vision."""
    system_prompt = build_system_prompt()
    user_content = [
        {"type": "text", "text": (
            "Analyze the following Ontario residential lease agreement shown in the page images below. "
            "Read all text visible in the images and identify all clauses that may violate or conflict "
            "with the Residential Tenancies Act, 2006."
        )},
        *page_images,
    ]
    return _call_claude(system_prompt, user_content)
