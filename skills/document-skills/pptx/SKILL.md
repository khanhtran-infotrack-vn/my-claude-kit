---
name: pptx
description: "Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks"
---

# PPTX Creation, Editing, and Analysis

Work with .pptx files (ZIP archives containing XML). Different tools for different tasks.

## Reading Content

**Text extraction**:
```bash
python -m markitdown path-to-file.pptx
```

**Raw XML access** (for comments, notes, layouts, animations):
```bash
python ooxml/scripts/unpack.py <office_file> <output_dir>
```

Key files: `ppt/slides/slide{N}.xml`, `ppt/notesSlides/`, `ppt/comments/`, `ppt/theme/`

## Creating New Presentations

### Without Template (html2pptx)

1. **Read**: `html2pptx.md` completely for syntax and rules
2. **Design**: Load `references/design-principles.md` for colors and visual options
3. **Create HTML** slides (720pt × 405pt for 16:9)
   - Use `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` for text
   - `class="placeholder"` for charts/tables
   - Rasterize gradients/icons as PNG first
4. **Convert**: Run `scripts/html2pptx.js` to generate PowerPoint
5. **Validate**: `python scripts/thumbnail.py output.pptx` - check for cutoff/overlap

**Requirements**:
- Web-safe fonts only: Arial, Helvetica, Times New Roman, Georgia, Verdana, etc.
- Two-column layout for charts/tables (never vertical stack)
- State design approach before coding

### With Template

Load `references/template-workflow.md` for complete 7-step workflow:
1. Extract template text and thumbnails
2. Analyze and create inventory
3. Create outline with template mapping
4. Rearrange slides: `python scripts/rearrange.py`
5. Extract inventory: `python scripts/inventory.py`
6. Create replacement JSON
7. Apply: `python scripts/replace.py`

## Editing Existing Presentations

1. **Read**: `ooxml.md` completely for OOXML structure
2. **Unpack**: `python ooxml/scripts/unpack.py <file> <dir>`
3. **Edit XML**: Modify `ppt/slides/slide{N}.xml`
4. **Validate**: `python ooxml/scripts/validate.py <dir> --original <file>`
5. **Pack**: `python ooxml/scripts/pack.py <dir> <file>`

## Utilities

- **Thumbnails**: `references/thumbnails.md` - grid generation and image conversion
- **Rearrange**: `python scripts/rearrange.py template.pptx output.pptx 0,34,50`
- **Inventory**: `python scripts/inventory.py working.pptx inventory.json`
- **Replace**: `python scripts/replace.py input.pptx replacements.json output.pptx`

## Dependencies

- markitdown: `pip install "markitdown[pptx]"`
- pptxgenjs, playwright, react-icons, sharp: `npm install -g`
- LibreOffice, Poppler, defusedxml for PDF/image conversion
