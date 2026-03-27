from fastapi import HTTPException, Request

from config import settings


def check_access_code(request: Request) -> None:
    """Validate the access code header if one is configured."""
    if not settings.access_code:
        return
    code = request.headers.get("X-Access-Code", "")
    if code.lower().strip() != settings.access_code.lower().strip():
        raise HTTPException(status_code=401, detail="Invalid access code.")
