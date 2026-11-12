import math
import random
import os
import sys
import json
import urllib.request
from PIL import Image, ImageDraw

# Color definitions (Namco Galaxian Arcade 1979 RGB)
C_BLACK = (0, 0, 0)
C_WHITE = (255, 255, 255)
C_RED = (255, 36, 0)
C_YELLOW = (255, 230, 0)
C_BLUE = (30, 100, 255)
C_CYAN = (0, 240, 255)
C_PURPLE = (220, 50, 220)
C_GREEN = (0, 230, 80)
C_DARK_GREEN = (20, 80, 40)
C_GRAY = (80, 80, 80)
C_DARK_GRAY = (30, 42, 32)

COLOR_MAP = {
    'W': C_WHITE,
    'R': C_RED,
    'Y': C_YELLOW,
    'B': C_BLUE,
    'C': C_CYAN,
    'P': C_PURPLE,
    'G': C_GREEN,
    'D': C_DARK_GREEN,
    '.': None
}

def parse_sprite(ascii_art):
    h = len(ascii_art)
    w = max(len(row) for row in ascii_art)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, row in enumerate(ascii_art):
        for x, ch in enumerate(row):
            if ch in COLOR_MAP and COLOR_MAP[ch] is not None:
                img.putpixel((x, y), (*COLOR_MAP[ch], 255))
    return img

# 13x11 Authentic Galaxip (Player Ship)
SHIP_ART = [
    "......R......",
    "......W......",
    ".....WWW.....",
    ".....WWW.....",
    "....WWWWW....",
    "...WWWCWWW...",
    "..WWWBBBW...",
    ".WWBRRRRRBW.",
    "W.WBRRRRRBW.W",
    "W.B.RRRRR.B.W",
    "R.B.......B.R"
]

# 11x9 Boss Galaxian (Flagship) Frame 1 & 2
BOSS_1 = [
    "..YYYYYYY..",
    ".YYRRRRRYY.",
    "YYRRCCCCRRY",
    "YYRCCCCCCRY",
    "YYRRCCCCRRY",
    ".YYRRRRRYY.",
    "..YYYYYYY..",
    ".RR.RRR.RR.",
    "R....R....R"
]

BOSS_2 = [
    "...YYYYY...",
    "YYYRRRRRYYY",
    "YYRRCCCCRRY",
    "YYRCCCCCCRY",
    "YYRRCCCCRRY",
    ".YYYRRRYYY.",
    "..YY.Y.YY..",
    ".RR..R..RR.",
    "R.........R"
]

# 11x9 Red Alien (Escort) Frame 1 & 2
RED_1 = [
    "..RRRRRRR..",
    ".RRYYYYYRR.",
    "RRYYWYYWYRR",
    "RRYYYYYYYRR",
    "RRYYYYYYYRR",
    ".RRRYYYRRR.",
    "..RRRRRRR..",
    ".RR.RRR.RR.",
    "R....R....R"
]

RED_2 = [
    "...RRRRR...",
    "RRRRYYYRRRR",
    "RRYYWYYWYRR",
    "RRYYYYYYYRR",
    "RRYYYYYYYRR",
    ".RRRRYRRRR.",
    "..RR.R.RR..",
    ".RR..R..RR.",
    "R.........R"
]

# 11x9 Purple Alien Frame 1 & 2
PURPLE_1 = [
    "..PPPPPPP..",
    ".PPYYYYYPP.",
    "PPYYCYYCYPP",
    "PPYYYYYYYPP",
    "PPYYYYYYYPP",
    ".PPPYYYPPP.",
    "..PPPPPPP..",
    ".PP.PPP.PP.",
    "P....P....P"
]

PURPLE_2 = [
    "...PPPPP...",
    "PPPPYYYPPPP",
    "PPYYCYYCYPP",
    "PPYYYYYYYPP",
    "PPYYYYYYYPP",
    ".PPPPYPPPP.",
    "..PP.P.PP..",
    ".PP..P..PP.",
    "P.........P"
]

