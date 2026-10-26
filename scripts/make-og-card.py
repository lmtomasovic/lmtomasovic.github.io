"""Rebuild assets/og-card.png, the preview image shown when the site is shared.

Run this after changing the name, tagline or headshot. Nothing else uses it,
and the site works fine without running it, as long as the card already exists.

    pip install Pillow
    python3 scripts/make-og-card.py

Fonts are downloaded once into a cache folder beside this script, so the first
run needs the internet and later runs do not.
"""

import pathlib
import urllib.request

from PIL import Image, ImageDraw, ImageFont

SITE = pathlib.Path(__file__).resolve().parent.parent
CACHE = pathlib.Path(__file__).resolve().parent / ".font-cache"

# Text shown on the card. Keep these in step with index.html.
NAME = "Luke Tomasovic"
TAGLINE = "MD-PhD candidate at Johns Hopkins"
URL = "luketomasovic.com"

# 1200x630 is what LinkedIn, X and Slack want. Drawing at 3x and shrinking
# at the end is what keeps the text from looking ragged.
W, H, SCALE = 1200, 630, 3

# These match the light-mode tokens at the top of assets/style.css.
BG, FG, MUTED, ACCENT, LINE = "#fbfcfd", "#1b2430", "#5d6a79", "#4292c6", "#e2e7ed"

FONT_URLS = {
    "Figtree.ttf": "https://github.com/google/fonts/raw/main/ofl/figtree/Figtree%5Bwght%5D.ttf",
    "JetBrainsMono.ttf": "https://github.com/google/fonts/raw/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}


def load_font(filename, size, weight):
    CACHE.mkdir(exist_ok=True)
    path = CACHE / filename
    if not path.exists():
        print(f"downloading {filename}...")
        urllib.request.urlretrieve(FONT_URLS[filename], path)
    f = ImageFont.truetype(path, size * SCALE)
    # Both files are variable fonts, so the weight is an axis rather than a
    # separate file. Older FreeType builds cannot set it; the default is close.
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def main():
    name_f = load_font("Figtree.ttf", 76, 600)
    tag_f = load_font("JetBrainsMono.ttf", 29, 400)
    url_f = load_font("JetBrainsMono.ttf", 25, 500)

    img = Image.new("RGB", (W * SCALE, H * SCALE), BG)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 10 * SCALE, H * SCALE], fill=ACCENT)

    pad = 96 * SCALE
    av = 188 * SCALE
    av_x = pad
    av_y = (H * SCALE - av) // 2 - 28 * SCALE

    photo = Image.open(SITE / "assets" / "photo.jpg").convert("RGB")
    photo = photo.resize((av, av), Image.LANCZOS)
    mask = Image.new("L", (av, av), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, av, av], fill=255)
    img.paste(photo, (av_x, av_y), mask)
    d.ellipse([av_x, av_y, av_x + av, av_y + av], outline=LINE, width=2 * SCALE)

    tx = av_x + av + 56 * SCALE
    d.text((tx, av_y + 22 * SCALE), NAME, font=name_f, fill=FG)
    d.text((tx, av_y + 126 * SCALE), TAGLINE, font=tag_f, fill=MUTED)

    rule_y = av_y + av + 52 * SCALE
    d.line([tx, rule_y, W * SCALE - pad, rule_y], fill=LINE, width=2 * SCALE)
    d.text((tx, rule_y + 26 * SCALE), URL, font=url_f, fill=ACCENT)

    out = SITE / "assets" / "og-card.png"
    img.resize((W, H), Image.LANCZOS).save(out, optimize=True)
    print(f"wrote {out.relative_to(SITE)}")


if __name__ == "__main__":
    main()
