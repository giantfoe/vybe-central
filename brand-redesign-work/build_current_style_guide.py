from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path("/Users/ayorindejohn/Documents/VYBE_CENTRAL")
WORK = ROOT / "brand-redesign-work"
OUT_DIR = WORK / "current_style_guide_pages"
OUT_PDF = ROOT / "Vybe_Central_Brand_Guidelines_2026.pdf"
CONTACT = WORK / "current-style-guide-contact-sheet.png"

ASSET_DIR = ROOT / "public" / "assets"
LOGO = ASSET_DIR / "vibe-central-logo.png"
HERO = ASSET_DIR / "dark-studio-bg.png"
SESSION = ASSET_DIR / "hero-session.png"
STUDIO = ASSET_DIR / "studio-room.png"
ARTIST = ASSET_DIR / "artist-performance.png"

FONT_DIR = Path(
    "/Users/ayorindejohn/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/"
    "libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype"
)

W, H = 3200, 1800

BLACK = "#000000"
SOFT = "#0A0A0A"
PANEL = "#111111"
WHITE = "#FFFFFF"
TEXT_2 = "#A3A3A3"
TEXT_3 = "#666666"
LINE = "#2A2A2A"
PINK = "#FF4D85"
CYAN = "#00E5FF"
BLUE = "#304FFE"
GOLD = "#F5B43A"
GREEN = "#3E8E3E"
RED = "#D32F2F"


def rgb(hex_color):
    hex_color = hex_color.strip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def fnt(file_name, size):
    return ImageFont.truetype(str(FONT_DIR / file_name), size)


DISPLAY = "NotoSans-Bold.ttf"
DISPLAY_X = "DejaVuSansCondensed-Bold.ttf"
BODY = "NotoSans-Regular.ttf"
BODY_BOLD = "NotoSans-Bold.ttf"
MONO = "DejaVuSansMono.ttf"


def font(size, weight="regular", condensed=False):
    if condensed:
        return fnt(DISPLAY_X, size)
    if weight == "bold":
        return fnt(BODY_BOLD, size)
    return fnt(BODY, size)


def measure(draw, text, face):
    box = draw.textbbox((0, 0), text, font=face)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw, text, face, width):
    lines = []
    for block in text.split("\n"):
        words = block.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = f"{line} {word}"
            if measure(draw, trial, face)[0] <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_wrapped(draw, xy, text, face, fill, width, leading=1.25):
    x, y = xy
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=fill)
        y += int(face.size * leading)
    return y


def cover_crop(path, size, focus=(0.5, 0.5)):
    img = Image.open(path).convert("RGB")
    sw, sh = img.size
    tw, th = size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = int((nw - tw) * focus[0])
    top = int((nh - th) * focus[1])
    return img.crop((left, top, left + tw, top + th)).convert("RGBA")


def tint(img, color=BLACK, alpha=130):
    overlay = Image.new("RGBA", img.size, rgb(color) + (alpha,))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def base(bg=BLACK):
    img = Image.new("RGBA", (W, H), rgb(bg) + (255,))
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(120, W, 320):
        d.line((x, 0, x, H), fill=(255, 255, 255, 10), width=1)
    for y in range(120, H, 240):
        d.line((0, y, W, y), fill=(255, 255, 255, 8), width=1)
    return img, d


