---
name: xlsx
description: "Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for: (1) Creating new spreadsheets with formulas and formatting, (2) Reading or analyzing data, (3) Modify existing spreadsheets while preserving formulas, (4) Data analysis and visualization in spreadsheets, or (5) Recalculating formulas"
---

# Excel/Spreadsheet Processing

Create, edit, and analyze spreadsheets with formulas, formatting, and data operations.

## Critical Rules

1. **Use Excel formulas, NOT hardcoded values** - Spreadsheets must remain dynamic
2. **Zero formula errors** - Deliver with no #REF!, #DIV/0!, #VALUE!, #N/A, #NAME?
3. **Always recalculate** - Run `python recalc.py output.xlsx` after creating/modifying

## Quick Start

```python
# Read with pandas (data analysis)
import pandas as pd
df = pd.read_excel('file.xlsx')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)

# Create with openpyxl (formulas/formatting)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
wb = Workbook()
sheet = wb.active
sheet['A1'] = 'Revenue'
sheet['B1'] = 1000
sheet['B2'] = '=B1*1.1'  # Use formulas, not calculated values!
sheet['A1'].font = Font(bold=True)
wb.save('output.xlsx')
```

## Library Selection

| Task | Library | Notes |
|------|---------|-------|
| Data analysis | pandas | `read_excel()`, `to_excel()` |
| Formulas & formatting | openpyxl | Preserves formulas, supports styling |
| Read calculated values | openpyxl | `load_workbook(data_only=True)` |

## Formula Best Practices

```python
# WRONG - Hardcoding calculated values
total = df['Sales'].sum()
sheet['B10'] = total  # Bad!

# CORRECT - Use Excel formulas
sheet['B10'] = '=SUM(B2:B9)'
sheet['C5'] = '=(C4-C2)/C2'  # Growth rate
sheet['D20'] = '=AVERAGE(D2:D19)'
```

## Financial Model Standards

**Color Coding:**
- Blue text: Hardcoded inputs/assumptions
- Black text: Formulas and calculations
- Green text: Links from other worksheets
- Yellow background: Key assumptions needing attention

**Number Formatting:**
- Years as text ("2024" not "2,024")
- Currency: `$#,##0` with units in headers
- Negatives in parentheses: `$#,##0;($#,##0);-`
- Percentages: `0.0%`
- Multiples: `0.0x`

## Workflow

1. Create/load workbook with openpyxl
2. Add data and **formulas** (not calculated values)
3. Apply formatting
4. Save file
5. **Recalculate**: `python recalc.py output.xlsx`
6. Check for errors in JSON output, fix if needed

## Recalculating Formulas

```bash
python recalc.py <excel_file> [timeout_seconds]
```

Returns JSON with error details:
```json
{"status": "success", "total_errors": 0, "total_formulas": 42}
```

Common errors to fix:
- `#REF!`: Invalid cell references
- `#DIV/0!`: Division by zero  
- `#VALUE!`: Wrong data type
- `#NAME?`: Unrecognized formula

## Tips

- Cell indices are 1-based in openpyxl
- `data_only=True` reads values but **loses formulas on save**
- Use `read_only=True` / `write_only=True` for large files
- Check column mapping (column 64 = BL, not BK)
- DataFrame row 5 = Excel row 6 (1-indexed)
