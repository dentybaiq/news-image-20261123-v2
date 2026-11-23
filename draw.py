#!/usr/bin/env python3
"""news-image-20261123 v2 — one-day world news front page, Monday 23 November 2026.

Draws a single 1024x1024 newspaper front page with PIL: a navy top bar and
serif masthead naming the day, a number strip, region tabs sized by story
count, a UTC timeline, three illustrated hero stories, ten illustrated
cards, a schematic world map with numbered pins, a numbered list of 22 more
stories, a DATE CHECK box naming stories left out because they happened on
other days, and a certainty-tags legend. 35 dated stories in all, every one
from Monday 23 November 2026.

The layout follows the shape the best-ranked one-day pages share (masthead,
numbers, tabs, timeline, illustrated heroes, illustrated cards, map,
also-list, date check), but every line of code, every scene and every
wording here is written fresh for this entry.

Run:  python3 draw.py            (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 230)
INK = (24, 24, 24)
NAVY = (18, 36, 70)
NAVY2 = (30, 54, 98)
RED = (170, 32, 36)
RED_DK = (128, 22, 26)
GOLD = (198, 160, 40)
GREEN = (28, 104, 56)
TEAL = (14, 92, 90)
ORANGE = (176, 90, 0)
PURPLE = (88, 56, 138)
GREY = (96, 94, 88)
RULE = (198, 188, 166)
CARD = (255, 253, 246)
NIGHT = (12, 26, 56)

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype/noto/"
SERIF_B = os.path.join(FD, "NotoSerif-Bold.ttf")
SERIF_I = os.path.join(FD, "NotoSerif-Italic.ttf")
SANS = os.path.join(FD, "NotoSans-Regular.ttf")
SANS_B = os.path.join(FD, "NotoSans-Bold.ttf")
SANS_I = os.path.join(FD, "NotoSans-Italic.ttf")


def load_font(path, size):
    return ImageFont.truetype(path, size)


def fit_text(text, font, width):
    """Greedy word wrap to a pixel width; returns the lines that fit."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def clip_line(text, font, width):
    """Shorten one line with an ellipsis until it fits the width."""
    if font.getlength(text) <= width:
        return text
    while text and font.getlength(text + "…") > width:
        text = text[:-1].strip()
    return text + "…"


def blurb(d, x, y, text, font, fill, width, leading, limit=None):
    """Draw wrapped text; returns the y below the last line drawn."""
    lines = fit_text(text, font, width)
    if limit is not None:
        lines = lines[:limit]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def tag_chip(d, x, y, label, bg, size=9):
    """Small filled certainty tag; returns the x just past the chip."""
    f = load_font(SANS_B, size)
    w = int(f.getlength(label)) + 10
    h = size + 7
    d.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=bg)
    d.text((x + 5, y + 3), label, font=f, fill=(255, 255, 255))
    return x + w


# ---------------------------------------------------------------- stories
# Certainty of the claim as printed on the page.
TAG_FILL = {
    "CONFIRMED": GREEN,
    "REPORTED": NAVY,
    "CLAIM": ORANGE,
    "ONGOING": RED_DK,
    "PENDING": GREY,
}

REGION_FILL = {
    "EUROPE": NAVY,
    "MIDDLE EAST": RED_DK,
    "ASIA-PACIFIC": TEAL,
    "AMERICAS": GREEN,
    "AFRICA": ORANGE,
    "OCEANIA": PURPLE,
    "WORLD": GREY,
}

HEROES = [
    {
        "n": 1, "tag": "ONGOING", "place": "DYMER, UKRAINE",
        "region": "EUROPE", "beat": "EUROPE · WAR", "art": "dymer",
        "head": "Dymer toll rises to 11 as boy, 7, is pulled alive after 14 hours",
        "body": ("A drone hit a five-storey block at 05:00 on Sunday; Kyiv region "
                 "mourns on Monday as 14 are killed across the region."),
        "src": "Reuters · Al Jazeera · Kyiv officials",
    },
    {
        "n": 2, "tag": "CONFIRMED", "place": "ANTALYA, TÜRKIYE",
        "region": "WORLD", "beat": "WORLD · CLIMATE", "art": "cop31",
        "head": "COP31 ends with no deal — the first failure since 2009",
        "body": ("The EU rejects a text with no fossil fuels; Bowen faces "
                 "resignation calls as Pacific nations say they were let down."),
        "src": "Reuters · AAP",
    },
    {
        "n": 3, "tag": "CONFIRMED", "place": "BENGHAZI, LIBYA",
        "region": "AFRICA", "beat": "AFRICA · NAVAL", "art": "merkury",
        "head": "Zelenskyy confirms: Ukraine sank Russian corvette off Libya",
        "body": ("Seven sea drones sank the Merkury and hit the MV Angara; "
                 "10 injured and a Ka-27 helicopter destroyed."),
        "src": "Reuters · CNN · Zelenskyy",
    },
]