# 11x9 Blue Alien (Drone) Frame 1 & 2
BLUE_1 = [
    "..CCCCCCC..",
    ".CCYYYYYCC.",
    "CCYYBYYBYCC",
    "CCYYYYYYYCC",
    "CCYYYYYYYCC",
    ".CCCYYYCCC.",
    "..CCCCCCC..",
    ".CC.CCC.CC.",
    "C....C....C"
]

BLUE_2 = [
    "...CCCCC...",
    "CCCCYYYCCCC",
    "CCYYBYYBYCC",
    "CCYYYYYYYCC",
    "CCYYYYYYYCC",
    ".CCCCYCCCC.",
    "..CC.C.CC..",
    ".CC..C..CC.",
    "C.........C"
]

# Explosion Frames
EXPLOSION_1 = [
    "..Y.Y..",
    ".YYWYY.",
    "YWWWWWY",
    ".YYWYY.",
    "..Y.Y.."
]

EXPLOSION_2 = [
    "R...Y...R",
    ".R..Y..R.",
    "..RWWWR..",
    "YYW.C.WYY",
    "..RWWWR..",
    ".R..Y..R.",
    "R...Y...R"
]

EXPLOSION_3 = [
    "R.....C.....R",
    ".Y...Y.Y...Y.",
    "..R.......R..",
    "...W.....W...",
    "C...W...W...C",
    "...W.....W...",
    "..R.......R..",
    ".Y...Y.Y...Y.",
    "R.....C.....R"
]

LIFE_ICON = [
    "...W...",
    "..WWW..",
    ".WWCWW.",
    "WWBRBWW",
    "W.BRB.W",
    "R.B.B.R",
    "R.....R"
]

FLAG_ICON = [
    "YYYY...",
    "YYYYY..",
    "YYYYYY.",
    "YYYYY..",
    "YYYY...",
    "B......",
    "B......",
    "B......"
]

SPRITES = {
    'ship': parse_sprite(SHIP_ART),
    'boss': [parse_sprite(BOSS_1), parse_sprite(BOSS_2)],
    'red': [parse_sprite(RED_1), parse_sprite(RED_2)],
    'purple': [parse_sprite(PURPLE_1), parse_sprite(PURPLE_2)],
    'blue': [parse_sprite(BLUE_1), parse_sprite(BLUE_2)],
    'exp1': parse_sprite(EXPLOSION_1),
    'exp2': parse_sprite(EXPLOSION_2),
    'exp3': parse_sprite(EXPLOSION_3),
    'life': parse_sprite(LIFE_ICON),
    'flag': parse_sprite(FLAG_ICON),
}

