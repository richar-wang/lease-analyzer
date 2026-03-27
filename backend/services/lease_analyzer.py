import anthropic

from config import settings
from rta.prompt_builder import build_system_prompt, build_user_prompt
from schemas.analysis import AnalysisResponse

_client: anthropic.AsyncAnthropic | None = None


def _get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        _client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
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
                        "standard_lease_comparison": {
                            "type": "string",
                            "description": "How the Ontario Standard Lease (Form 2229E) handles this topic differently. Empty string if not applicable.",
                        },
                    },
                    "required": [
                        "original_clause_text",
                        "violation_type",
                        "severity",
                        "rta_section",
                        "explanation",
                        "standard_lease_comparison",
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


# Sonnet pricing per token
INPUT_COST_PER_TOKEN = 3.0 / 1_000_000   # $3 per 1M input tokens
OUTPUT_COST_PER_TOKEN = 15.0 / 1_000_000  # $15 per 1M output tokens


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 characters per token."""
    return len(text) // 4


async def _call_claude(system_prompt: str, user_content) -> AnalysisResponse:
    """Call Claude with prompt caching and async I/O."""
    if not settings.anthropic_api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not configured. Set it in the .env file.")

    # Estimate input tokens and calculate max output tokens within budget
    input_tokens_est = _estimate_tokens(system_prompt)
    if isinstance(user_content, str):
        input_tokens_est += _estimate_tokens(user_content)
    else:
        # Vision: estimate text parts, add ~1600 tokens per image
        for block in user_content:
            if isinstance(block, dict) and block.get("type") == "text":
                input_tokens_est += _estimate_tokens(block["text"])
            elif isinstance(block, dict) and block.get("type") == "image":
                input_tokens_est += 1600

    input_cost = input_tokens_est * INPUT_COST_PER_TOKEN
    remaining_budget = settings.max_cost_per_request - input_cost
    max_output_tokens = min(
        settings.claude_max_tokens,
        max(2000, int(remaining_budget / OUTPUT_COST_PER_TOKEN))
    )

    try:
        response = await _get_client().messages.create(
            model=settings.claude_model,
            max_tokens=max_output_tokens,
            system=[{
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_content}],
            tools=[{**ANALYSIS_TOOL, "cache_control": {"type": "ephemeral"}}],
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


async def analyze_lease(lease_text: str, language: str = "en") -> AnalysisResponse:
    """Analyze lease from extracted text."""
    system_prompt = build_system_prompt(language)
    user_prompt = build_user_prompt(lease_text)
    return await _call_claude(system_prompt, user_prompt)


async def analyze_lease_images(page_images: list[dict], language: str = "en") -> AnalysisResponse:
    """Analyze lease from page images (scanned PDFs). Uses Claude vision."""
    system_prompt = build_system_prompt(language)
    user_content = [
        {"type": "text", "text": (
            "Analyze the following Ontario residential lease agreement shown in the page images below. "
            "Read all text visible in the images and identify all clauses that may violate or conflict "
            "with the Residential Tenancies Act, 2006."
        )},
        *page_images,
    ]
    return await _call_claude(system_prompt, user_content)
