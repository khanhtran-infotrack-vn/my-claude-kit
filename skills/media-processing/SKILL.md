---
name: media-processing
description: Process multimedia files with FFmpeg (video/audio encoding, conversion, streaming, filtering, hardware acceleration) and ImageMagick (image manipulation, format conversion, batch processing, effects, composition). Use when converting media formats, encoding videos with specific codecs (H.264, H.265, VP9), resizing/cropping images, extracting audio from video, applying filters and effects, optimizing file sizes, creating streaming manifests (HLS/DASH), generating thumbnails, batch processing images, creating composite images, or implementing media processing pipelines. Supports 100+ formats, hardware acceleration (NVENC, QSV), and complex filtergraphs.
---

# Media Processing Skill

Process video, audio, and images using FFmpeg and ImageMagick CLI tools.

## Tool Selection

| Task | Tool |
|------|------|
| Video encoding/conversion | FFmpeg |
| Audio extraction/conversion | FFmpeg |
| Image resize/effects | ImageMagick |
| Batch image processing | ImageMagick (mogrify) |
| Video thumbnails | FFmpeg |
| GIF from video | FFmpeg |
| Streaming (HLS/DASH) | FFmpeg |

## Installation

```bash
# macOS
brew install ffmpeg imagemagick

# Ubuntu/Debian
sudo apt-get install ffmpeg imagemagick
```

## Quick Reference

### Video

```bash
# Convert (copy streams, fast)
ffmpeg -i input.mkv -c copy output.mp4

# Re-encode H.264
ffmpeg -i input.avi -c:v libx264 -crf 22 -c:a aac output.mp4

# Resize to 720p
ffmpeg -i input.mp4 -vf scale=-1:720 -c:a copy output.mp4

# Extract audio
ffmpeg -i video.mp4 -vn -c:a copy audio.m4a

# HLS streaming
ffmpeg -i input.mp4 -c:v libx264 -preset fast -crf 22 \
  -c:a aac -f hls -hls_time 6 playlist.m3u8

# Thumbnail at 5s
ffmpeg -ss 00:00:05 -i video.mp4 -vframes 1 thumb.jpg
```

### Images

```bash
# Convert format
magick input.png output.jpg

# Resize (maintain aspect)
magick input.jpg -resize 800x600 output.jpg

# Square thumbnail
magick input.jpg -resize 200x200^ -gravity center -extent 200x200 thumb.jpg

# Batch resize
mogrify -resize 800x -quality 85 *.jpg

# Add watermark
magick input.jpg watermark.png -gravity southeast -geometry +10+10 -composite output.jpg
```

### GIF Creation

```bash
# High quality with palette
ffmpeg -i input.mp4 -vf "fps=15,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

## Common Parameters

**FFmpeg Video**: `-c:v` (codec), `-crf` (quality 0-51), `-preset` (speed), `-vf` (filters)
**FFmpeg Audio**: `-c:a` (codec), `-b:a` (bitrate), `-ar` (sample rate)
**ImageMagick Geometry**: `800x600` (fit), `800x600!` (force), `800x600^` (fill), `50%` (scale)

## Reference Documentation

- `references/ffmpeg-encoding.md` - Codecs, quality, hardware acceleration
- `references/ffmpeg-streaming.md` - HLS/DASH, live streaming
- `references/ffmpeg-filters.md` - Video/audio filters, filtergraphs
- `references/imagemagick-editing.md` - Effects, transformations
- `references/imagemagick-batch.md` - Batch processing, mogrify
