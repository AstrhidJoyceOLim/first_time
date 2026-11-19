# How to reproduce it — architecture and build plan

This is an original, functional reproduction. It does not copy Hop
Studio, which is a paid closed plugin. It rebuilds the *observable*
behaviour with open tools.

## 1. Pipeline (the whole system in 5 stages)

```
raw talking-head mp4
  -> 1. transcribe (Whisper, word timestamps)
  -> 2. plan (LLM / rules: pick caption style + effect + layer per phrase)
  -> 3. segment + track (person mask per frame)
  -> 4. render (Remotion / HTML+Canvas, or FFmpeg+ASS, per frame)
  -> 5. review (storyboard check-frames, Keep / Tweak / Cut)
  -> edited mp4, 9:16, 1080x1920 or 1440x2560
```

### Stage 1 — Transcription
- Tool: `whisper.cpp` or `faster-whisper`, small/base model, `word_timestamps=True`.
- Output: `words.json`: `[{word, start, end, score}]`, plus segments.
- Why it matters: every caption, mask, and effect in the reel is timed
  to a *word*, not to a second. Without word timestamps you cannot do
  "for just one word" masking or per-word highlighting.
- See `reproduce/transcribe.py`.

### Stage 2 — Planning / the "brain"
- Input: transcript + a library of effects (see `caption_styles.json`).
- A Claude Code plugin / skill is, in practice: a folder of markdown
  prompts + scripts + templates, invoked by a slash command.
  Example (from the creator's free repos):
  - `/captions pop-sticker`
  - `/effects orbit from 3 to 6 seconds`
  - `/video-studio:studio`
- The planner's job, per phrase:
  - choose 1 keyword to highlight (colour / scale up)
  - choose a caption style (curved, neon, liquid-glass, pop-sticker…)
  - choose a layer: `behind` / `in-front` / `as-designed`
  - choose an effect, if any: Wall Light, background swap, orbit, etc.
  - choose size / position (e.g. Wall Light: size 135%, pos -0.2, -1.8)
- You can implement this first as *rules* (highlight nouns / verbs,
  switch style every 2–3 phrases), then let an LLM rewrite the plan.
  The reel's "brain" is this plan — not a video-generation model.
  Claude does not generate the footage; it writes the edit.

### Stage 3 — Segmentation / tracking
- Goal: a clean person mask for every frame, so text can go behind
  the head and the background can be replaced.
- Options, cheapest first:
  1. MediaPipe Selfie Segmentation (fast, good for talking head)
  2. `rembg` (U2-Net) — per-frame, then temporal smoothing
  3. SAM 2 — video tracking, best edges, heaviest
- Track the mask: propagate with optical flow, smooth edges over
  3–5 frames to avoid flicker. Store mask as a grayscale video or
  per-frame PNGs.
- The reel proves tracking: frame 0389 / 1305, box 145x64, draggable
  handle — the mask is a tracked object, not a one-off cutout.
- Face tracking for effects: MediaPipe Face Mesh gives a stable
  head centre; effects that "follow your face" anchor to it, and
  anything that would cover the face is forced to the `behind` layer.

### Stage 4 — Rendering
Two honest routes. Pick one.

**A. Remotion (what the ecosystem uses — recommended)**
- Remotion = React code → video. Claude Code has an official plugin:
  `claude plugin marketplace add remotion-dev/claude-code-plugin`
  `claude plugin install remotion@remotion`
- Each caption style = a React component. Each effect = a component
  with props (size, position, layer, colour). The transcript + plan
  become props. Render with `npx remotion render`.
- Pros: text layout, curves, glass, animation are easy in CSS.
  Preview in Remotion Studio, approve frames, re-render.
- Cons: needs Node, React knowledge.

**B. FFmpeg + ASS subtitles + Pillow (what `reproduce/` does)**
- Render captions as ASS (Advanced Substation Alpha) with per-word
  timing, or as PNG overlays per word with Pillow, composited with
  FFmpeg `overlay` / `chromakey` / `maskedmerge`.
- Liquid glass / neon: Pillow blur + glow, or FFmpeg `geq` / `boxblur`.
- Background replacement: `ffmpeg -i raw -i bg -i mask -filter_complex
  "[1][2]maskedmerge"` — or do it in OpenCV per frame.
- Pros: no Node/React, runs anywhere FFmpeg runs.
  Cons: curved text and glass are harder; ASS cannot do true glass.

Either way, keep the render *deterministic from a plan file*:
`words.json + plan.json -> edited.mp4`. That is the key insight:
the edit is code + data, so Claude can edit it by editing text.

### Stage 5 — Review UI
- Render check frames (e.g. 1 per effect, 1 per style change).
- For each effect show: name, size, position, layer, verdict
  Keep / Needs a tweak / Cut — exactly as in frame 032 ("Wall Light").
- Only after approval, render the full 30 fps output.
- This is why "1 hour" is credible: most of the hour is review,
  not manual masking.

## 2. Caption styles (observed → implementable)

See `caption_styles.json`. In short:

| Style | Look in reel | Implementation |
|---|---|---|
| pop-sticker | bold, sticker outline, pops per word | Pillow bold font + stroke, scale 1.2 on entry |
| curved / arc | text arched over head | draw each letter on a circular path |
| neon | yellow/pink glow | font + multi-pass blur glow |
| liquid-glass | huge translucent bubble letters | blurred, brightened text with refraction-ish highlight, low opacity fill |
| behind-head | word sits behind person | render caption, then composite person mask on top |
| wall-light | glowing line on wall, perspective-mapped | skewed gradient line, `behind` layer |
| smoke-exit / retro-typer | (in free pack, not in this reel) | fade / typewriter per character |

Highlight rule observed: 1 keyword per line in a contrasting colour
(yellow on white, or vice versa).

## 3. Effects catalogue (observed)

- orbit, spotlight, wall-light, background swap (sunset/bookshelf),
  warm colour grade + vignette, pixel sticker, asterisk sticker.
- Free pack has 51 effects; full Studio claims 220+.
- Rule from the free repos: "Every effect follows your face.
  Anything that would cover your face goes behind your head instead."

## 4. Minimal build order (do this first)

1. `ffmpeg` + Whisper → `words.json` for your clip.
2. One caption style, hard-coded, rendered with FFmpeg/ASS.
3. Person mask with MediaPipe, one background swap.
4. Add a second style + a plan file, switch style per phrase.
5. Add the review step: dump 6 check frames, approve, render full.
6. Only then add Remotion, SFX, LUFS loudness, etc.

## 5. What to buy vs build

- If you want the *exact* Hop Studio library: buy it at
  https://www.vibha.is/ai-video-studio — it needs a paid Claude plan,
  one payment, live setup. Do not try to pirate it; the video gives
  you no code to pirate.
- If you want the *capability*: build the pipeline above. The free
  MIT packs (`claude-caption-styles`, `claude-video-effects`) are a
  legitimate head start, and Remotion's official plugin is free for
  individuals / companies up to 3 people.
- Sound: the reel's full version claims 190+ SFX. Add SFX last,
  with `earshot`-style timing (SFX on word emphasis, LUFS check).

## 6. Files in this repo

- `reproduce/transcribe.py` — Whisper word timestamps → words.json
- `reproduce/caption_overlay.py` — ASS + FFmpeg render, style switch
- `reproduce/effects.py` — Pillow helpers: neon, glass, pop-sticker, arc
- `reproduce/requirements.txt`
- `caption_styles.json`, `frames_index.md`