CARDS = [
    {"n": 4, "tag": "CONFIRMED", "place": "WASHINGTON", "region": "AMERICAS",
     "beat": "AMERICAS · POLITICS", "art": "capitol",
     "head": "Democrats win 258 House seats — biggest since 1992",
     "body": "Foxx concedes after a recount confirms Hubbard's 330-vote win in "
             "North Carolina.", "src": "AP · CNN"},
    {"n": 5, "tag": "CONFIRMED", "place": "CIKANDE, INDONESIA", "region": "ASIA-PACIFIC",
     "beat": "ASIA-PACIFIC · FIRE", "art": "factory",
     "head": "Banten fire: 24 confirmed dead, ~30 still missing",
     "body": "Search resumes Monday; DNA tests to identify the remains may take "
             "weeks.", "src": "Reuters · Guardian"},
    {"n": 6, "tag": "CONFIRMED", "place": "SEOUL", "region": "ASIA-PACIFIC",
     "beat": "ASIA-PACIFIC · MARKETS", "art": "market",
     "head": "Markets rebound as Seoul unveils $8bn fund",
     "body": "S&P futures +2.2%, Nasdaq +3% after Friday's rout; China cuts "
             "margin rules.", "src": "NordFX · Substack"},
    {"n": 7, "tag": "REPORTED", "place": "KHARTOUM", "region": "AFRICA",
     "beat": "AFRICA · WAR", "art": "khartoum",
     "head": "Drone strikes hit homes and a UN building in Khartoum",
     "body": "Sudan's army accuses Ethiopia of launching the attacks.",
     "src": "France 24"},
    {"n": 8, "tag": "REPORTED", "place": "GAZA", "region": "MIDDLE EAST",
     "beat": "MIDDLE EAST · HEALTH", "art": "gaza",
     "head": "Gaza 'toxic wasteland' threatens health for generations",
     "body": "Oxfam: contamination across 99% of the strip; 61m tonnes of debris.",
     "src": "Guardian · Al Jazeera"},
    {"n": 9, "tag": "CONFIRMED", "place": "BRUSSELS", "region": "EUROPE",
     "beat": "EUROPE · TRANSPORT", "art": "airport",
     "head": "Belgian airports shut as strike grounds flights",
     "body": "Air traffic controllers join a national anti-austerity strike.",
     "src": "OneTurn"},
    {"n": 10, "tag": "CONFIRMED", "place": "LONDON", "region": "EUROPE",
     "beat": "EUROPE · BUSINESS", "art": "capita",
     "head": "Capita shares plunge 67% as boss steps down",
     "body": "Chief executive Adolfo Hernandez leaves with immediate effect.",
     "src": "OneTurn"},
    {"n": 11, "tag": "CONFIRMED", "place": "MUMBAI", "region": "ASIA-PACIFIC",
     "beat": "ASIA-PACIFIC · BUSINESS", "art": "steel",
     "head": "Tata Steel buys $1.67bn stake in APL Apollo",
     "body": "A 26.4% stake in India's top steel pipe maker; APL shares fall.",
     "src": "OneTurn"},
    {"n": 12, "tag": "REPORTED", "place": "WASHINGTON", "region": "AMERICAS",
     "beat": "AMERICAS · ECONOMY", "art": "treasury",
     "head": "Bessent warns Fed hikes risk needless slowdown",
     "body": "Treasury chief pushes back as bets on a December hike build.",
     "src": "Substack"},
    {"n": 13, "tag": "REPORTED", "place": "BENGHAZI", "region": "AFRICA",
     "beat": "AFRICA · DIPLOMACY", "art": "un",
     "head": "Eastern Libya calls Merkury strike a sovereignty violation",
     "body": "It seeks a UN probe; Tripoli warns against dragging ports into war.",
     "src": "Al Jazeera · BBC"},
]

# (number, place, headline, source, tag, region) — the breadth list.
ALSO = [
    (14, "Kyiv", "Region mourns; 14 killed across Kyiv region", "Reuters", "CONFIRMED", "EUROPE"),
    (15, "Kyiv", "Zelenskyy urges US to approve Patriot interceptors", "Reuters", "REPORTED", "EUROPE"),
    (16, "Kyiv", "Russia fired 2,700 drones in a week", "Zelenskyy", "REPORTED", "EUROPE"),
    (17, "Beijing", "China signs 35% electrification goal for 2035", "AAP", "CONFIRMED", "ASIA-PACIFIC"),
    (18, "Canberra", "Australia–South Korea green deal survives flop", "AAP", "CONFIRMED", "OCEANIA"),
    (19, "Majuro", "Marshall Islands: 'let down on all sides'", "Reuters", "REPORTED", "OCEANIA"),
    (20, "St Paul", "Minnesota recount Nov 30; Louisiana runoffs Dec 12", "CNN", "CONFIRMED", "AMERICAS"),
    (21, "New York", "Ackman: US may enter recession if Fed hikes", "Morningstar", "REPORTED", "AMERICAS"),
    (22, "Seoul", "Kospi −3.3% despite fund; Taiex +2.4%", "NordFX", "CONFIRMED", "ASIA-PACIFIC"),
    (23, "Tokyo", "Japan closed for Labour Thanksgiving Day", "NordFX", "CONFIRMED", "ASIA-PACIFIC"),
    (24, "Frankfurt", "Germany booms as France stalls, PMIs show", "Morningstar", "REPORTED", "EUROPE"),
    (25, "Washington", "US flash PMI due 9:45 AM EST", "Substack", "PENDING", "AMERICAS"),
    (26, "Benghazi", "Eastern Libya seeks UN probe into strike", "Al Jazeera", "REPORTED", "AFRICA"),
    (27, "Helsinki", "Sparta II salvage under way; Finland leads", "TWZ", "REPORTED", "EUROPE"),
    (28, "Riyadh", "Houthis claim Saudi refinery strike", "NordFX", "CLAIM", "MIDDLE EAST"),
    (29, "Gulf", "Shipping attacks keep oil near $90", "NordFX", "REPORTED", "MIDDLE EAST"),
    (30, "Gaza", "61m tonnes of debris; 74,000+ killed", "Guardian", "REPORTED", "MIDDLE EAST"),
    (31, "Mumbai", "Nifty −1.1%; ASX 200 −0.3%, 8th loss in a row", "NordFX", "CONFIRMED", "ASIA-PACIFIC"),
    (32, "Beijing", "China cuts margin financing 100% to 80%", "Substack", "CONFIRMED", "ASIA-PACIFIC"),
    (33, "Taipei", "Taiwan tightens short-selling rules", "Substack", "CONFIRMED", "ASIA-PACIFIC"),
    (34, "London", "Gold $3,620; Bitcoin holds $60k", "NordFX", "CONFIRMED", "WORLD"),
    (35, "Washington", "US PCE due Wed; markets shut Thu", "NordFX", "PENDING", "AMERICAS"),
]

