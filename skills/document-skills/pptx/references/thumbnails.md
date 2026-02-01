# Thumbnail Generation & Image Conversion

## Creating Thumbnail Grids

```bash
python scripts/thumbnail.py template.pptx [output_prefix]
```

**Features**:
- Creates: `thumbnails.jpg` (or `thumbnails-1.jpg`, etc. for large decks)
- Default: 5 columns, max 30 slides per grid (5×6)
- Custom prefix: `python scripts/thumbnail.py template.pptx workspace/my-grid`
- Adjust columns: `--cols 4` (range 3-6)
- Grid limits: 3 cols = 12, 4 cols = 20, 5 cols = 30, 6 cols = 42
- Slides are zero-indexed

**Use cases**:
- Template analysis: understand layouts and patterns
- Content review: visual overview
- Navigation: find slides by appearance
- Quality check: verify formatting

**Examples**:
```bash
# Basic
python scripts/thumbnail.py presentation.pptx

# Custom name and columns
python scripts/thumbnail.py template.pptx analysis --cols 4
```

## Converting Slides to Images

Two-step process:

**1. Convert PPTX to PDF**:
```bash
soffice --headless --convert-to pdf template.pptx
```

**2. Convert PDF to JPEG**:
```bash
pdftoppm -jpeg -r 150 template.pdf slide
```
Creates: `slide-1.jpg`, `slide-2.jpg`, etc.

**Options**:
- `-r 150`: DPI (quality/size balance)
- `-jpeg`/`-png`: output format
- `-f N`: first page
- `-l N`: last page

**Specific range**:
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 template.pdf slide  # Pages 2-5 only
```
