# Template-Based Workflow

Create presentations following existing template's design by duplicating, rearranging, and replacing content.

## Step 1: Extract and Analyze Template

```bash
# Extract text content
python -m markitdown template.pptx > template-content.md

# Create visual thumbnail grid
python scripts/thumbnail.py template.pptx
```

## Step 2: Create Template Inventory

Save to `template-inventory.md`:
```markdown
# Template Inventory Analysis
**Total Slides: [count]**
**IMPORTANT: Slides are 0-indexed (first slide = 0, last = count-1)**

## [Category Name]
- Slide 0: [Layout code] - Description/purpose
- Slide 1: [Layout code] - Description/purpose
[... list every slide ...]
```

## Step 3: Create Outline with Template Mapping

**Match layout structure to content**:
- Single-column: unified narrative
- Two-column: exactly 2 items
- Three-column: exactly 3 items
- Image+text: only when images exist
- Quote layouts: only for actual quotes with attribution

Save `outline.md` with mapping:
```python
template_mapping = [
    0,   # Title/Cover
    34,  # Body slide
    34,  # Duplicate body
    50,  # Quote
    54,  # Closing
]
```

## Step 4: Rearrange Slides

```bash
python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
```
- 0-based indices, duplicates allowed

## Step 5: Extract Text Inventory

```bash
python scripts/inventory.py working.pptx text-inventory.json
```

JSON structure:
```json
{
  "slide-0": {
    "shape-0": {
      "placeholder_type": "TITLE",
      "paragraphs": [{"text": "...", "bold": true, "alignment": "CENTER"}]
    }
  }
}
```

## Step 6: Create Replacement JSON

Save to `replacement-text.json`:
```json
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        {"text": "New Title", "bold": true, "alignment": "CENTER"},
        {"text": "Bullet item", "bullet": true, "level": 0}
      ]
    }
  }
}
```

**Rules**:
- Shapes without "paragraphs" are cleared automatically
- When `bullet: true`, don't include bullet symbols
- Include formatting props from original inventory

## Step 7: Apply Replacements

```bash
python scripts/replace.py working.pptx replacement-text.json output.pptx
```