NUMBERS = [
    ("11", "Dymer toll on Monday"),
    ("258", "Democrats' House seats"),
    ("24", "confirmed dead in Banten"),
    ("$8bn", "Seoul stabilisation fund"),
    ("2,700", "Russian drones in a week"),
    ("35%", "China's 2035 power goal"),
]

TIMELINE = ("05:20 Dymer toll reaches 11  ·  11:17 Foxx concedes in N. Carolina  ·  "
            "12:15 US futures rally  ·  14:45 US flash PMI due  ·  Seoul fund "
            "steadies Asia  ·  Canberra blames Bowen")

DATE_CHECK = ("Left out because they happened on other days: Nikkei −5.06%, S&P −3.7% "
              "(Fri 20 Nov)  ·  Alcaraz wins ATP Finals (Sun)  ·  Hong Kong elects its "
              "Election Committee (Sun)  ·  Verstappen takes Las Vegas GP (Sun)  ·  "
              "India 720/9 in NZ (Sun)  ·  Peru quake (Fri)  ·  Russia's 400-drone "
              "barrage (Thu–Fri)  ·  'El Chapo Isidro' captured (Fri)  ·  EU–Indonesia "
              "deal signed (Sat)")

# pins on the schematic map: (number, x, y) in map-panel coordinates.
PINS = [(1, 150, 22), (2, 162, 36), (3, 150, 52), (4, 88, 32), (5, 240, 62),
        (6, 252, 30), (7, 158, 68), (8, 168, 42), (9, 136, 28), (10, 126, 10),
        (11, 210, 48), (12, 94, 42), (13, 158, 62)]


# ---------------------------------------------------------------- scenes
def sky_stars(d, x0, y0, pts):
    for (sx, sy, r) in pts:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + r, y0 + sy + r], fill=(255, 255, 255))


def art_dymer(d, x0, y0, x1, y1):
    """Night over Dymer: stars, a drone, a skyline, a collapsed block, smoke."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=NIGHT)
    sky_stars(d, x0, y0, [(18, 8, 2), (70, 6, 2), (140, 12, 2), (210, 8, 3),
                          (270, 14, 2), (110, 22, 2), (240, 26, 2)])
    d.ellipse([x0 + w - 44, y0 + 6, x0 + w - 20, y0 + 30], fill=(238, 234, 208))
    # drone: dark diamond with a lit dot
    dx, dy = x0 + 150, y0 + 20
    d.polygon([(dx, dy - 6), (dx + 7, dy), (dx, dy + 6), (dx - 7, dy)], fill=(8, 8, 12))
    d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 220, 100))
    # skyline with lit windows
    for (bx, bw, bh) in [(6, 44, 40), (56, 32, 54), (94, 50, 36), (150, 28, 48),
                         (184, 54, 42), (244, 38, 56)]:
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(15, 20, 42))
        for wy in range(y1 - bh + 8, y1 - 6, 12):
            for wx in range(x0 + bx + 6, x0 + bx + bw - 6, 12):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 5, wy + 6], fill=(247, 215, 116))
    # collapsed block, tilted, with smoke curls
    d.polygon([(x0 + 256, y1 - 28), (x0 + 288, y1 - 36), (x0 + 294, y1 - 6),
               (x0 + 262, y1)], fill=(42, 42, 50))
    for (sx, sy, r) in [(270, 16, 8), (280, 8, 6), (264, 6, 5)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(150, 150, 150))
    # rescue beam: a narrow searchlight from the rubble
    d.polygon([(x0 + 48, y1), (x0 + 64, y1), (x0 + 58, y0 + 30), (x0 + 54, y0 + 30)],
              fill=(255, 240, 170))
    d.ellipse([x0 + 52, y0 + 26, x0 + 60, y0 + 34], fill=(255, 250, 210))


def art_cop31(d, x0, y0, x1, y1):
    """Dawn over an empty COP31 hall: banded sunrise, sun, hall, flags, bare table."""
    w, h = x1 - x0, y1 - y0
    bands = [(238, 160, 88), (246, 196, 112), (246, 230, 198)]
    for i, col in enumerate(bands):
        d.rectangle([x0, y0 + i * h // 3, x1, y0 + (i + 1) * h // 3], fill=col)
    d.ellipse([x0 + int(w * 0.72), y0 + 6, x0 + int(w * 0.72) + 28, y0 + 34],
              fill=(247, 214, 114), outline=(228, 178, 58), width=2)
    # hall block with arched windows
    d.rectangle([x0 + 8, y0 + h - 44, x1 - 8, y1], fill=NAVY)
    for i in range(7):
        wx = x0 + 18 + i * int((w - 36) / 7)
        d.rectangle([wx, y0 + h - 36, wx + 12, y0 + h - 12], fill=(247, 215, 116))
    # flags on the roofline
    for i, col in enumerate([(170, 32, 36), (28, 104, 56), (18, 36, 70),
                             (198, 160, 40), (176, 90, 0)]):
        fx = x0 + 28 + i * 26
        d.line([fx, y0 + h - 60, fx, y0 + h - 44], fill=INK, width=2)
        d.rectangle([fx, y0 + h - 60, fx + 14, y0 + h - 52], fill=col)
    # long table, empty chairs: no deal was signed
    d.rectangle([x0 + 14, y0 + h - 10, x1 - 14, y0 + h - 3], fill=(120, 82, 38))
    for i in range(6):
        cx = x0 + 30 + i * int((w - 60) / 5)
        d.rectangle([cx - 7, y0 + h - 24, cx + 7, y0 + h - 11], fill=(70, 60, 46))
    # papers left on the table
    for px in (60, 150, 240):
        d.rectangle([x0 + px, y0 + h - 14, x0 + px + 16, y0 + h - 10],
                    fill=(255, 255, 255))


def art_merkury(d, x0, y0, x1, y1):
    """Night at Benghazi port: sea, a burning listing corvette, sea drones."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=NIGHT)
    sky_stars(d, x0, y0, [(16, 8, 2), (90, 6, 2), (180, 10, 2), (250, 8, 2),
                          (60, 20, 2), (200, 22, 2)])
    # sea with wave arcs
    d.rectangle([x0, y0 + h - 22, x1, y1], fill=(16, 56, 90))
    for i in range(6):
        d.arc([x0 + 8 + i * 52, y0 + h - 16, x0 + 32 + i * 52, y0 + h - 6],
              200, 340, fill=(140, 190, 220), width=2)
    # listing hull, bow up, stern low
    d.polygon([(x0 + 40, y1 - 30), (x0 + 260, y1 - 44), (x0 + 272, y1 - 22),
               (x0 + 60, y1 - 14)], fill=(44, 50, 62))
    d.rectangle([x0 + 120, y1 - 52, x0 + 130, y1 - 34], fill=(44, 50, 62))
    # flames and smoke from the midship hit
    for (fx, fh, col) in [(140, 24, (255, 140, 40)), (152, 32, (255, 200, 60)),
                          (166, 20, (255, 140, 40))]:
        d.polygon([(x0 + fx, y1 - 44), (x0 + fx + 7, y1 - 44 - fh),
                   (x0 + fx + 14, y1 - 44)], fill=col)
    for (sx, sy, r) in [(150, 8, 6), (162, 2, 5), (140, 4, 4)]:
        d.ellipse([x0 + sx - r, y0 + sy, x0 + sx + r, y0 + sy + 2 * r],
                  fill=(130, 130, 130))
    # sea drones closing in
    for (dx, dy) in [(60, 62), (210, 58)]:
        d.rounded_rectangle([x0 + dx, y0 + dy, x0 + dx + 26, y0 + dy + 8],
                            radius=3, fill=(220, 220, 220))
        d.line([x0 + dx + 26, y0 + dy + 4, x0 + dx + 34, y0 + dy + 4],
               fill=(255, 220, 100), width=2)