def blur_blob(img, center, radius, color, alpha=110):
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blob, "RGBA")
    x, y = center
    bd.ellipse((x - radius, y - radius, x + radius, y + radius), fill=rgb(color) + (alpha,))
    blob = blob.filter(ImageFilter.GaussianBlur(radius // 2))
    return Image.alpha_composite(img, blob)


def label(draw, x, y, text, color=PINK):
    draw.text((x, y), text.upper(), font=font(30, "bold"), fill=rgb(color) + (255,))
    draw.ellipse((x - 34, y + 9, x - 16, y + 27), fill=rgb(color) + (255,))


def header(draw, n, title="VYBE CENTRAL STYLE GUIDE"):
    draw.text((128, 72), title, font=font(28, "bold"), fill=rgb(TEXT_2) + (220,))
    draw.text((W - 245, 72), f"2026 / {n:02d}", font=fnt(MONO, 28), fill=rgb(TEXT_3) + (220,))


def paste_logo(img, box, shadow=True):
    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    x = box[0] + ((box[2] - box[0]) - logo.width) // 2
    y = box[1] + ((box[3] - box[1]) - logo.height) // 2
    if shadow:
        sh = Image.new("RGBA", logo.size, (0, 0, 0, 0))
        sh.putalpha(logo.getchannel("A").filter(ImageFilter.GaussianBlur(22)))
        img.alpha_composite(sh, (x + 24, y + 32))
    img.alpha_composite(logo, (x, y))


def card(draw, box, fill=PANEL, outline=LINE, radius=28, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=rgb(fill) + (255,), outline=rgb(outline) + (255,), width=width)


def big(draw, xy, text, size=180, fill=WHITE, width=None):
    face = font(size, "bold", condensed=True)
    if width:
        while measure(draw, text, face)[0] > width and size > 70:
            size -= 4
            face = font(size, "bold", condensed=True)
    draw.text(xy, text, font=face, fill=rgb(fill) + (255,))


def wave(draw, x, y, w, h, colors=(PINK, CYAN, GOLD), bars=16):
    gap = w / bars
    for i in range(bars):
        amp = (0.25 + 0.75 * abs(math.sin(i * 0.85))) * h
        bx = x + i * gap
        color = rgb(colors[i % len(colors)]) + (255,)
        draw.rounded_rectangle((bx, y + (h - amp) / 2, bx + gap * 0.35, y + (h + amp) / 2), radius=8, fill=color)


def footer_note(draw, text):
    draw.text((128, H - 108), text, font=font(28), fill=rgb(TEXT_3) + (255,))


def save(img, idx):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"page-{idx:02d}.png"
    img.convert("RGB").save(path, quality=95)
    return path


def cover():
    img, d = base(BLACK)
    bg = cover_crop(HERO, (W, H), focus=(0.5, 0.5))
    img.alpha_composite(tint(bg, BLACK, 70), (0, 0))
    img = blur_blob(img, (2550, 360), 420, PINK, 120)
    img = blur_blob(img, (720, 1320), 440, CYAN, 60)
    d = ImageDraw.Draw(img, "RGBA")
    header(d, 1)
    label(d, 170, 240, "current code-derived system", CYAN)
    big(d, (128, 365), "VYBE", 360, WHITE, 1450)
    big(d, (128, 660), "CENTRAL", 310, PINK, 1700)
    draw_wrapped(
        d,
        (145, 1050),
        "Style guide rebuilt from the current Svelte/CSS codebase: dark framed canvas, glass navigation, neon shader energy, artist discovery, community capture, and studio-platform positioning.",
        font(54, "bold"),
        rgb(WHITE) + (230,),
        1420,
        1.18,
    )
    paste_logo(img, (2320, 560, 3060, 1300))
    wave(d, 150, 1510, 560, 130)
    footer_note(d, "Generated from /src/App.svelte, /src/app.css, /src/lib, and /public/assets")
    return img


def overview():
    img, d = base(SOFT)
    header(d, 2)
    label(d, 170, 220, "brand overview")
    big(d, (128, 345), "CREATIVE ECOSYSTEM", 186, WHITE, 1850)
    draw_wrapped(
        d,
        (140, 575),
        "VYBE Central is a creative ecosystem where artists, producers, storytellers, and creators come together to create, collaborate, and be heard.",
        font(58, "bold"),
        rgb(TEXT_2) + (255,),
        1750,
        1.18,
    )
    panels = [
        ("MISSION", "Amplify African voices through studio production, live performance sessions, storytelling, and creative community.", PINK),
        ("PROMISE", "Professional creation space, culturally rooted storytelling, and visibility beyond the session.", CYAN),
        ("PERSONALITY", "Precise, cinematic, social, rooted, ambitious, modern, and built for repeat creative action.", GOLD),
    ]
    x = 140
    for title, body, color in panels:
        card(d, (x, 980, x + 900, 1458), PANEL, LINE, 20)
        d.text((x + 48, 1035), title, font=font(40, "bold"), fill=rgb(color) + (255,))
        draw_wrapped(d, (x + 48, 1110), body, font(40), rgb(TEXT_2) + (255,), 760, 1.28)
        x += 980
    side = cover_crop(ARTIST, (760, 760), focus=(0.52, 0.42))
    img.alpha_composite(tint(side, BLACK, 20), (2290, 185))
    d.rectangle((2290, 185, 3050, 945), outline=rgb(PINK) + (220,), width=4)
    footer_note(d, "Core line: Studio. Sessions. Community. Discovery.")
    return img


def logo_page():
    img, d = base(BLACK)
    header(d, 3)
    label(d, 170, 220, "logo system", GOLD)
    big(d, (128, 345), "THE MARK", 220, WHITE, 1400)
    draw_wrapped(
        d,
        (140, 620),
        "Use the circular microphone logo as the primary identity mark. Use /public/assets/vibe-central-logo.png as the production-ready transparent web logo.",
        font(40),
        rgb(TEXT_2) + (255,),
        1060,
        1.25,
    )
    paste_logo(img, (210, 880, 1040, 1710))
    placements = [(1340, 500, SOFT, "Dark UI"), (1940, 500, WHITE, "White"), (2540, 500, PINK, "Accent"), (1640, 1080, CYAN, "Signal"), (2240, 1080, GOLD, "Highlight")]
    for x, y, bg, name in placements:
        card(d, (x, y, x + 460, y + 360), bg, LINE, 16)
        paste_logo(img, (x + 82, y + 45, x + 378, y + 310), shadow=False)
        fg = BLACK if bg in [WHITE, CYAN, GOLD, PINK] else WHITE
        d.text((x + 36, y + 300), name.upper(), font=font(24, "bold"), fill=rgb(fg) + (220,))
    rules = [
        "Clear space: at least one microphone-width around the full badge.",
        "Do not crop, recolor, outline, or place over busy imagery without a dark overlay.",
        "Use the circular mark for nav, loading screen, cover surfaces, footer, and social avatars.",
    ]
    y = 1495
    for rule in rules:
        d.ellipse((1370, y + 12, 1388, y + 30), fill=rgb(PINK) + (255,))
        draw_wrapped(d, (1415, y), rule, font(30), rgb(TEXT_2) + (255,), 1360, 1.18)
        y += 70
    footer_note(d, "Asset source: public/assets/vibe-central-logo.png")
    return img


def color_page():
    img, d = base(BLACK)
    header(d, 4)
    label(d, 170, 220, "color tokens")
    big(d, (128, 345), "NEON ON BLACK", 200, WHITE, 1850)
    swatches = [
        ("Background", BLACK, "#000000", "Root canvas, body, hero frame"),
        ("Background Soft", SOFT, "#0A0A0A", "Marquee, cards, footer surfaces"),
        ("Background Accent", PANEL, "#111111", "Panels, process rows, hover states"),
        ("Text Primary", WHITE, "#FFFFFF", "Headings, active labels, buttons"),
        ("Text Secondary", TEXT_2, "#A3A3A3", "Body copy, descriptions"),
        ("Text Muted", TEXT_3, "#666666", "Captions and partner strip"),
        ("Accent Hot", PINK, "#FF4D85", "Primary brand signal and form focus"),
        ("Accent Blue", CYAN, "#00E5FF", "Process/open-call utility signal"),
        ("Accent Blue Dark", BLUE, "#304FFE", "Deep electric support color"),
        ("Accent Gold", GOLD, "#F5B43A", "Warm highlight, never dominant"),
    ]
    x0, y0 = 140, 670
    for i, (name, color, hexv, usage) in enumerate(swatches):
        col = i % 5
        row = i // 5
        x = x0 + col * 590
        y = y0 + row * 430
        d.rounded_rectangle((x, y, x + 500, y + 220), radius=26, fill=rgb(color) + (255,), outline=rgb(LINE) + (255,), width=2)
        fg = BLACK if color in [WHITE, CYAN, GOLD, PINK] else WHITE
        d.text((x + 32, y + 34), name.upper(), font=font(28, "bold"), fill=rgb(fg) + (255,))
        d.text((x + 32, y + 92), hexv, font=fnt(MONO, 27), fill=rgb(fg) + (220,))
        draw_wrapped(d, (x + 32, y + 250), usage, font(27), rgb(TEXT_2) + (255,), 430, 1.18)
    draw_wrapped(
        d,
        (150, 1580),
        "Ratio guidance: 70% black surfaces, 18% soft panels, 7% hot pink, 3% cyan, 2% gold. Pink and cyan should guide attention, not decorate every block.",
        font(40, "bold"),
        rgb(WHITE) + (230,),
        2600,
        1.2,
    )
    return img


def typography_page():
    img, d = base(SOFT)
    header(d, 5)
    label(d, 170, 220, "typography")
    big(d, (128, 335), "PLUS JAKARTA SANS", 178, WHITE, 1900)
    d.text((145, 570), "Fallback stack in code: Plus Jakarta Sans, Inter, system sans-serif.", font=font(40), fill=rgb(TEXT_2) + (255,))
    examples = [
        ("Hero giant", "Vybe®Central", "clamp(4rem, 15vw, 16rem) / 800 / -0.04em"),
        ("Hero headline", "CREATE. COLLABORATE. BE HEARD.", "clamp(2rem, 4.5vw, 4rem) / 800 / uppercase"),
        ("Section heading", "Discover Artists", "clamp(2.5rem, 4.5vw, 4.5rem) / 800 / -0.05em"),
        ("Body copy", "Professional creation space, culturally rooted storytelling, and visibility beyond the session.", "1.05rem / 1.6 / text-secondary"),
    ]
    y = 765
    for role, sample, spec in examples:
        d.text((145, y), role.upper(), font=font(24, "bold"), fill=rgb(PINK) + (255,))
        size = 86 if role != "Body copy" else 38
        face = font(size, "bold" if role != "Body copy" else "regular", condensed=False)
        draw_wrapped(d, (145, y + 55), sample, face, rgb(WHITE) + (255,), 1880, 1.1)
        d.text((2150, y + 70), spec, font=fnt(MONO, 27), fill=rgb(TEXT_2) + (255,))
        d.line((145, y + 245, 3040, y + 245), fill=rgb(LINE) + (255,), width=2)
        y += 280
    footer_note(d, "Rule: oversized type is for hero and section identity only; compact panels use restrained sizes.")
    return img


def layout_page():
    img, d = base(BLACK)
    header(d, 6)
    label(d, 170, 220, "layout language", CYAN)
    big(d, (128, 345), "FRAMED DARK CANVAS", 184, WHITE, 1960)
    draw_wrapped(d, (145, 590), "The app uses a black page background with a bordered, rounded app container. Most sections are full-width bands with 4% side padding, 8rem vertical rhythm, and one-pixel grid borders.", font(42), rgb(TEXT_2) + (255,), 1800, 1.24)
    d.rounded_rectangle((170, 860, 3030, 1510), radius=56, fill=rgb(BLACK) + (255,), outline=rgb("#333333") + (255,), width=4)
    d.rounded_rectangle((260, 940, 2940, 1450), radius=80, fill=(255, 255, 255, 24), outline=(255, 255, 255, 42), width=3)
    d.text((360, 1018), "glass nav pill", font=font(36, "bold"), fill=rgb(WHITE) + (255,))
    d.rectangle((360, 1140, 1260, 1390), fill=rgb(PANEL) + (255,), outline=rgb(LINE) + (255,))
    d.rectangle((1320, 1140, 2200, 1390), fill=rgb(PANEL) + (255,), outline=rgb(LINE) + (255,))
    d.rectangle((2260, 1140, 2820, 1390), fill=rgb(PANEL) + (255,), outline=rgb(LINE) + (255,))
    d.text((392, 1220), "content left", font=font(32), fill=rgb(TEXT_2) + (255,))
    d.text((1352, 1220), "feature grid", font=font(32), fill=rgb(TEXT_2) + (255,))
    d.text((2292, 1220), "action panel", font=font(32), fill=rgb(TEXT_2) + (255,))
    notes = [
        "Desktop: use multi-column grids for portfolio, stats, capabilities, FAQ, and contact split.",
        "Mobile: collapse to one column below 860px; app radius changes from 20px to 12px.",
        "Border system: use 1px rgba white lines and 1px gaps between cards.",
    ]
    y = 1585
    for note in notes:
        d.ellipse((178, y + 14, 196, y + 32), fill=rgb(CYAN) + (255,))
        draw_wrapped(d, (225, y), note, font(30), rgb(TEXT_2) + (255,), 2600, 1.2)
        y += 70
    return img


def component_page():
    img, d = base(SOFT)
    header(d, 7)
    label(d, 170, 220, "component system", PINK)
    big(d, (128, 345), "UI PATTERNS", 208, WHITE, 1560)
    blocks = [
        ("Glass Nav", "Rounded 40px nav pill, 0.1 white background, 12px blur, uppercase links.", PINK),
        ("Portfolio Card", "Image crop, dark panel meta, category/date row, hover image scale.", CYAN),
        ("Stats Card", "Icon in hot pink, huge number, uppercase label, centered panel.", GOLD),
        ("Form Field", "Dark input, 1px line border, 8px radius, hot-pink focus ring.", PINK),
        ("FAQ Row", "Monospace number, large question, plus/minus toggle, hairline divider.", CYAN),
        ("CTA Button", "White-on-black or black-on-white default; pink hover for active action.", GOLD),
    ]
    x0, y0 = 140, 710
    for i, (title, body, color) in enumerate(blocks):
        x = x0 + (i % 3) * 990
        y = y0 + (i // 3) * 430
        card(d, (x, y, x + 900, y + 320), PANEL, LINE, 22)
        d.text((x + 42, y + 40), f"[0{i+1}]", font=fnt(MONO, 32), fill=rgb(color) + (255,))
        d.text((x + 42, y + 98), title, font=font(46, "bold"), fill=rgb(WHITE) + (255,))
        draw_wrapped(d, (x + 42, y + 170), body, font(30), rgb(TEXT_2) + (255,), 750, 1.2)
    footer_note(d, "Source classes: .ora-nav-pill, .portfolio-card, .achievement-card, .contact-form-column, .faq-item-btn.")
    return img


def imagery_page():
    img, d = base(BLACK)
    header(d, 8)
    label(d, 170, 220, "imagery")
    big(d, (128, 345), "STUDIO REALISM", 210, WHITE, 1700)
    shots = [(SESSION, (145, 650, 1175, 1315), (0.58, 0.5)), (STUDIO, (1260, 650, 2050, 1315), (0.5, 0.5)), (ARTIST, (2135, 650, 3040, 1315), (0.52, 0.42))]
    for path, box, focus in shots:
        crop = cover_crop(path, (box[2] - box[0], box[3] - box[1]), focus)
        img.alpha_composite(crop, (box[0], box[1]))
        d.rectangle(box, outline=rgb(LINE) + (255,), width=3)
    rules = [
        "Show real creation: microphones, cameras, artists, producers, live rooms, control rooms.",
        "Grade imagery dark, high contrast, and warm enough to support black/pink/cyan UI.",
        "Avoid generic stock lifestyle. Every image should communicate performance, recording, or discovery.",
    ]
    y = 1455
    for rule in rules:
        d.ellipse((158, y + 14, 178, y + 34), fill=rgb(PINK) + (255,))
        draw_wrapped(d, (210, y), rule, font(36), rgb(TEXT_2) + (255,), 2600, 1.2)
        y += 84
    return img


def motion_page():
    img, d = base(SOFT)
    header(d, 9)
    label(d, 170, 220, "motion and shaders", CYAN)
    big(d, (128, 345), "ADVANCED BUT CONTROLLED", 178, WHITE, 2200)
    modules = [
        ("Loading Screen", "Initial brand reveal before the app fades in: opacity, translateY, scale."),
        ("SVG Shader", "High-quality animated neon studio backdrop in the hero."),
        ("Lottie Waveform", "Equalizer waveform for audio identity and section energy."),
        ("Lottie Record", "Rotating mark in footer and brand moments."),
        ("Marquee", "Partner/talent loop at 35s linear, background-soft surface."),
        ("Hover Motion", "Portfolio image scale, buttons scale, line/color transitions."),
    ]
    x0, y0 = 145, 720
    for i, (title, body) in enumerate(modules):
        x = x0 + (i % 2) * 1460
        y = y0 + (i // 2) * 275
        d.line((x, y - 30, x + 1250, y - 30), fill=rgb(LINE) + (255,), width=2)
        d.text((x, y), f"0{i+1}", font=fnt(MONO, 32), fill=rgb(CYAN) + (255,))
        d.text((x + 110, y - 4), title, font=font(46, "bold"), fill=rgb(WHITE) + (255,))
        draw_wrapped(d, (x + 110, y + 68), body, font(30), rgb(TEXT_2) + (255,), 1060, 1.2)
    wave(d, 160, 1550, 900, 140, (PINK, CYAN, GOLD), 24)
    d.text((1180, 1578), "Reduced motion: disable smooth scroll and shorten animations.", font=font(36, "bold"), fill=rgb(TEXT_2) + (255,))
    return img


def pages_map():
    img, d = base(BLACK)
    header(d, 10)
    label(d, 170, 220, "website structure", GOLD)
    big(d, (128, 345), "SITE MAP", 230, WHITE, 1200)
    items = [
        ("Home", "#top", "Ora-inspired hero, shader, nav pill, studio/service signal."),
        ("Create", "#create", "Why VYBE Central capabilities and platform proof."),
        ("Join", "#join", "Community capture form: email + WhatsApp."),
        ("Calls", "#calls", "Background vocalists, session musicians, hosts, producers."),
        ("Discover", "#discover", "Artist cards with profile direction and performance context."),
    ]
    y = 705
    for i, (name, href, body) in enumerate(items, start=1):
        d.text((150, y), f"[0{i}]", font=fnt(MONO, 42), fill=rgb(PINK) + (255,))
        d.text((330, y - 10), name, font=font(66, "bold"), fill=rgb(WHITE) + (255,))
        d.text((900, y + 6), href, font=fnt(MONO, 34), fill=rgb(CYAN) + (255,))
        draw_wrapped(d, (1240, y + 2), body, font(34), rgb(TEXT_2) + (255,), 1400, 1.18)
        d.line((145, y + 128, 3040, y + 128), fill=rgb(LINE) + (255,), width=2)
        y += 170
    footer_note(d, "Navigation labels from src/App.svelte navItems.")
    return img


def voice_page():
    img, d = base(SOFT)
    header(d, 11)
    label(d, 170, 220, "voice and copy")
    big(d, (128, 345), "DIRECT. CULTURAL. ACTIVE.", 160, WHITE, 2240)
    dos = [
        "Use action verbs: create, capture, join, discover, amplify.",
        "Keep claims grounded in studio, sessions, community, and platform outcomes.",
        "Use VYBE in brand/title moments and Vybe Central in sentence copy where readability matters.",
        "Talk about African voices and Sierra Leonean talent with specificity and respect.",
    ]
    donts = [
        "Do not sound like a generic agency template.",
        "Do not overuse hype words without proof.",
        "Do not make the studio feel exclusive or gatekept.",
        "Do not bury the email/WhatsApp community action.",
    ]
    for x, title, arr, color in [(150, "DO", dos, CYAN), (1710, "AVOID", donts, PINK)]:
        d.text((x, 720), title, font=font(78, "bold"), fill=rgb(color) + (255,))
        y = 860
        for item in arr:
            d.ellipse((x + 8, y + 16, x + 28, y + 36), fill=rgb(color) + (255,))
            draw_wrapped(d, (x + 60, y), item, font(38), rgb(TEXT_2) + (255,), 1180, 1.2)
            y += 125
    return img


def usage_page():
    img, d = base(BLACK)
    header(d, 12)
    label(d, 170, 220, "final system")
    big(d, (128, 345), "SHIP RULES", 230, WHITE, 1300)
    rules = [
        ("01", "Lead with the dark framed canvas and studio energy."),
        ("02", "Use hot pink as the main interactive signal; cyan for process and system cues."),
        ("03", "Keep cards square or lightly rounded. Avoid decorative nested-card layouts."),
        ("04", "Every artist card must include image, role/category, summary, and path to video/profile."),
        ("05", "Every community CTA must capture email and WhatsApp with clear success/error state."),
        ("06", "Keep motion subtle, brand-led, and non-blocking."),
    ]
    y = 710
    for num, text in rules:
        d.text((165, y), num, font=fnt(MONO, 44), fill=rgb(CYAN) + (255,))
        draw_wrapped(d, (330, y - 8), text, font(52, "bold"), rgb(WHITE) + (255,), 2300, 1.1)
        d.line((150, y + 100, 3040, y + 100), fill=rgb(LINE) + (255,), width=2)
        y += 150
    paste_logo(img, (2380, 180, 3040, 840))
    wave(d, 2100, 1390, 760, 150)
    footer_note(d, "This PDF replaces the previous guide and reflects the current codebase as of June 11, 2026.")
    return img


def build():
    pages = [
        cover(),
        overview(),
        logo_page(),
        color_page(),
        typography_page(),
        layout_page(),
        component_page(),
        imagery_page(),
        motion_page(),
        pages_map(),
        voice_page(),
        usage_page(),
    ]
    paths = [save(page, i + 1) for i, page in enumerate(pages)]
    rgb_pages = [Image.open(path).convert("RGB") for path in paths]
    rgb_pages[0].save(OUT_PDF, save_all=True, append_images=rgb_pages[1:], resolution=160.0)

    thumb_w, thumb_h = 640, 360
    sheet = Image.new("RGB", (thumb_w * 3, thumb_h * 4), rgb(BLACK))
    for i, page in enumerate(rgb_pages):
        thumb = page.copy()
        thumb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = (i % 3) * thumb_w
        y = (i // 3) * thumb_h
        sheet.paste(thumb, (x, y))
    sheet.save(CONTACT, quality=95)
    print(OUT_PDF)
    print(CONTACT)


if __name__ == "__main__":
    build()
