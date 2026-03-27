import time
from collections import defaultdict

from fastapi import HTTPException, Request

from config import settings

# In-memory rate limit store: {ip: [timestamp, timestamp, ...]}
_request_log: dict[str, list[float]] = defaultdict(list)


def check_access_code(request: Request) -> None:
    """Validate the access code header if one is configured."""
    if not settings.access_code:
        return
    code = request.headers.get("X-Access-Code", "")
    if code.lower().strip() != settings.access_code.lower().strip():
        raise HTTPException(status_code=401, detail="Invalid access code.")


def check_rate_limit(request: Request) -> None:
    """Enforce per-IP rate limiting."""
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    one_hour_ago = now - 3600

    # Clean old entries
    _request_log[ip] = [t for t in _request_log[ip] if t > one_hour_ago]

    if len(_request_log[ip]) >= settings.rate_limit_per_hour:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {settings.rate_limit_per_hour} analyses per hour.",
        )

    _request_log[ip].append(now)