def art_capitol(d, x0, y0, x1, y1):
    """Capitol dome, columns, and a ballot box with a tick (42px box)."""
    d.rectangle([x0, y0, x1, y1], fill=(222, 231, 240))
    # dome
    d.pieslice([x0 + 80, y0 + 2, x0 + 120, y0 + 26], 180, 360,
               fill=(240, 240, 238))
    d.rectangle([x0 + 98, y0, x0 + 102, y0 + 4], fill=(120, 100, 60))
    # building block with columns
    d.rectangle([x0 + 16, y0 + 24, x0 + 184, y1], fill=(200, 205, 212))
    for cx in (30, 54, 146, 170):
        d.rectangle([x0 + cx, y0 + 26, x0 + cx + 8, y1 - 2],
                    fill=(250, 248, 240))
    # ballot box with a tick, standing in front
    d.rectangle([x0 + 84, y1 - 20, x0 + 116, y1 - 2], fill=(18, 36, 70))
    d.rectangle([x0 + 92, y1 - 24, x0 + 108, y1 - 20], fill=(128, 22, 26))
    d.line([x0 + 88, y1 - 13, x0 + 96, y1 - 8, x0 + 112, y1 - 18],
           fill=(255, 255, 255), width=3)


def art_factory(d, x0, y0, x1, y1):
    """Candy factory with a sawtooth roof, flames, smoke, and a rescue cross."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(238, 218, 188))
    d.rectangle([x0 + 14, y1 - 22, x0 + 158, y1], fill=(108, 108, 110))
    d.polygon([(x0 + 14, y1 - 22), (x0 + 50, y1 - 34), (x0 + 86, y1 - 22),
               (x0 + 122, y1 - 34), (x0 + 158, y1 - 22)], fill=(88, 88, 90))
    d.rectangle([x0 + 166, y1 - 36, x0 + 178, y1], fill=(88, 88, 90))
    for (fx, fh, col) in [(38, 18, (255, 140, 40)), (52, 26, (255, 200, 60)),
                          (68, 16, (255, 140, 40)), (108, 20, (255, 200, 60)),
                          (122, 14, (255, 140, 40))]:
        d.polygon([(x0 + fx, y1 - 22), (x0 + fx + 7, y1 - 22 - fh),
                   (x0 + fx + 14, y1 - 22)], fill=col)
    for (sx, sy, r) in [(58, 4, 6), (74, 0, 5), (118, 6, 5)]:
        d.ellipse([x0 + sx - r, y0 + sy, x0 + sx + r, y0 + sy + 2 * r],
                  fill=(140, 140, 140))
    # green cross sign
    d.rectangle([x0 + 168, y0 + 4, x0 + 190, y0 + 26], fill=(28, 104, 56))
    d.rectangle([x0 + 177, y0 + 8, x0 + 181, y0 + 22], fill=(255, 255, 255))
    d.rectangle([x0 + 172, y0 + 13, x0 + 186, y0 + 17], fill=(255, 255, 255))


def art_market(d, x0, y0, x1, y1):
    """A rebound chart: falling bars, then a green arrow climbing, with coins."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(232, 240, 232))
    # bars: down, down, then up
    bars = [(10, 26, (170, 32, 36)), (36, 34, (170, 32, 36)), (62, 22, (28, 104, 56)),
            (88, 14, (28, 104, 56)), (114, 8, (28, 104, 56))]
    for (bx, bh, col) in bars:
        d.rectangle([x0 + bx, y1 - 10 - bh, x0 + bx + 18, y1 - 10], fill=col)
    d.line([x0 + 8, y1 - 12, x0 + 196, y1 - 12], fill=(120, 120, 120), width=1)
    # rising arrow
    d.line([x0 + 140, y0 + 26, x0 + 168, y0 + 10, x0 + 190, y0 + 14],
           fill=(28, 104, 56), width=3)
    d.polygon([(x0 + 190, y0 + 14), (x0 + 178, y0 + 8), (x0 + 182, y0 + 20)],
              fill=(28, 104, 56))
    # coins
    for (cx, cy) in [(150, 34), (166, 40)]:
        d.ellipse([x0 + cx, y0 + cy, x0 + cx + 14, y0 + cy + 14],
                  fill=(198, 160, 40), outline=(150, 118, 20), width=1)
        d.text((x0 + cx + 4, y0 + cy + 2), "$", font=load_font(SANS_B, 9),
               fill=(120, 90, 10))


