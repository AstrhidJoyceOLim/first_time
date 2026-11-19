# Frame-by-frame analysis — instagram.com/reels/DfuhrDdN975

Source: @vibha.in.progress, "HOW CLAUDE EDITS MY REELS", 37.3 s, 30 fps,
1440x2560, VP9. 37 frames extracted at 1 fps with:
`ffmpeg -i reel.mp4 -vf fps=1 frames/frame_%03d.jpg`
All 37 were viewed (contact sheet + full-size checks of frames 003, 009,
014, 020, 028, 032). The layout never changes: brown background, title at
top, RAW on the left, EDITED BY CLAUDE on the right, footer
"all by Claude · 1 plugin · 1 hour" on every frame.

## 0:00–0:05 — Hook / caption styles switching

- 00s (frame 001): split screen established. Creator top-down, then on sofa.
- 02s (frame 003): edited side shows curved, arched captions:
  "even come / of these captions" in white + yellow, and below
  "where did all / Wait," — captions are *not* a straight subtitle bar.
  They arc over the head, change colour mid-phrase, and use mixed case.
  A small pixel-art orange character sits at right.
- 03s (frame 004): "Every time"
- 04s (frame 005): "THEY / switch" — "switch" in large yellow italic serif.
  Point: the same spoken line can be restyled instantly; style is data,
  not re-editing.
- 07–08s (frames 008–009): "actual / liquid / glass" — huge translucent
  bubble / liquid-glass letters filling the top half of the edited frame,
  with rainbow refraction. The raw side is a plain white wall; the edited
  side is a warm bookshelf / living-room grade.

Inference: caption engine = word-timed text + a style template
(font, colour, curve, scale, glow, glass shader). Switching style =
changing the template name, re-rendering the same word timings.

## 0:10–0:17 — Background replacement + captions behind the head

- 11s (frame 012): "of every frame"
- 13–14s (frames 014–015): edited background is *completely replaced*:
  sunset gradient (orange to purple), bookshelf with warm lights,
  hanging plant top-left, red sofa. Raw background is a white wall /
  grey sofa. Caption "behind" sits *above* the head, with the pixel
  character and a pink asterisk sticker top-right.
- The person is cleanly cut out — hair edges hold up — so this is person
  segmentation / matting, not a simple background blur.

Inference: per-frame person mask (e.g. MediaPipe Selfie Segmentation,
Rembg / SAM, or Remotion + a segmentation model), composited as:
background plate → caption layer (behind) → person mask → caption layer
(in front). That layer order is what makes "words behind your head" work.

## 0:18–0:24 — The masking demo (the core claim)

- 18–19s (frames 019–020): edited side shows a blue bounding box and
  label "frame 0389 / 1305" at top, and a large blue "frame" label
  "145 x 64" with a cursor dragging its corner. This is a screen recording
  of the editor UI, overlaid on the reel.
  On-screen spoken captions: "you'd have to / mask" / "frame" / "for just" /
  "for just one word."
- 1305 frames = 43.5 s at 30 fps, close to the 37.3 s downloaded file
  (the difference is the editor's source clip / handles). Frame 389 is
  ~13 s in. The point is explicit: previously, masking *one word* meant
  hand-masking every frame; now the mask is tracked automatically.

Inference: mask = tracked segmentation mask, propagated frame-to-frame
(optical flow / tracking), with a per-word bounding box. The editor
exposes frame number, box size, and a draggable handle — i.e. it is a
normal video editor's mask UI, auto-filled by AI.

## 0:25–0:30 — Caption pack + comment CTA

- 25–27s (frames 026–028): "neon" in pink neon, then huge yellow neon
  "CAPTIONS", with an Instagram comment box at the bottom reading
  "CAPTION | Post". This is the CTA: comment `CAPTIONS` to get 7 free
  caption styles.
- The creator's own repos confirm this: 7 free styles, MIT licence,
  `/captions pop-sticker`, etc. (see README.md).

## 0:30–0:37 — The plugin UI / storyboard

- 31–32s (frames 032–033): a floating macOS-style window titled
  "caption editor", 4x zoom badge. Inside: a preview with "your" in red,
  and a right panel:
  - Effect name: "Wall Light"
  - Description: "The line glows onto the angled wall like projected
    light, mapped to the room's real perspective lines. …"
  - Size slider: 135%
  - Position: -0.2, -1.8, with arrow keys + Reset
  - "Or drag on the video. Arrow keys nudge 1px."
  - Layer: [As designed] [Behind you] [In front]
  - Verdict: [Keep] [Needs a tweak] [Cut]
  - "- Claude" signature at bottom
  - Spoken caption underneath: "and a link to / MY / video"
- 33–34s: "studio" / "plugin" / "do all of" — the Hop Studio plugin
  window, showing a storyboard / checklist.
- 35–36s (frames 036–037): "Make sure" / "see you" + a comment bubble.
  End card / follow CTA.

Inference: the workflow is *agentic + human-approved*. Claude proposes
an effect with parameters (size, position, layer, verdict), shows check
frames, the human keeps / tweaks / cuts it. It is not fully automatic,
and it is not a black box — every effect is a named, parameterised
object in a list.

## What is NOT in the video

- No terminal, no code editor with source, no GitHub URL for Hop Studio,
  no API key, no model name, no prompt text (except the slash commands
  `/captions`, `/effects`, `/video-studio:studio` from the creator's
  other posts / pages).
- No audio waveform, LUFS meter, or SFX list on screen in this reel.
- No price on screen. Pricing / paywall questions appear in comments.

## Reconstructed spoken captions (partial, from on-screen text only)

In order, as they appear on the edited side. Gaps are frames where the
caption was off-screen, too small to read, or a UI panel covered it.
This is *not* a verified ASR transcript.

> "… even come [?] of these captions … where did all … Wait, …
> Every time … THEY switch … actual liquid glass … by Claude …
> of every frame … behind … you'd have to mask … frame … for just …
> for just one word. … [neon] CAPTIONS … and a link to MY video …
> studio … plugin … do all of … Make sure … see you …"

The intended meaning, from the creator's summary and the visuals, is:
she used to mask frame-by-frame for one word; Claude now does the
captions, masking, background and effects instantly; comment CAPTIONS
for 7 free styles, and the link is to her video-studio plugin.

## Effect inventory observed

1. Split-screen RAW vs EDITED, persistent title + footer
2. Word-level animated captions, curved / arched layout
3. Style switching per phrase (yellow italic, neon, glass, pop-sticker)
4. Liquid-glass / bubble text with refraction
5. Neon glow text
6. Background replacement (sunset + bookshelf + warm grade)
7. Colour grade: warm, contrasty, vignette on edited side
8. Person segmentation / masking, tracked per frame
9. Text behind the head (layering)
10. Pixel-art character + asterisk stickers
11. Caption-editor UI: Wall Light, size / position / layer / verdict
12. Storyboard / plugin UI, comment CTA "CAPTIONS"
