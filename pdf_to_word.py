#!/usr/bin/env python3
"""Convert the Multi-Party MRUNDA PDF into an editable Word (.docx)."""
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

SRC = "Multi-Party MRUNDA Acknowledgment (v10-28-2021) FORM.pdf"
OUT = "Multi-Party MRUNDA Acknowledgment (v10-28-2021) FORM.docx"

doc = fitz.open(SRC)
out = Document()

# Base style
style = out.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

for pnum, page in enumerate(doc):
    # Extract text as blocks to keep paragraph structure
    blocks = page.get_text("blocks")
    # blocks: (x0, y0, x1, y1, text, block_no, block_type)
    blocks = sorted(blocks, key=lambda b: (round(b[1]), round(b[0])))
    for b in blocks:
        text = (b[4] or "").strip()
        if not text:
            continue
        # Join wrapped lines within a block into readable paragraphs
        text = " ".join(line.strip() for line in text.splitlines() if line.strip())
        p = out.add_paragraph(text)
    if pnum < doc.page_count - 1:
        out.add_page_break()

out.save(OUT)
print("Saved:", OUT)