def art_khartoum(d, x0, y0, x1, y1):
    """Khartoum skyline under a drone, smoke rising, a blue UN flag."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(240, 222, 190))
    for (bx, bw, bh) in [(6, 34, 26), (46, 24, 36), (76, 40, 22), (122, 28, 32),
                         (156, 34, 24), (192, 14, 30)]:
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(140, 118, 84))
        for wy in range(y1 - bh + 6, y1 - 4, 10):
            for wx in range(x0 + bx + 4, x0 + bx + bw - 4, 10):
                if (wx + wy) % 4 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(247, 215, 116))
    # drone above the city
    dx, dy = x0 + 96, y0 + 12
    d.polygon([(dx, dy - 5), (dx + 6, dy), (dx, dy + 5), (dx - 6, dy)], fill=(20, 20, 24))
    d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 220, 100))
    # smoke plume
    for (sx, sy, r) in [(150, 10, 6), (160, 4, 5), (142, 4, 4)]:
        d.ellipse([x0 + sx - r, y0 + sy, x0 + sx + r, y0 + sy + 2 * r],
                  fill=(120, 120, 120))
    # UN flag on a rooftop
    d.line([x0 + 182, y0 + 4, x0 + 182, y0 + 18], fill=INK, width=2)
    d.rectangle([x0 + 182, y0 + 4, x0 + 196, y0 + 12], fill=(40, 90, 160))


def art_gaza(d, x0, y0, x1, y1):
    """Rubble blocks, a cracked ground line, and a warning triangle."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(226, 216, 196))
    # rubble: grey blocks of different sizes
    for (bx, by, bw, bh) in [(10, 34, 44, 16), (58, 28, 36, 22), (98, 38, 52, 12),
                             (20, 20, 30, 12), (120, 22, 40, 14)]:
        d.rectangle([x0 + bx, y0 + by, x0 + bx + bw, y0 + by + bh],
                    fill=(140, 132, 118), outline=(100, 94, 82))
    d.line([x0 + 6, y1 - 8, x0 + 60, y1 - 16, x0 + 120, y1 - 8, x0 + 196, y1 - 14],
           fill=(90, 84, 74), width=2)
    # warning triangle
    tx, ty = x0 + 158, y0 + 4
    d.polygon([(tx, ty), (tx + 22, ty + 30), (tx - 22, ty + 30)], fill=(240, 190, 40),
              outline=(150, 110, 0))
    d.text((tx - 2, ty + 8), "!", font=load_font(SANS_B, 16), fill=(120, 80, 0))
    # small green shoots between rubble
    for (gx, gy) in [(40, 46), (170, 44)]:
        d.line([x0 + gx, y0 + gy, x0 + gx, y0 + gy - 8], fill=(28, 104, 56), width=2)
        d.ellipse([x0 + gx - 3, y0 + gy - 10, x0 + gx + 3, y0 + gy - 6],
                  fill=(28, 104, 56))


def art_airport(d, x0, y0, x1, y1):
    """Control tower, a grounded plane, and runway stripes."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(214, 228, 240))
    # control tower
    d.rectangle([x0 + 16, y0 + 12, x0 + 30, y1 - 14], fill=(120, 128, 140))
    d.rectangle([x0 + 10, y0 + 4, x0 + 36, y0 + 14], fill=(40, 90, 160))
    d.rectangle([x0 + 14, y0 + 7, x0 + 32, y0 + 11], fill=(180, 220, 240))
    # grounded plane
    d.rounded_rectangle([x0 + 70, y1 - 28, x0 + 170, y1 - 16], radius=5,
                        fill=(240, 240, 240), outline=(150, 150, 150))
    d.polygon([(x0 + 170, y1 - 26), (x0 + 192, y1 - 20), (x0 + 170, y1 - 16)],
              fill=(240, 240, 240), outline=(150, 150, 150))
    d.rectangle([x0 + 108, y1 - 38, x0 + 128, y1 - 26], fill=(240, 240, 240),
                outline=(150, 150, 150))
    for wx in (84, 100, 116, 132, 148):
        d.rectangle([x0 + wx, y1 - 26, x0 + wx + 6, y1 - 20], fill=(40, 90, 160))
    # runway
    d.rectangle([x0, y1 - 8, x1, y1], fill=(70, 70, 76))
    for i in range(5):
        d.rectangle([x0 + 12 + i * 40, y1 - 5, x0 + 30 + i * 40, y1 - 3],
                    fill=(255, 255, 255))


def art_capita(d, x0, y0, x1, y1):
    """An office tower with a steep red falling arrow and a closing door."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(232, 236, 240))
    d.rectangle([x0 + 14, y0 + 8, x0 + 78, y1], fill=(90, 100, 120))
    for wy in range(y0 + 14, y1 - 6, 12):
        for wx in range(x0 + 20, x0 + 72, 12):
            d.rectangle([wx, wy, wx + 6, wy + 6], fill=(180, 200, 220))
    # falling arrow
    d.line([x0 + 96, y0 + 8, x0 + 150, y0 + 34, x0 + 182, y0 + 28],
           fill=(170, 32, 36), width=4)
    d.polygon([(x0 + 182, y0 + 28), (x0 + 168, y0 + 22), (x0 + 172, y0 + 38)],
              fill=(170, 32, 36))
    # door, half shut
    d.rectangle([x0 + 120, y1 - 24, x0 + 150, y1], fill=(60, 50, 40))
    d.rectangle([x0 + 132, y1 - 24, x0 + 150, y1], fill=(120, 100, 80))


