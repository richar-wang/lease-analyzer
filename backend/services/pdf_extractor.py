import base64

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text_parts = []

    # Extract fillable form field values (Ontario Standard Lease is a fillable PDF)
    form_fields = []
    for page in doc:
        widgets = page.widgets()
        if widgets:
            for widget in widgets:
                label = widget.field_name or ""
                value = widget.field_value or ""
                if value.strip():
                    form_fields.append(f"{label}: {value}")

    if form_fields:
        text_parts.append("=== FORM FIELD DATA ===")
        text_parts.append("\n".join(form_fields))
        text_parts.append("=== END FORM FIELD DATA ===\n")

    # Extract body text with sort=True for proper reading order
    for page in doc:
        page_text = page.get_text(sort=True)
        if page_text.strip():
            text_parts.append(page_text)

    doc.close()
    return "\n".join(text_parts)


def extract_pages_as_images(pdf_bytes: bytes, dpi: int = 200) -> list[dict]:
    """Render each PDF page as a base64-encoded PNG for Claude vision."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        png_bytes = pix.tobytes("png")
        b64 = base64.b64encode(png_bytes).decode("ascii")
        pages.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": b64,
            },
        })
    doc.close()
    return pages
