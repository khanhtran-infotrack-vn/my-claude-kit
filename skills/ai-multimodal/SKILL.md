---
name: ai-multimodal
description: Process and generate multimedia content using Google Gemini API. Capabilities include analyze audio files (transcription with timestamps, summarization, speech understanding, music/sound analysis up to 9.5 hours), understand images (captioning, object detection, OCR, visual Q&A, segmentation), process videos (scene detection, Q&A, temporal analysis, YouTube URLs, up to 6 hours), extract from documents (PDF tables, forms, charts, diagrams, multi-page), generate images (text-to-image, editing, composition, refinement). Use when working with audio/video files, analyzing images or screenshots, processing PDF documents, extracting structured data from media, creating images from text prompts, or implementing multimodal AI features. Supports multiple models (Gemini 2.5/2.0) with context windows up to 2M tokens.
---

# AI Multimodal Processing Skill

Process audio, images, videos, documents, and generate images using Google Gemini API.

## Capabilities

| Capability | Audio | Image | Video | PDF |
|------------|:-----:|:-----:|:-----:|:---:|
| Transcription | ✓ | - | ✓ | - |
| Summarization | ✓ | ✓ | ✓ | ✓ |
| Q&A | ✓ | ✓ | ✓ | ✓ |
| Object Detection | - | ✓ | ✓ | - |
| Text Extraction | - | ✓ | - | ✓ |

## Quick Start

**API Key**: Set `GEMINI_API_KEY` in environment or `.env`

```bash
pip install google-genai python-dotenv pillow
```

## Common Patterns

**Transcribe Audio**:
```bash
python scripts/gemini_batch_process.py --files audio.mp3 --task transcribe
```

**Analyze Image**:
```bash
python scripts/gemini_batch_process.py --files image.jpg --task analyze \
  --prompt "Describe this image" --output docs/assets/output.md
```

**Process Video**:
```bash
python scripts/gemini_batch_process.py --files video.mp4 --task analyze \
  --prompt "Summarize with timestamps" --output docs/assets/output.md
```

**Extract from PDF**:
```bash
python scripts/gemini_batch_process.py --files doc.pdf --task extract \
  --prompt "Extract tables as JSON" --format json
```

**Generate Image**:
```bash
python scripts/gemini_batch_process.py --task generate \
  --prompt "A futuristic city" --output docs/assets/city.png \
  --model gemini-2.5-flash-image --aspect-ratio 16:9
```

## Model Selection

| Model | Use Case |
|-------|----------|
| gemini-2.5-flash | Best balance (recommended) |
| gemini-2.5-pro | Highest quality |
| gemini-2.5-flash-image | Image generation |

## Supported Formats

- **Audio**: WAV, MP3, AAC, FLAC, OGG (up to 9.5 hours)
- **Images**: PNG, JPEG, WEBP, HEIC (up to 3,600 images)
- **Video**: MP4, MOV, AVI, WebM (up to 6 hours)
- **Documents**: PDF (up to 1,000 pages)

## Reference Documentation

- `references/audio-processing.md` - Transcription, analysis, TTS
- `references/vision-understanding.md` - Detection, segmentation, OCR
- `references/video-analysis.md` - Scene detection, timestamps
- `references/document-extraction.md` - PDF processing, tables
- `references/image-generation.md` - Text-to-image, editing

## Scripts

- `gemini_batch_process.py` - Batch process media files
- `media_optimizer.py` - Prepare media for API limits
- `document_converter.py` - Convert documents to PDF

## Cost Optimization

- Use `gemini-2.5-flash` for most tasks
- Use File API for files >20MB
- Process specific segments vs full videos
- Batch process multiple files in parallel