def art_steel(d, x0, y0, x1, y1):
    """Steel mill: chimney, sparks, and stacked coils."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(238, 228, 210))
    # chimney with smoke
    d.rectangle([x0 + 18, y0 + 12, x0 + 34, y1], fill=(110, 110, 112))
    for (sx, sy, r) in [(26, 2, 5), (32, -2, 4)]:
        d.ellipse([x0 + sx - r, y0 + sy, x0 + sx + r, y0 + sy + 2 * r],
                  fill=(150, 150, 150))
    # furnace glow
    d.rectangle([x0 + 48, y1 - 18, x0 + 120, y1], fill=(70, 70, 74))
    d.rectangle([x0 + 56, y1 - 14, x0 + 112, y1 - 6], fill=(255, 140, 40))
    # steel coils
    for (cx, cy, r) in [(150, 34, 12), (172, 38, 10), (160, 20, 9)]:
        d.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r],
                  fill=(150, 158, 168), outline=(90, 96, 104), width=2)
        d.ellipse([x0 + cx - 4, y0 + cy - 4, x0 + cx + 4, y0 + cy + 4],
                  fill=(90, 96, 104))
    # sparks
    for (sx, sy) in [(90, 16), (110, 8), (130, 18)]:
        d.line([x0 + sx, y0 + sy, x0 + sx + 4, y0 + sy + 4], fill=(255, 200, 60),
               width=2)


def art_treasury(d, x0, y0, x1, y1):
    """A treasury facade with a dollar sign and a red downward arrow."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(230, 234, 238))
    # pediment
    d.polygon([(x0 + 20, y0 + 22), (x0 + 100, y0 + 4), (x0 + 180, y0 + 22)],
              fill=(200, 204, 210))
    for cx in (36, 66, 134, 164):
        d.rectangle([x0 + cx, y0 + 24, x0 + cx + 8, y1 - 10], fill=(250, 248, 240))
    d.rectangle([x0 + 84, y0 + 24, x0 + 116, y1 - 10], fill=(40, 50, 70))
    # dollar coin
    d.ellipse([x0 + 88, y0 + 26, x0 + 112, y0 + 50], fill=(198, 160, 40),
              outline=(150, 118, 20), width=1)
    d.text((x0 + 96, y0 + 30), "$", font=load_font(SANS_B, 14), fill=(120, 90, 10))
    # downward arrow
    d.line([x0 + 130, y0 + 10, x0 + 130, y0 + 30], fill=(170, 32, 36), width=3)
    d.polygon([(x0 + 124, y0 + 26), (x0 + 136, y0 + 26), (x0 + 130, y0 + 36)],
              fill=(170, 32, 36))


