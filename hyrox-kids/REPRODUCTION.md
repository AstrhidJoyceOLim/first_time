# HYROX for kids — how to reproduce this promo

An original reproduction plan, based on the HYROX Youngstars reel
analysed in `ANALYSIS.md`. Do not re-upload HYROX's video, copy
their footage, or use their branding without permission. Film your
own event, with your own children / families, and use this as a
shot-list and edit template.

## 1. The template (58 seconds)

Copy this chapter order. It is the whole structure.

| # | Chapter | Length | Shots you need |
|---|---|---|---|
| 1 | RACE DAY | 0–3s | Wide: family walking under the entrance arch, backs to camera. |
| 2 | REGISTRATION | 3–7s | Close: wristband on, number on arm, shoes. |
| 3 | SIGN PREP | 7–9s | Table: child + family making a supporter sign. |
| 4 | WARM UP | 9–18s | Lunges, high-five, group line-up, plank, run drills. |
| 5 | RACE — start | 19–24s | Line-up, start signal, first run. |
| 6 | RACE — stations | 25–35s | 3–4 stations, 1 shot each: SkiErg / rower, sled push, farmer's carry, medicine-ball squat. |
| 7 | HYDRATION BREAK | 31–33s | Drink, breather, smile — a pause in the middle. |
| 8 | BACK INTO IT | 33–35s | Rower / carry, back to work. |
| 9 | FINISH | 44–49s | Finish arch, tired-but-happy face, hug from a parent. |
| 10 | CHECK OUT | 50–53s | Staff check wristband at the exit pillars. |
| 11 | ADD TO THE COLLECTION | 53–55s | Close-up: hands adding a finisher patch / medal to a bag. |
| 12 | HOME TIME | 56–58s | Family walking away together, backs to camera. |

Total: 12 chapters, ~50 shots, 1–2s per shot.

## 2. Filming checklist

- **Camera:** phone in 9:16, 1080x1920, 25 or 30 fps, or a camera
  with the same framing. Shoot at the child's eye level, not from
  adult height. Follow from behind for arrival / home time.
- **Close-ups to get on the day (these carry the film):** shoes,
  wristband, number on arm, hands on equipment, patch, sign,
  parent's hug. Get each one — they are 1 second each in the edit.
- **Wide shots:** entrance arch, finish arch, group warm-up,
  arena. One wide per chapter is enough.
- **Stations:** film each station once, side-on, 3–5 seconds of
  usable footage. You only need 1–2 seconds in the cut.
- **Sound on set:** record clean ambient sound (crowd, feet,
  equipment). You will lay music over it, but keep the natural
  sound low under the music at the finish hug.
- **Do not film:** other children without their parent's consent,
  changing areas, results boards with full names, or any child
  who looks distressed. If in doubt, do not use the shot.

## 3. Edit recipe

- **Software:** CapCut / Premiere / DaVinci, or Remotion if you
  want the edit as code (see the main `REPRODUCTION.md` in this
  repo for the Claude + Remotion route).
- **Titles:** plain white sans-serif capitals, centred, e.g.
  `RACE DAY`, `WARM UP`, `FINISH`. No fancy fonts. Hold each
  title for 2–4 seconds while 2–3 shots play under it.
- **Cutting:** cut on the beat. 1–2s per shot, no shot longer
  than 3s except the finish hug (let that breathe, 3–4s).
- **Grade:** lift blacks slightly, warm the skin, saturate your
  brand colour (in the original: purple). Keep it consistent
  across all shots — shoot a colour card if you can.
- **Music:** one upbeat, licenced track for the whole 58s.
  No voiceover. Let the finish land on a musical lift.
- **Export:** 1080x1920, H.264, 25 fps, with captions / chapter
  titles burned in (not as a separate subtitle file, so they
  survive Instagram re-uploads).

## 4. The Claude / AI version (optional)

If you want the first reel's workflow applied to this one:

1. Transcribe any speech (there is none in the original — skip
   this if your version is music-only).
2. Write the chapter list above as a `plan.json`:
   `[{chapter, start, end, title, shots[]}]`.
3. In Claude Code / Remotion, make one component per chapter:
   title + shots + a close-up. Claude can assemble the timeline
   from the plan, you approve the check frames.
4. Use the caption / effect code in `../reproduce/` for titles
   and transitions, not for the children's footage itself.

## 5. Safeguarding — read this before you film kids

This matters more than the edit.

- Get **written consent from a parent / guardian for every child
  who is recognisable**, before you publish. Verbal is not enough.
- Use **first names only, if at all**. The original uses only
  "Laurence, 10-11". Do not publish surnames, schools, ages
  with dates of birth, or home locations.
- A parent should be present at filming, and should see the
  final cut before it is posted.
- Do not show a child crying, injured, or upset, even if it is
  "real". Cut it.
- Do not film in changing areas, toilets, or medical areas.
- Check your event / school / club's photo policy and HYROX's
  brand rules before using their name, logo, or "Youngstars"
  wording in your own promo. This template is for *your* event,
  with *your* branding, unless you have permission.
- If a parent withdraws consent after posting, take the video
  down. Keep a list of who consented, and when.

## 6. What to measure

The original got 8,610 likes / 70 comments on 39k followers
(about 22% like-to-follower, very high for a promo) — because
it is a story, not an advert. For your version, track:
saves, shares to parents, profile visits, and sign-ups from
the link in bio — not just likes. The patch / "collection"
idea is worth copying: a physical, collectable reason to
come back is stronger than a discount code.

## Files

- `ANALYSIS.md` — frame-by-frame breakdown of the original
- `frames_index.md` — per-second index (58 frames)
- `shot-list.md` — printable shot list for the day