# Crisp 4x5 Pixel Font for Authentic Retro Arcade HUD
FONT_4x5 = {
    '0': ["0110", "1001", "1001", "1001", "0110"],
    '1': ["0010", "0110", "0010", "0010", "0111"],
    '2': ["0110", "1001", "0010", "0100", "1111"],
    '3': ["1110", "0001", "0110", "0001", "1110"],
    '4': ["1001", "1001", "1111", "0001", "0001"],
    '5': ["1111", "1000", "1110", "0001", "1110"],
    '6': ["0111", "1000", "1110", "1001", "0110"],
    '7': ["1111", "0001", "0010", "0100", "0100"],
    '8': ["0110", "1001", "0110", "1001", "0110"],
    '9': ["0110", "1001", "0111", "0001", "1110"],
    'A': ["0110", "1001", "1111", "1001", "1001"],
    'B': ["1110", "1001", "1110", "1001", "1110"],
    'C': ["0111", "1000", "1000", "1000", "0111"],
    'D': ["1110", "1001", "1001", "1001", "1110"],
    'E': ["1111", "1000", "1110", "1000", "1111"],
    'F': ["1111", "1000", "1110", "1000", "1000"],
    'G': ["0111", "1000", "1011", "1001", "0111"],
    'H': ["1001", "1001", "1111", "1001", "1001"],
    'I': ["1110", "0100", "0100", "0100", "1110"],
    'J': ["0001", "0001", "0001", "1001", "0110"],
    'K': ["1001", "1010", "1100", "1010", "1001"],
    'L': ["1000", "1000", "1000", "1000", "1111"],
    'M': ["1001", "1111", "1001", "1001", "1001"],
    'N': ["1001", "1101", "1011", "1001", "1001"],
    'O': ["0110", "1001", "1001", "1001", "0110"],
    'P': ["1110", "1001", "1110", "1000", "1000"],
    'Q': ["0110", "1001", "1001", "0110", "0001"],
    'R': ["1110", "1001", "1110", "1010", "1001"],
    'S': ["0111", "1000", "0110", "0001", "1110"],
    'T': ["1111", "0100", "0100", "0100", "0100"],
    'U': ["1001", "1001", "1001", "1001", "0110"],
    'V': ["1001", "1001", "1001", "0110", "0100"],
    'W': ["1001", "1001", "1001", "1111", "1001"],
    'X': ["1001", "0110", "0010", "0110", "1001"],
    'Y': ["1001", "1001", "0110", "0010", "0010"],
    'Z': ["1111", "0010", "0100", "1000", "1111"],
    ' ': ["0000", "0000", "0000", "0000", "0000"],
    ':': ["0000", "0100", "0000", "0100", "0000"],
    '-': ["0000", "0000", "1111", "0000", "0000"],
    '+': ["0000", "0100", "1110", "0100", "0000"],
    '!': ["0100", "0100", "0100", "0000", "0100"],
    '.': ["0000", "0000", "0000", "0000", "0100"],
}

def draw_text(img, text, x, y, color):
    cx = x
    for ch in text.upper():
        bitmap = FONT_4x5.get(ch, FONT_4x5[' '])
        for r, row in enumerate(bitmap):
            for c, bit in enumerate(row):
                if bit == '1':
                    img.putpixel((cx + c, y + r), (*color, 255))
        cx += 5

