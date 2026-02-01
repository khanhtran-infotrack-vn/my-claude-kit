---
name: chrome-devtools
description: Browser automation, debugging, and performance analysis using Puppeteer CLI scripts. Use for automating browsers, taking screenshots, analyzing performance, monitoring network traffic, web scraping, form automation, and JavaScript debugging.
---

# Chrome DevTools Agent Skill

Browser automation via Puppeteer scripts. All scripts output JSON.

## Installation

```bash
cd .claude/skills/chrome-devtools/scripts
./install-deps.sh    # Linux/WSL only
npm install          # All platforms
brew install imagemagick  # Optional, for compression
```

## Quick Test
```bash
node navigate.js --url https://example.com
```

## Available Scripts

Located in `scripts/`:

**Core Automation**:
- `navigate.js` - Navigate to URLs
- `screenshot.js` - Capture screenshots (auto-compresses >5MB)
- `click.js` - Click elements
- `fill.js` - Fill form fields
- `evaluate.js` - Execute JavaScript

**Analysis**:
- `snapshot.js` - Extract interactive elements
- `console.js` - Monitor console messages
- `network.js` - Track HTTP traffic
- `performance.js` - Measure Core Web Vitals

## Common Patterns

**Screenshot**:
```bash
node screenshot.js --url https://example.com --output ./docs/screenshots/page.png
```

**Chain Commands** (reuse browser):
```bash
node navigate.js --url https://example.com/login --close false
node fill.js --selector "#email" --value "user@example.com" --close false
node click.js --selector "button[type=submit]"
```

**Performance Testing**:
```bash
node performance.js --url https://example.com | jq '.vitals.LCP'
```

**Find Selectors**:
```bash
node snapshot.js --url https://example.com | jq '.elements[] | {tagName, text, selector}'
```

## Execution Protocol

**Before running**: Check `pwd` - must be in scripts directory
**After screenshots**: Verify with `ls -lh` and Read tool

## Script Options

All scripts support:
- `--headless false` - Show browser
- `--close false` - Keep browser for chaining
- `--timeout 30000` - Set timeout (ms)
- `--wait-until networkidle2` - Wait strategy

## Troubleshooting

| Error | Fix |
|-------|-----|
| Cannot find puppeteer | `npm install` |
| libnss3.so missing | `./install-deps.sh` |
| Element not found | Use `snapshot.js` for selectors |
| Screenshot >5MB | Install ImageMagick or use `--max-size 3` |

## Reference Documentation

- `references/cdp-domains.md` - 47 CDP domains
- `references/puppeteer-reference.md` - Complete API
- `references/performance-guide.md` - Core Web Vitals
- `scripts/README.md` - Script usage details
