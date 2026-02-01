---
name: docx
description: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"
---

# DOCX Processing

Create, edit, and analyze Word documents (.docx files).

## Workflow Decision Tree

| Task | Workflow |
|------|----------|
| Read/analyze content | pandoc text extraction or raw XML |
| Create new document | docx-js (JavaScript) |
| Edit existing document | OOXML editing (Python) |
| Edit someone else's doc | Redlining workflow (tracked changes) |

## Reading Content

```bash
# Convert to markdown with tracked changes
pandoc --track-changes=all document.docx -o output.md

# Unpack for raw XML access
python ooxml/scripts/unpack.py document.docx unpacked/
# Key files: word/document.xml, word/comments.xml, word/media/
```

## Creating Documents

Use docx-js (JavaScript). **MANDATORY**: Read [`docx-js.md`](docx-js.md) completely first.

```javascript
import { Document, Paragraph, TextRun, Packer } from "docx";
const doc = new Document({ sections: [{ children: [new Paragraph({ children: [new TextRun("Hello")] })] }] });
const buffer = await Packer.toBuffer(doc);
```

## Editing Documents

Use OOXML editing (Python). **MANDATORY**: Read [`ooxml.md`](ooxml.md) completely first.

```bash
python ooxml/scripts/unpack.py document.docx unpacked/
# Edit with Python Document library
python ooxml/scripts/pack.py unpacked/ output.docx
```

## Redlining Workflow (Tracked Changes)

For legal, academic, business docs or editing someone else's document:

1. `pandoc --track-changes=all doc.docx -o current.md`
2. Identify and group changes (batches of 3-10)
3. Read [`ooxml.md`](ooxml.md), unpack document
4. Implement changes using Document library (minimal, precise edits)
5. `python ooxml/scripts/pack.py unpacked/ reviewed.docx`
6. Verify: `pandoc --track-changes=all reviewed.docx -o verify.md`

**Principle**: Only mark text that actually changes. Preserve unchanged text with original RSID.

## Converting to Images

```bash
soffice --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page  # Creates page-1.jpg, page-2.jpg...
```

## Reference Documentation

| Document | Description |
|----------|-------------|
| [docx-js.md](docx-js.md) | JavaScript document creation API |
| [ooxml.md](ooxml.md) | Python OOXML editing, Document library |

## Dependencies

- pandoc: Text extraction
- docx (npm): Creating documents
- LibreOffice: PDF conversion
- poppler-utils: PDF to images
- defusedxml: Secure XML parsing
