import asyncio
import json
import time
from pathlib import Path
from typing import AsyncGenerator

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse

from config import settings
from middleware import check_access_code
from rta.prompt_builder import SUPPORTED_LANGUAGES
from services.lease_analyzer import analyze_lease, analyze_lease_images
from services.pdf_extractor import extract_pages_as_images, extract_text_from_pdf

router = APIRouter(prefix="/api")


def _sse_event(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _get_language(request: Request) -> str:
    lang = request.headers.get("X-Language", "en")
    return lang if lang in SUPPORTED_LANGUAGES else "en"


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/config")
async def get_config():
    return {
        "requires_code": bool(settings.access_code),
        "access_hint": settings.access_hint,
    }


@router.get("/languages")
async def get_languages():
    return [{"code": code, "name": name} for code, name in SUPPORTED_LANGUAGES.items()]


@router.post("/analyze")
async def analyze_lease_endpoint(request: Request, file: UploadFile = File(...)):
    check_access_code(request)
    language = _get_language(request)

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

        yield _sse_event("status", {"step": "analyzing", "message": "Analyzing lease against the RTA..."})

        if use_vision:
            task = asyncio.create_task(analyze_lease_images(page_images, language))
        else:
            task = asyncio.create_task(analyze_lease(text, language))

        start = time.monotonic()
        last_update = start
        while not task.done():
            await asyncio.sleep(1)
            now = time.monotonic()
            if not task.done() and now - last_update >= 3:
                elapsed = int(now - start)
                yield _sse_event("status", {"step": "analyzing", "message": f"Analyzing... ({elapsed}s elapsed)"})
                last_update = now

        try:
            result = task.result()
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
    language = _get_language(request)

    demo_path = Path(__file__).parent.parent / "sample" / "demo_lease.pdf"
    if not demo_path.exists():
        raise HTTPException(status_code=404, detail="Demo lease PDF not found.")

    contents = demo_path.read_bytes()

    async def stream() -> AsyncGenerator[str, None]:
        yield _sse_event("status", {"step": "extracting", "message": "Extracting text from demo lease..."})

        text = extract_text_from_pdf(contents)

        yield _sse_event("status", {"step": "analyzing", "message": "Analyzing lease against the RTA..."})

        task = asyncio.create_task(analyze_lease(text, language))
        start = time.monotonic()
        last_update = start
        while not task.done():
            await asyncio.sleep(1)
            now = time.monotonic()
            if not task.done() and now - last_update >= 3:
                elapsed = int(now - start)
                yield _sse_event("status", {"step": "analyzing", "message": f"Analyzing... ({elapsed}s elapsed)"})
                last_update = now

        try:
            result = task.result()
        except (RuntimeError, Exception) as e:
            yield _sse_event("error", {"message": str(e)})
            return

        result.lease_text = text
        yield _sse_event("status", {"step": "complete", "message": "Analysis complete!"})
        yield _sse_event("result", result.model_dump())

    return StreamingResponse(stream(), media_type="text/event-stream")
