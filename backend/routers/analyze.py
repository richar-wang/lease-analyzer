from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from config import settings
from schemas.analysis import AnalysisResponse
from services.lease_analyzer import analyze_lease, analyze_lease_images
from services.pdf_extractor import extract_pages_as_images, extract_text_from_pdf

router = APIRouter(prefix="/api")


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_lease_endpoint(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=422, detail="Only PDF files are accepted.")

    contents = await file.read()
    if len(contents) > settings.max_file_size_bytes:
        raise HTTPException(status_code=413, detail="File too large. Maximum 10MB.")

    text = extract_text_from_pdf(contents)

    try:
        if text and len(text.strip()) >= 50:
            result = await analyze_lease(text)
        else:
            # Scanned/image PDF — fall back to Claude vision
            page_images = extract_pages_as_images(contents)
            if not page_images:
                raise HTTPException(status_code=422, detail="Could not read this PDF.")
            result = await analyze_lease_images(page_images)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Unexpected error: {type(e).__name__}: {e}")

    return result


@router.get("/demo", response_model=AnalysisResponse)
async def demo_analysis():
    demo_path = Path(__file__).parent.parent / "sample" / "demo_lease.pdf"
    if not demo_path.exists():
        raise HTTPException(status_code=404, detail="Demo lease PDF not found.")

    contents = demo_path.read_bytes()
    text = extract_text_from_pdf(contents)

    try:
        result = await analyze_lease(text)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Unexpected error: {type(e).__name__}: {e}")

    return result
