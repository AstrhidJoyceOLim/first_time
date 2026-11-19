"""Pillow helpers for the caption styles observed in the reel.

These are original implementations of *looks*, not copies of any
plugin code. Use them to render one word as a PNG with transparency,
then composite it over a video frame with FFmpeg `overlay`, or in
OpenCV / Remotion.

- pop_sticker: bold text, thick outline, white on dark
- neon: text + multi-pass glow
- liquid_glass: large translucent text with a bright top edge
- arc_text: letters placed on a circular arc (the curved captions
  in frame 003: "even come / of these captions")
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def _font(size, bold=True):
    # DejaVu Sans is bundled with most Linux Pillow installs.
    # Replace with any bold TTF you have, e.g. Arial Black.
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def pop_sticker(text, size=120, fill="white", outline="black", stroke=8):
    font = _font(size)
    # Measure with a dummy draw.
    tmp = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(tmp)
    bbox = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
    w, h = bbox[2] - bbox[0] + 20, bbox[3] - bbox[1] + 20
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((10 - bbox[0], 10 - bbox[1]), text, font=font, fill=fill,
           stroke_width=stroke, stroke_fill=outline)
    return img


def neon(text, size=120, colour=(255, 230, 0, 255)):
    """Yellow neon: solid core + three blurred glow passes."""
    font = _font(size)
    tmp = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(tmp)
    bbox = d.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0] + 80, bbox[3] - bbox[1] + 80
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.text((40 - bbox[0], 40 - bbox[1]), text, font=font, fill=colour)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for blur in (24, 12, 4):
        out = Image.alpha_composite(out, glow.filter(ImageFilter.GaussianBlur(blur)))
    d = ImageDraw.Draw(out)
    d.text((40 - bbox[0], 40 - bbox[1]), text, font=font, fill=(255, 255, 255, 255))
    return out


def liquid_glass(text, size=200):
    """Translucent bubble letters: low-opacity fill, bright top edge."""
    font = _font(size)
    tmp = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(tmp)
    bbox = d.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0] + 40, bbox[3] - bbox[1] + 40
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Soft shadow / refraction halo
    d.text((20 - bbox[0], 20 - bbox[1]), text, font=font,
           fill=(255, 255, 255, 60), stroke_width=6,
           stroke_fill=(255, 255, 255, 40))
    img = img.filter(ImageFilter.GaussianBlur(2))
    d = ImageDraw.Draw(img)
    d.text((20 - bbox[0], 20 - bbox[1]), text, font=font,
           fill=(255, 255, 255, 140))
    # Bright top edge: draw again offset by -2 px in near-white.
    d.text((20 - bbox[0], 18 - bbox[1]), text, font=font,
           fill=(255, 255, 255, 90))
    return img


def arc_text(text, size=90, radius=500, fill="white"):
    """Place each letter on a circular arc, like the reel's curved captions."""
    font = _font(size)
    # Rough per-letter width; good enough for a demo, tune per font.
    import math
    total_angle = 0.0
    letters = []
    for ch in text:
        w = font.getlength(ch)
        angle = w / radius  # radians
        letters.append((ch, w, angle))
        total_angle += angle
    width = int(2 * radius * math.sin(total_angle / 2)) + size
    height = int(radius - radius * math.cos(total_angle / 2)) + size * 2
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = width // 2, height - size
    angle = -total_angle / 2
    for ch, w, a in letters:
        # Position on the arc, rotate the letter to be tangent.
        x = cx + radius * math.sin(angle + a / 2)
        y = cy - radius * math.cos(angle + a / 2)
        letter = Image.new("RGBA", (int(w) + 10, size + 10), (0, 0, 0, 0))
        ld = ImageDraw.Draw(letter)
        ld.text((5, 5), ch, font=font, fill=fill)
        deg = math.degrees(angle + a / 2)
        letter = letter.rotate(-deg, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(letter, (int(x - letter.width / 2),
                                     int(y - letter.height / 2)))
        angle += a
    return img


if __name__ == "__main__":
    pop_sticker("switch").save("/tmp/pop.png")
    neon("CAPTIONS").save("/tmp/neon.png")
    liquid_glass("glass").save("/tmp/glass.png")
    arc_text("even come").save("/tmp/arc.png")
    print("Wrote /tmp/pop.png /tmp/neon.png /tmp/glass.png /tmp/arc.png")