def art_un(d, x0, y0, x1, y1):
    """A UN-style emblem, two flags, and a document with a seal."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(222, 232, 242))
    # emblem: blue circle with a globe grid
    d.ellipse([x0 + 78, y0 + 4, x0 + 122, y0 + 44], fill=(40, 90, 160))
    d.ellipse([x0 + 88, y0 + 12, x0 + 112, y0 + 36], outline=(255, 255, 255), width=2)
    d.line([x0 + 100, y0 + 6, x0 + 100, y0 + 42], fill=(255, 255, 255), width=2)
    d.line([x0 + 80, y0 + 24, x0 + 120, y0 + 24], fill=(255, 255, 255), width=2)
    # flags
    for (fx, col) in [(20, (170, 32, 36)), (156, (28, 104, 56))]:
        d.line([x0 + fx, y0 + 8, x0 + fx, y0 + 34], fill=INK, width=2)
        d.rectangle([x0 + fx, y0 + 8, x0 + fx + 18, y0 + 18], fill=col)
    # document with a seal
    d.rectangle([x0 + 60, y1 - 18, x0 + 140, y1 - 4], fill=(255, 255, 255),
                outline=(150, 150, 150))
    for ly in (y1 - 15, y1 - 11, y1 - 7):
        d.line([x0 + 66, ly, x0 + 118, ly], fill=(150, 150, 150), width=1)
    d.ellipse([x0 + 126, y1 - 16, x0 + 136, y1 - 6], fill=(170, 32, 36))


ART = {
    "dymer": art_dymer, "cop31": art_cop31, "merkury": art_merkury,
    "capitol": art_capitol, "factory": art_factory, "market": art_market,
    "khartoum": art_khartoum, "gaza": art_gaza, "airport": art_airport,
    "capita": art_capita, "steel": art_steel, "treasury": art_treasury,
    "un": art_un,
}


# ---------------------------------------------------------------- map
def paint_scene(img, name, x0, y0, x1, y1):
    """Render one scene into a throwaway image, then paste it: nothing a
    scene draws can spill past its own box onto the card border."""
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (w, h), PAPER)
    td = ImageDraw.Draw(tmp)
    ART[name](td, 0, 0, w, h)
    img.paste(tmp, (x0, y0))


def draw_world_map(d, x0, y0, x1, y1):
    """Schematic world map: pale continents on a light sea, numbered pins."""
    d.rectangle([x0, y0, x1, y1], fill=(212, 228, 236))
    continents = [
        [(18, 18), (86, 12), (96, 44), (70, 66), (34, 58), (14, 38)],   # N America
        [(78, 76), (100, 72), (106, 100), (90, 118), (76, 98)],          # S America
        [(128, 14), (158, 10), (166, 30), (146, 40), (128, 30)],         # Europe
        [(132, 48), (162, 44), (170, 80), (152, 104), (134, 82)],        # Africa
        [(172, 10), (262, 8), (268, 48), (230, 64), (182, 44)],          # Asia
        [(226, 92), (258, 88), (262, 106), (236, 110), (224, 100)],      # Oceania
    ]
    for poly in continents:
        d.polygon([(x0 + px, y0 + py) for (px, py) in poly], fill=(238, 228, 196),
                  outline=(180, 168, 140))
    for (n, px, py) in PINS:
        d.ellipse([x0 + px - 7, y0 + py - 7, x0 + px + 7, y0 + py + 7],
                  fill=RED, outline=(255, 255, 255), width=1)
        f = load_font(SANS_B, 9)
        label = str(n)
        tw = f.getlength(label)
        d.text((x0 + px - tw / 2, y0 + py - 5), label, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- build
def region_counts():
    """Count stories per region across heroes, cards and the also-list."""
    counts = {}
    for st in HEROES + CARDS:
        counts[st["region"]] = counts.get(st["region"], 0) + 1
    for (_, _, _, _, _, region) in ALSO:
        counts[region] = counts.get(region, 0) + 1
    order = ["EUROPE", "MIDDLE EAST", "ASIA-PACIFIC", "AMERICAS", "AFRICA",
             "OCEANIA", "WORLD"]
    return [(name, counts.get(name, 0)) for name in order]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top navy bar
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((8, 6), "THE WORLD IN ONE DAY", font=load_font(SANS_B, 13),
           fill=(255, 255, 255))
    right = "35 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
    f = load_font(SANS_B, 11)
    d.text((W - 8 - f.getlength(right), 7), right, font=f, fill=GOLD)

    # masthead
    f = load_font(SERIF_B, 58)
    title = "Monday 23 November 2026"
    d.text(((W - f.getlength(title)) / 2, 30), title, font=f, fill=INK)
    f = load_font(SERIF_I, 17)
    sub = ("Dymer toll rises to 11  ·  COP31 ends with no deal  ·  "
           "Ukraine sinks a Russian corvette off Libya")
    d.text(((W - f.getlength(sub)) / 2, 94), sub, font=f, fill=RED)

    # number strip
    y0, y1 = 114, 152
    cell = (W - 16) / 6
    d.line([8, y0, W - 8, y0], fill=RULE, width=1)
    d.line([8, y1, W - 8, y1], fill=RULE, width=1)
    for i, (num, cap) in enumerate(NUMBERS):
        cx = 8 + i * cell
        d.text((cx + 8, y0 + 2), num, font=load_font(SANS_B, 22), fill=RED)
        d.text((cx + 8, y0 + 26), cap, font=load_font(SANS, 9), fill=INK)
        if i:
            d.line([cx, y0 + 3, cx, y1 - 3], fill=RULE, width=1)

    # region tabs, sized by story count
    counts = region_counts()
    total = sum(c for _, c in counts)
    y0, y1 = 156, 172
    x = 8
    for (name, count) in counts:
        wseg = (W - 16) * count / total
        d.rectangle([x, y0, x + wseg - 1, y1], fill=REGION_FILL[name])
        label = f"{name} {count}"
        f = load_font(SANS_B, 10)
        d.text((x + (wseg - f.getlength(label)) / 2, y0 + 3), label, font=f,
               fill=(255, 255, 255))
        x += wseg

    # UTC timeline
    y0, y1 = 176, 192
    d.rectangle([8, y0, W - 8, y1], fill=NAVY2)
    f = load_font(SANS_B, 10)
    d.text((14, y0 + 3), "THE DAY IN UTC", font=f, fill=GOLD)
    f = load_font(SANS, 10)
    d.text((14 + load_font(SANS_B, 10).getlength("THE DAY IN UTC") + 14, y0 + 3),
           TIMELINE, font=f, fill=(255, 255, 255))

    # hero cards: 3 across
    hy0, hy1 = 196, 430
    hw = 322
    for i, st in enumerate(HEROES):
        x0 = 8 + i * (hw + 8)
        x1 = x0 + hw
        d.rounded_rectangle([x0, hy0, x1, hy1], radius=4, outline=RULE, width=1,
                            fill=CARD)
        paint_scene(img, st["art"], x0 + 1, hy0 + 1, x1 - 1, hy0 + 97)
        d.rectangle([x0 + 1, hy0 + 97, x1 - 1, hy0 + 98], fill=RULE)
        tx = x0 + 10
        ty = hy0 + 104
        d.text((tx, ty), str(st["n"]), font=load_font(SANS_B, 11), fill=RED)
        tx = tag_chip(d, tx + 16, ty - 1, st["tag"], TAG_FILL[st["tag"]], size=9)
        d.text((tx + 8, ty), st["place"], font=load_font(SANS_B, 10), fill=INK)
        ty += 18
        d.text((x0 + 10, ty), st["beat"], font=load_font(SANS_B, 9), fill=RED)
        ty += 13
        ty = blurb(d, x0 + 10, ty, st["head"], load_font(SANS_B, 15), INK,
                   hw - 20, 18, limit=3)
        ty += 2
        ty = blurb(d, x0 + 10, ty, st["body"], load_font(SANS, 11), INK,
                   hw - 20, 13, limit=2)
        d.text((x0 + 10, hy1 - 14), st["src"], font=load_font(SANS_I, 9), fill=GREY)

    # section header
    d.text((8, 434), "THE DAY IN TEN", font=load_font(SANS_B, 13), fill=INK)
    right = "THE STORIES THAT MOVED THE WORLD TODAY"
    f = load_font(SANS_B, 11)
    d.text((W - 8 - f.getlength(right), 436), right, font=f, fill=GREY)

    # small cards: 2 rows x 5
    cw, ch, gap = 196, 118, 8
    for i, st in enumerate(CARDS):
        row, col = divmod(i, 5)
        x0 = 8 + col * (cw + gap)
        y0 = 452 + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        d.rounded_rectangle([x0, y0, x1, y1], radius=4, outline=RULE, width=1,
                            fill=CARD)
        paint_scene(img, st["art"], x0 + 1, y0 + 1, x1 - 1, y0 + 43)
        d.rectangle([x0 + 1, y0 + 43, x1 - 1, y0 + 44], fill=RULE)
        tx = x0 + 7
        ty = y0 + 47
        d.text((tx, ty), str(st["n"]), font=load_font(SANS_B, 10), fill=RED)
        tx = tag_chip(d, tx + 14, ty - 1, st["tag"], TAG_FILL[st["tag"]], size=8)
        d.text((tx + 6, ty), st["place"], font=load_font(SANS_B, 8), fill=INK)
        ty += 15
        ty = blurb(d, x0 + 7, ty, st["head"], load_font(SANS_B, 11), INK,
                   cw - 14, 13, limit=2)
        blurb(d, x0 + 7, ty, st["body"], load_font(SANS, 9), INK, cw - 14, 11,
              limit=2)
        d.text((x0 + 7, y1 - 11), st["src"], font=load_font(SANS_I, 8), fill=GREY)

    # bottom: map + also-list
    by0, by1 = 700, 896
    # map panel
    d.rounded_rectangle([8, by0, 308, by1], radius=4, outline=RULE, width=1,
                        fill=CARD)
    d.text((16, by0 + 6), "WHERE IT HAPPENED", font=load_font(SANS_B, 12), fill=INK)
    d.text((16, by0 + 22), "pins match story numbers", font=load_font(SANS, 9),
           fill=GREY)
    draw_world_map(d, 16, by0 + 40, 300, by1 - 34)
    d.text((16, by1 - 28), "Pins 1–13 match the illustrated stories above.",
           font=load_font(SANS_I, 9), fill=GREY)
    d.text((16, by1 - 16), "Schematic map, drawn in code.",
           font=load_font(SANS_I, 9), fill=GREY)
    # also-list panel
    d.rounded_rectangle([316, by0, W - 8, by1], radius=4, outline=RULE, width=1,
                        fill=CARD)
    d.text((326, by0 + 6), "ALSO ON MONDAY 23 NOVEMBER — 22 MORE STORIES",
           font=load_font(SANS_B, 12), fill=INK)
    col_w = (W - 8 - 316 - 20 - 12) // 2
    for i, (n, place, head, src, tag, region) in enumerate(ALSO):
        col, row = divmod(i, 11)
        x = 326 + col * (col_w + 12)
        y = by0 + 26 + row * 14
        d.text((x, y), str(n), font=load_font(SANS_B, 10), fill=RED)
        line = f"{place} — {head}"
        line = clip_line(line, load_font(SANS, 10), col_w - 24)
        d.text((x + 22, y), line, font=load_font(SANS, 10), fill=INK)
    d.text((326, by1 - 13),
           "Wires: Reuters, AP, BBC, Al Jazeera, AAP, France 24, NordFX, TWZ.",
           font=load_font(SANS_I, 9), fill=GREY)

    # date check box
    dy0, dy1 = 900, 944
    d.rectangle([8, dy0, W - 8, dy1], outline=RED, width=2, fill=(255, 245, 240))
    d.text((14, dy0 + 4), "DATE CHECK", font=load_font(SANS_B, 11), fill=RED)
    blurb(d, 14, dy0 + 20, DATE_CHECK, load_font(SANS, 10), INK, W - 28, 13,
          limit=2)

    # legend
    ly = 948
    d.text((8, ly), "HOW TO READ THE TAGS — ", font=load_font(SANS_B, 10), fill=INK)
    lx = 8 + load_font(SANS_B, 10).getlength("HOW TO READ THE TAGS — ")
    legend = ("CONFIRMED official or 2+ outlets  ·  REPORTED one source's account  ·  "
              "CLAIM one side's claim, contested  ·  ONGOING still developing  ·  "
              "PENDING not settled yet")
    d.text((lx, ly), legend, font=load_font(SANS, 10), fill=INK)

    # sources footer
    sy = 962
    d.text((8, sy), "Sources: Reuters, BBC, AP, Al Jazeera, AAP, France 24, Guardian, "
           "NordFX, TWZ. Scenes are drawn illustrations, not photographs.",
           font=load_font(SANS, 9), fill=GREY)

    # bottom navy bar
    d.rectangle([0, 974, W, 1000], fill=NAVY)
    d.text((8, 982), "THE WORLD IN ONE DAY", font=load_font(SANS_B, 11),
           fill=(255, 255, 255))
    right = "MONDAY 23 NOVEMBER 2026  ·  ONE PAGE"
    f = load_font(SANS_B, 10)
    d.text((W - 8 - f.getlength(right), 983), right, font=f, fill=GOLD)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    build()
