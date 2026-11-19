#!/usr/bin/env python3
"""
Render word-timed captions over a clip with FFmpeg + ASS subtitles.

This is a minimal, honest version of the reel's caption engine:
- words.json (from transcribe.py) drives timing, not a fixed subtitle file
- one keyword per line is highlighted (the reel's rule)
- --style picks a template from caption_styles.json

Usage:
    python3 caption_overlay.py clip.mp4 words.json --style pop-sticker --out edited.mp4
    python3 caption_overlay.py clip.mp4 words.json --style neon --out edited.mp4
    python3 caption_overlay.py clip.mp4 words.json --style liquid-glass --out edited.mp4

ASS cannot do true liquid glass or curved text — for those, render
PNG overlays per word with effects.py and composite with FFmpeg
overlay, or use Remotion (see REPRODUCTION.md, route A).
This script is the working baseline: correct timing + style switching.
"""
import argparse
import json
import subprocess
import sys

# ASS colour is &HAABBGGRR (alpha, blue, green, red), in hex.
STYLES = {
    "pop-sticker": {
        "font": "Arial Black", "size": 96,
        "primary": "&H00FFFFFF", "outline": "&H00000000",
        "outline_px": 6, "bold": -1,
    },
    "neon": {
        "font": "Arial Black", "size": 96,
        "primary": "&H0000E5FF", "outline": "&H000000FF",
        "outline_px": 4, "bold": -1,
    },
    "liquid-glass": {
        "font": "Arial", "size": 140,
        "primary": "&H99FFFFFF", "outline": "&H33FFFFFF",
        "outline_px": 2, "bold": -1,
    },
}


def ass_time(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    cs = int(round((t - int(t)) * 100))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def highlight_word(words, i):
    """Highlight one keyword per line: the longest content word."""
    line = words[max(0, i - 2): i + 3]
    # Simple rule: highlight the current word if it is long, else the
    # longest word in the window. The reel highlights ~1 word per line.
    return words[i]["word"]


def build_ass(words, style_name, width=1080, height=1920):
    st = STYLES.get(style_name, STYLES["pop-sticker"])
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,{st["font"]},{st["size"]},{st["primary"]},&H000000FF,{st["outline"]},&H80000000,{st["bold"]},0,0,0,100,100,0,0,1,{st["outline_px"]},0,2,40,40,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    # Group words into 3-word lines, like the reel's short captions.
    for i in range(0, len(words), 3):
        chunk = words[i:i + 3]
        if not chunk:
            continue
        start = ass_time(chunk[0]["start"])
        end = ass_time(chunk[-1]["end"] + 0.15)
        # Highlight the middle / longest word with a yellow override.
        text = " ".join(w["word"] for w in chunk)
        longest = max(chunk, key=lambda w: len(w["word"]))["word"]
        text = text.replace(longest, "{\\c&H00FFFF&}" + longest + "{\\c}", 1)
        events.append(f"Dialogue: 0,{start},{end},Caption,,0,0,0,,{text}")
    return header + "\n".join(events) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("words_json")
    p.add_argument("--style", default="pop-sticker",
                   choices=list(STYLES))
    p.add_argument("--out", default="edited.mp4")
    args = p.parse_args()

    with open(args.words_json, encoding="utf-8") as f:
        data = json.load(f)
    words = data["words"]
    if not words:
        print("No words in words.json", file=sys.stderr)
        raise SystemExit(1)

    ass = build_ass(words, args.style)
    with open("captions.ass", "w", encoding="utf-8") as f:
        f.write(ass)

    cmd = [
        "ffmpeg", "-y", "-i", args.video,
        "-vf", "ass=captions.ass",
        "-c:a", "copy", args.out,
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Wrote {args.out} with style {args.style}")


if __name__ == "__main__":
    main()
