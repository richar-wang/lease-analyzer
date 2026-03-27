import json
from pathlib import Path
from typing import AsyncGenerator

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse

from config import settings
from middleware import check_access_code, check_rate_limit
from schemas.analysis import AnalysisResponse
from services.lease_analyzer import analyze_lease, analyze_lease_images
from services.pdf_extractor import extract_pages_as_images, extract_text_from_pdf

router = APIRouter(prefix="/api")


def _sse_event(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/config")
async def get_config():
    return {
        "requires_code": bool(settings.access_code),
        "access_hint": settings.access_hint,
    }


@router.post("/analyze")
async def analyze_lease_endpoint(request: Request, file: UploadFile = File(...)):
    check_access_code(request)
    check_rate_limit(request)

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=422, detail="Only PDF files are accepted.")

    contents = await file.read()
    if len(contents) > settings.max_file_size_bytes:
        raise HTTPException(status_code=413, detail="File too large. Maximum 10MB.")

    async def stream() -> AsyncGenerator[str, None]:
        yield _sse_event("status", {"step": "extracting", "message": "Extracting text from PDF..."})

        text = extract_text_from_pdf(contents)
        use_vision = not text or len(text.strip()) < 50

        if use_vision:
            yield _sse_event("status", {"step": "rendering", "message": "Scanned PDF detected. Rendering pages as images..."})
            page_images = extract_pages_as_images(contents)
            if not page_images:
                yield _sse_event("error", {"message": "Could not read this PDF."})
                return

        yield _sse_event("status", {"step": "analyzing", "message": "Analyzing lease against the RTA (this takes 15-30 seconds)..."})

        try:
            if use_vision:
                result = await analyze_lease_images(page_images)
            else:
                result = await analyze_lease(text)
        except (RuntimeError, Exception) as e:
            yield _sse_event("error", {"message": str(e)})
            return

        result.lease_text = text or ""
        yield _sse_event("status", {"step": "complete", "message": "Analysis complete!"})
        yield _sse_event("result", result.model_dump())

    return StreamingResponse(stream(), media_type="text/event-stream")


@router.get("/demo")
async def demo_analysis(request: Request):
    check_access_code(request)
    check_rate_limit(request)

    demo_path = Path(__file__).parent.parent / "sample" / "demo_lease.pdf"
    if not demo_path.exists():
        raise HTTPException(status_code=404, detail="Demo lease PDF not found.")

    contents = demo_path.read_bytes()

    async def stream() -> AsyncGenerator[str, None]:
        yield _sse_event("status", {"step": "extracting", "message": "Extracting text from demo lease..."})

        text = extract_text_from_pdf(contents)

        yield _sse_event("status", {"step": "analyzing", "message": "Analyzing lease against the RTA (this takes 15-30 seconds)..."})

        try:
            result = await analyze_lease(text)
        except (RuntimeError, Exception) as e:
            yield _sse_event("error", {"message": str(e)})
            return

        result.lease_text = text
        yield _sse_event("status", {"step": "complete", "message": "Analysis complete!"})
        yield _sse_event("result", result.model_dump())

    return StreamingResponse(stream(), media_type="text/event-stream")
