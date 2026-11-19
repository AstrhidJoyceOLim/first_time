#!/usr/bin/env python3
"""
Transcribe a talking-head clip with word-level timestamps.

This is the first stage of the pipeline in REPRODUCTION.md.
Whisper gives you the word timings that every caption, mask and
effect in the reel is timed to.

Usage:
    python3 transcribe.py your-clip.mp4 --out words.json
    python3 transcribe.py your-clip.mp4 --model base --out words.json

Requires: faster-whisper (pip install faster-whisper) and ffmpeg.
If faster-whisper is not available, use whisper.cpp instead and
convert its JSON output to the same words.json shape.
"""
import argparse
import json
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--model", default="small")
    p.add_argument("--language", default="en")
    p.add_argument("--out", default="words.json")
    args = p.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("faster-whisper is not installed. Run: pip install faster-whisper",
              file=sys.stderr)
        print("Or use whisper.cpp and convert its output to words.json.",
              file=sys.stderr)
        raise SystemExit(1)

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(
        args.video, language=args.language, word_timestamps=True)

    words = []
    for seg in segments:
        for w in (seg.words or []):
            words.append({
                "word": w.word.strip(),
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "score": round(float(w.probability), 3),
            })

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"video": args.video, "words": words}, f, indent=2)
    print(f"Wrote {len(words)} words to {args.out}")


if __name__ == "__main__":
    main()
