---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.
---

# PDF Processing Guide

Process, create, and manipulate PDF documents using Python libraries and CLI tools.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read and extract text
reader = PdfReader("document.pdf")
text = "".join(page.extract_text() for page in reader.pages)

# Merge PDFs
writer = PdfWriter()
for pdf in ["doc1.pdf", "doc2.pdf"]:
    for page in PdfReader(pdf).pages:
        writer.add_page(page)
with open("merged.pdf", "wb") as f:
    writer.write(f)
```

## Library Selection

| Task | Library | Key Function |
|------|---------|--------------|
| Merge/Split PDFs | pypdf | `PdfWriter.add_page()` |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Fill PDF forms | pdf-lib (JS) / pypdf | See [forms.md](forms.md) |
| OCR scanned PDFs | pytesseract + pdf2image | Convert to image first |

## Common Operations

```python
# Extract tables to DataFrame
import pdfplumber, pandas as pd
with pdfplumber.open("doc.pdf") as pdf:
    tables = [pd.DataFrame(t[1:], columns=t[0]) 
              for page in pdf.pages for t in page.extract_tables() if t]

# Create PDF with reportlab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
c = canvas.Canvas("output.pdf", pagesize=letter)
c.drawString(100, 700, "Hello World!")
c.save()

# Add password protection
writer = PdfWriter()
for page in PdfReader("input.pdf").pages:
    writer.add_page(page)
writer.encrypt("userpass", "ownerpass")
with open("encrypted.pdf", "wb") as f:
    writer.write(f)
```

## CLI Tools

```bash
# pdftotext (poppler-utils)
pdftotext -layout input.pdf output.txt

# qpdf - merge, split, rotate
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf output.pdf --rotate=+90:1

# Extract images
pdfimages -j input.pdf output_prefix
```

## Reference Documentation

| Document | Description |
|----------|-------------|
| [reference.md](reference.md) | Advanced pypdfium2, JavaScript libraries, troubleshooting |
| [forms.md](forms.md) | PDF form filling with pdf-lib and pypdf |

## Best Practices

- Use pypdf for basic operations (merge, split, metadata)
- Use pdfplumber for text/table extraction with layout preservation
- Use reportlab for programmatic PDF creation
- For scanned PDFs, convert to images first then OCR with pytesseract
- Always verify PDF structure before processing complex forms