def fetch_contributions(username):
    url = f"https://github-contributions-api.jogruber.de/v4/{username}?y=last"
    headers = {"User-Agent": "Galaxian-Generator"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data
    except Exception as e:
        print(f"Warning: Could not fetch public contributions ({e}), using default fallback.")
        return None

def generate_animation(username="AndyHung-dentsu", output_path="galaxian.gif"):
    WIDTH = 300
    HEIGHT = 175
    TOTAL_FRAMES = 60
    SCALE = 2

    data = fetch_contributions(username)
    total_commits = 1366
    contributions = []
    if data and 'total' in data:
        total_commits = data['total'].get('lastYear', 1366)
        contributions = data.get('contributions', [])

    recent_contribs = contributions[-98:] if len(contributions) >= 98 else []

    formation_grid = []
    for col in range(14):
        col_cells = []
        for row in range(7):
            idx = col * 7 + row
            if idx < len(recent_contribs):
                lvl = recent_contribs[idx].get('level', 0)
            else:
                lvl = random.choice([0, 1, 2, 3, 4]) if not recent_contribs else 0

            if lvl == 4:
                alien_type = 'boss'
            elif lvl == 3:
                alien_type = 'red'
            elif lvl == 2:
                alien_type = 'purple'
            elif lvl == 1:
                alien_type = 'blue'
            else:
                alien_type = None
            col_cells.append(alien_type)
        formation_grid.append(col_cells)

    # Find attacker aliens from existing formation
    boss_cands = [(c, r) for c in range(14) for r in range(7) if formation_grid[c][r] == 'boss']
    red_cands = [(c, r) for c in range(14) for r in range(7) if formation_grid[c][r] == 'red']
    purple_cands = [(c, r) for c in range(14) for r in range(7) if formation_grid[c][r] == 'purple']

    if boss_cands:
        attacker_boss = boss_cands[len(boss_cands) // 2]
    elif red_cands:
        attacker_boss = red_cands[0]
    else:
        attacker_boss = (6, 0)
        formation_grid[6][0] = 'boss'

    if red_cands:
        attacker_red = min(red_cands, key=lambda p: abs(p[0] - attacker_boss[0]) + abs(p[1] - attacker_boss[1]))
    elif purple_cands:
        attacker_red = purple_cands[0]
    else:
        attacker_red = (5, 1)
        formation_grid[5][1] = 'red'

    random.seed(42)
    stars = []
    star_colors = [C_WHITE, C_CYAN, C_YELLOW, C_RED]
    for _ in range(45):
        stars.append({
            'x': random.randint(0, WIDTH - 1),
            'y': random.randint(0, HEIGHT - 1),
            'speed': random.choice([0.4, 0.8, 1.2]),
            'color': random.choice(star_colors)
        })

    frames = []

    for f in range(TOTAL_FRAMES):
        frame = Image.new("RGBA", (WIDTH, HEIGHT), (*C_BLACK, 255))

        # Starfield
        for star in stars:
            star['y'] = (star['y'] + star['speed']) % HEIGHT
            color = star['color']
            if (f + int(star['x'])) % 8 == 0:
                color = C_WHITE if star['color'] != C_WHITE else C_CYAN
            frame.putpixel((int(star['x']), int(star['y'])), (*color, 255))

        # HUD Score
        score_val = total_commits * 10
        if f >= 36:
            score_val += 100
        if f >= 42:
            score_val += 800

        draw_text(frame, "1UP", 16, 4, C_RED)
        draw_text(frame, f"{score_val:06d}", 16, 11, C_WHITE)

        draw_text(frame, "HIGH SCORE", 108, 4, C_RED)
        draw_text(frame, "099990", 120, 11, C_WHITE)

        draw_text(frame, "COMMITS", 218, 4, C_RED)
        draw_text(frame, f"{total_commits}", 226, 11, C_YELLOW)

        # Formation sway & flap
        sway_x = math.sin(f * 0.12) * 8
        wing_state = (f // 6) % 2
        grid_start_x = 38 + sway_x
        grid_start_y = 22

        # Draw formation aliens
        for col_idx in range(14):
            for row_idx in range(7):
                is_diving_boss = (15 <= f < 49 and col_idx == attacker_boss[0] and row_idx == attacker_boss[1])
                is_diving_red = (15 <= f < 43 and col_idx == attacker_red[0] and row_idx == attacker_red[1])
                if is_diving_boss or is_diving_red:
                    continue

                atype = formation_grid[col_idx][row_idx]
                ax = int(grid_start_x + col_idx * 16)
                ay = int(grid_start_y + row_idx * 12)

                if atype:
                    spr = SPRITES[atype][wing_state]
                    frame.paste(spr, (ax, ay), spr)
                else:
                    frame.putpixel((ax + 5, ay + 4), (*C_DARK_GRAY, 255))

        # Diving Red Alien (frames 15..36)
        red_intercept = (86, 142)
        if 15 <= f <= 36:
            t = (f - 15) / 21.0
            p0 = (grid_start_x + attacker_red[0] * 16, grid_start_y + attacker_red[1] * 12)
            p1 = (p0[0] - 35, p0[1] + 28)
            p2 = red_intercept
            rx = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
            ry = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]

            next_t = min(1.0, t + 0.05)
            nx = (1 - next_t)**2 * p0[0] + 2 * (1 - next_t) * next_t * p1[0] + next_t**2 * p2[0]
            ny = (1 - next_t)**2 * p0[1] + 2 * (1 - next_t) * next_t * p1[1] + next_t**2 * p2[1]
            angle = math.degrees(math.atan2(ny - ry, nx - rx)) - 90

            red_spr = SPRITES['red'][wing_state].rotate(-angle, resample=Image.NEAREST, expand=True)
            frame.paste(red_spr, (int(rx - red_spr.width / 2), int(ry - red_spr.height / 2)), red_spr)

            # Alien drops bullet
            if 24 <= f <= 36:
                by = int(ry + (f - 24) * 4)
                if by < 155:
                    frame.putpixel((int(rx), by), (*C_YELLOW, 255))
                    frame.putpixel((int(rx), by + 1), (*C_RED, 255))

        # Diving Boss Galaxian (frames 16..42)
        boss_intercept = (96, 136)
        if 16 <= f <= 42:
            t = (f - 16) / 26.0
            p0 = (grid_start_x + attacker_boss[0] * 16, grid_start_y + attacker_boss[1] * 12)
            p1 = (p0[0] + 45, p0[1] + 25)
            p2 = boss_intercept
            bx = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
            by = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]

            next_t = min(1.0, t + 0.05)
            nx = (1 - next_t)**2 * p0[0] + 2 * (1 - next_t) * next_t * p1[0] + next_t**2 * p2[0]
            ny = (1 - next_t)**2 * p0[1] + 2 * (1 - next_t) * next_t * p1[1] + next_t**2 * p2[1]
            angle = math.degrees(math.atan2(ny - by, nx - bx)) - 90

            boss_spr = SPRITES['boss'][wing_state].rotate(-angle, resample=Image.NEAREST, expand=True)
            frame.paste(boss_spr, (int(bx - boss_spr.width / 2), int(by - boss_spr.height / 2)), boss_spr)

        # Explosions and Floating Scores
        if 36 <= f <= 41:
            ex_frame = (f - 36) // 2
            spr = [SPRITES['exp1'], SPRITES['exp2'], SPRITES['exp3']][min(ex_frame, 2)]
            frame.paste(spr, (red_intercept[0] - spr.width // 2, red_intercept[1] - spr.height // 2), spr)
            score_y = 132 - (f - 36)
            draw_text(frame, "100", 68, score_y, C_YELLOW)

        if 42 <= f <= 48:
            ex_frame = (f - 42) // 2
            spr = [SPRITES['exp1'], SPRITES['exp2'], SPRITES['exp3']][min(ex_frame, 2)]
            frame.paste(spr, (boss_intercept[0] - spr.width // 2, boss_intercept[1] - spr.height // 2), spr)
            score_y = 126 - (f - 42)
            draw_text(frame, "800", 102, score_y, C_WHITE)

        # Player ship glide
        ship_y = 153
        if f < 15:
            ship_x = 130 - (f / 15.0) * 25
        elif 15 <= f <= 35:
            ship_x = 105 - ((f - 15) / 20.0) * 19
        elif 35 < f <= 44:
            ship_x = 86 + ((f - 35) / 9.0) * 10
        else:
            ship_x = 96 + ((f - 44) / 16.0) * 34

        ship_spr = SPRITES['ship']
        frame.paste(ship_spr, (int(ship_x - ship_spr.width / 2), ship_y), ship_spr)

        # Lasers
        if 31 <= f <= 36:
            lx = 86
            ly = ship_y - (f - 31) * 3
            frame.putpixel((lx, ly), (*C_YELLOW, 255))
            frame.putpixel((lx, ly - 1), (*C_YELLOW, 255))
            frame.putpixel((lx, ly - 2), (*C_RED, 255))

        if 36 <= f <= 42:
            lx = 96
            ly = ship_y - (f - 36) * 3
            frame.putpixel((lx, ly), (*C_YELLOW, 255))
            frame.putpixel((lx, ly - 1), (*C_YELLOW, 255))
            frame.putpixel((lx, ly - 2), (*C_RED, 255))

        # Bottom HUD
        for i in range(3):
            frame.paste(SPRITES['life'], (12 + i * 10, 166), SPRITES['life'])

        for i in range(4):
            frame.paste(SPRITES['flag'], (WIDTH - 45 + i * 9, 165), SPRITES['flag'])

        draw_text(frame, "STAGE 01", 124, 166, C_CYAN)

        scaled = frame.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.NEAREST)
        frames.append(scaled)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        optimize=True
    )
    print(f"Generated {output_path} successfully! Total frames: {len(frames)}")

if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "AndyHung-dentsu"
    out = sys.argv[2] if len(sys.argv) > 2 else "galaxian.gif"
    generate_animation(user, out)
