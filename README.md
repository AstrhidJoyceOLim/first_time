# first_time — How Claude Edits My Reels, reverse-engineered

Reverse-engineering notes and a working, original reproduction of the
AI reel-editing workflow shown in this Instagram reel:

- Source reel: https://www.instagram.com/reels/DfuhrDdN975/
- Creator: Vibha — AI · Careers · Marketing (@vibha.in.progress), verified,
  90,141 followers at time of check
- Co-author / plugin: Hop Studio (@get.hopstudio)
- Posted: 2026-11-14 07:29:17
- Engagement at check: 1,695 likes, 5,785 comments
- Hashtags: #claudecode #aivideoeditor #aivideoediting #claude #aitutorial
- Video downloaded with yt-dlp: 37.3 s, 1440x2560, 30 fps, VP9 + AAC,
  11,542,962 bytes, 1,305 frames total (frame 0389 / 1305 is visible on screen)
- Local copy kept at: `~/workspace/instagram_reel_DfuhrDdN975/reel.mp4`
  (37 frames extracted at 1 fps, plus a contact sheet — **not** pushed here,
  because the original video is the creator's copyrighted work and the
  GitHub snapshot tool only accepts UTF-8 text files)

## What the reel actually is

A split-screen demo, titled on screen:

> HOW CLAUDE EDITS MY REELS
> RAW | EDITED BY CLAUDE
> all by Claude · 1 plugin · 1 hour

Left = raw talking-head footage. Right = the same footage after Claude.
The creator says she used to mask herself frame-by-frame for one word.
Now Claude does it instantly.

It is a promotion for **Hop Studio** — a paid Claude Code plugin / AI video
editor inside Claude — and for its free starter packs (see below). It is
*not* a video that contains source code. No code, API key, model weight,
or plugin ZIP is visible in any frame. So this repo does not claim to be
a copy of Hop Studio. It is a functional reproduction: the same effects,
built from first principles with open tools.

## What is in this repo

- `ANALYSIS.md` — frame-by-frame log (all 37 one-second frames), what each
  effect is, and the exact on-screen text / UI that proves it.
- `REPRODUCTION.md` — architecture, pipeline, and how to build the same
  thing yourself, step by step.
- `caption_styles.json` — the 7+ caption styles observed, as data.
- `frames_index.md` — per-second index.
- `reproduce/` — original Python + FFmpeg code to do it on your own clip:
  transcribe with word timestamps, render animated captions, apply
  liquid-glass / neon / pop-sticker styles, and do a behind-the-head layer.
  No Hop Studio code is included, and none was copied.
- `hyrox-kids/` — second study, for promoting HYROX for kids:
  `ANALYSIS.md` (58 frames, HYROX Youngstars, Birmingham, Laurence
  10-11), `REPRODUCTION.md` (chapter template + edit recipe +
  safeguarding checklist), `frames_index.md`, `shot-list.md`.
  Source: https://www.instagram.com/reel/DfKctoVs1uI/
  57.8 s, 1080x1920, 25 fps, 8,610 likes. Local copy at
  `~/workspace/instagram_reel_DfKctoVs1uI/reel.mp4` — not pushed,
  for the same copyright / binary reasons as above.

## The short answer

The "technology" is not one model. It is a pipeline:

1. **Transcribe** the voice with Whisper (word-level timestamps).
2. **Plan the edit in code** — Claude Code writes / edits a Remotion
   (React) project, or an FFmpeg / HTML overlay script, choosing a
   caption style, effect, and layer per word / phrase.
3. **Track the person** — face / person segmentation per frame, so text
   can go *behind* the head, or be masked around them.
4. **Render effects as code** — captions, background replacement, colour
   grade, wall-light, glass, neon — as CSS / canvas / FFmpeg filters,
   not as a timeline you drag by hand.
5. **Review in a storyboard / caption-editor UI** — check frames, keep /
   tweak / cut each effect, then render the final MP4.

That is why the claim "1 plugin · 1 hour" is plausible: the plugin is a
library of pre-written effects + prompts ("the brain to know where to
place them"), Claude does the fiddly per-word timing, and the human
approves frames.

## Free, public starting points (MIT, by the same creator)

These are *not* Hop Studio itself — the creator says so in their READMEs —
but they are the free starter versions of the same ideas:

- 7 free caption styles: https://github.com/Vibha-Ramprakash/claude-caption-styles
  `git clone https://github.com/Vibha-Ramprakash/claude-caption-styles ~/.claude/skills/captions`
  then in Claude Code: `/captions pop-sticker`
- 51 free video effects: https://github.com/Vibha-Ramprakash/claude-video-effects
  `git clone https://github.com/Vibha-Ramprakash/claude-video-effects ~/.claude/skills/effects`
  then: `/effects orbit from 3 to 6 seconds`
- Hop Studio itself: https://www.vibha.is/ai-video-studio
  220+ video effects, 47 caption styles, 190+ sound effects, 50+ templates.
  Paid, one payment, needs a paid Claude plan. Early bird closed 26 Nov 2026.

Related open pieces named in the creator's other posts:
Remotion (official Claude Code plugin), HyperFrames (HTML captions /
title cards), `/watch` (analyse reels for cuts / zooms / captions),
`earshot` (pick SFX, check timing, measure LUFS).

## Honest limits

- Full spoken transcript: **not verified**. No local Whisper model was
  available in this environment (`faster-whisper` not installed, no model
  in `~/workspace/models/`), so the transcript in `ANALYSIS.md` is
  reconstructed from the on-screen captions visible in the frames.
  Do not quote it as a verbatim ASR transcript.
- Hop Studio is a paid, closed plugin. Its exact prompts, effect code,
  and sound library cannot be recovered from a 37-second promo video,
  and were not attempted to be.
- Cost / paywall: several commenters asked whether it works on Claude's
  free tier and whether payment is required. The creator's pages say a
  paid Claude plan is needed, billed separately from the one-time Studio
  purchase.

## Run the reproduction

See `REPRODUCTION.md`, then:

```bash
python3 reproduce/transcribe.py your-clip.mp4 --out words.json
python3 reproduce/caption_overlay.py your-clip.mp4 words.json --style liquid-glass --out your-clip_edited.mp4
```

Requires: ffmpeg, Python 3, `faster-whisper` (or `whisper.cpp`) for
transcription, Pillow / OpenCV for the mask demo.
