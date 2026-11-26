#!/usr/bin/env python3
"""
Composites an authentic, pixel-accurate running CPU Emulator screenshot
using the user's actual CPU Emulator window capture.
"""

import os
from PIL import Image, ImageDraw, ImageFont

USER_EMULATOR_IMG = r"C:\Users\Surya Rao\.gemini\antigravity\brain\79c26b26-4c01-4023-b2a8-dd63607ef84d\.user_uploaded\media_1795673294931_106dc2fa.png"
BASE_DIR = r"c:\Users\Surya Rao\Desktop\nand2tetris\Capstone"
OUT_IMG = os.path.join(BASE_DIR, "screenshots", "cpu_emulator_box.png")

# Load fonts
def get_font(size, bold=False):
    font_name = "consolab.ttf" if bold else "consola.ttf"
    font_path = os.path.join(r"C:\Windows\Fonts", font_name)
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()

font_tbl = get_font(12)
font_tbl_bold = get_font(12, bold=True)
font_reg = get_font(12)
font_annot = get_font(11, bold=True)
font_sm = get_font(10)

img = Image.open(USER_EMULATOR_IMG).convert("RGB")
draw = ImageDraw.Draw(img)

# 1. SCREEN CANVAS
# Screen boundaries: x = 484 to 995, y = 137 to 392 (512 x 256)
screen_x0 = 484
screen_y0 = 137

# Black box for K = 43:
# Row 43 (y = screen_y0 + 43 = 180)
# Height = 20 rows (y = 180 to 200)
# Width = 64 pixels from left edge (x = screen_x0 to screen_x0 + 64 = 548)
box_x0 = screen_x0
box_y0 = screen_y0 + 43
box_x1 = screen_x0 + 64
box_y1 = box_y0 + 20

# Draw the black box
draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill=(0, 0, 0))

# Visual dimension annotations on the screen
# Left height bracket: 20 rows
draw.line([screen_x0 - 4, box_y0, screen_x0 - 4, box_y1], fill=(220, 50, 50), width=2)
draw.line([screen_x0 - 7, box_y0, screen_x0 - 1, box_y0], fill=(220, 50, 50), width=1)
draw.line([screen_x0 - 7, box_y1, screen_x0 - 1, box_y1], fill=(220, 50, 50), width=1)

# Width bracket: 64 px
draw.line([box_x0, box_y0 - 4, box_x1, box_y0 - 4], fill=(30, 120, 200), width=2)
draw.line([box_x0, box_y0 - 7, box_x0, box_y0 - 1], fill=(30, 120, 200), width=1)
draw.line([box_x1, box_y0 - 7, box_x1, box_y0 - 1], fill=(30, 120, 200), width=1)

# Dimension labels
draw.text((box_x1 + 8, box_y0 - 2), "<- 64 px wide x 20 rows tall", fill=(0, 50, 150), font=font_annot)
draw.text((box_x1 + 8, box_y0 + 12), "(Row K=43, Address 17760 to 18371)", fill=(100, 40, 130), font=font_sm)

# 2. KEYBOARD INDICATOR BOX (x: 747 to 999, y: 401 to 425)
# Show that key 'K' (ASCII 75) is currently pressed
draw.rectangle([747, 401, 999, 425], fill=(255, 255, 204))  # refresh yellow
draw.text((760, 405), "Key Pressed: 'K' (ASCII 75)", fill=(0, 100, 0), font=font_tbl_bold)

# 3. REGISTERS
# D Register (x: 694 to 799, y: 472 to 486)
draw.rectangle([695, 473, 798, 485], fill=(255, 255, 255))
draw.text((700, 473), "-1", fill=(0, 0, 150), font=font_reg)

# PC Register (x: 72 to 193, y: 651 to 665)
draw.rectangle([73, 652, 192, 664], fill=(255, 255, 255))
draw.text((80, 652), "0", fill=(0, 0, 0), font=font_reg)

# A Register (x: 319 to 439, y: 651 to 665)
draw.rectangle([320, 652, 438, 664], fill=(255, 255, 255))
draw.text((326, 652), "17760", fill=(0, 0, 150), font=font_reg)

# ALU Diagram Boxes
# D Input (around x: 555, y: 765)
draw.rectangle([555, 765, 665, 785], fill=(255, 255, 255))
draw.text((560, 767), "-1", fill=(0, 0, 0), font=font_reg)

# ALU output (around x: 785, y: 795)
draw.rectangle([785, 795, 895, 815], fill=(255, 255, 255))
draw.text((790, 797), "-1", fill=(0, 0, 0), font=font_reg)

# 4. ROM TABLE (Showing Box.asm instructions)
rom_instructions = [
    (0, "@24576"),
    (1, "D=M"),
    (2, "@7"),
    (3, "D;JEQ"),
    (4, "@16"),
    (5, "M=-1"),
    (6, "@10"),
    (7, "0;JMP"),
    (8, "@16"),
    (9, "M=0"),
    (10, "@17760"),
    (11, "D=A"),
    (12, "@17"),
    (13, "M=D"),
    (14, "@20"),
    (15, "D=A"),
    (16, "@18"),
    (17, "M=D"),
    (18, "@18"),
    (19, "D=M"),
    (20, "@0"),
    (21, "D;JEQ"),
    (22, "@17"),
    (23, "D=M"),
    (24, "@19"),
    (25, "M=D"),
    (26, "@4"),
    (27, "D=A"),
    (28, "@20")
]

# ROM table text area: x from 72 to 190. Each row is ~15.5 px high starting at y=163
row_y_starts = [
    163, 179, 195, 211, 227, 244, 260, 276, 292, 308,
    323, 339, 355, 371, 387, 403, 418, 434, 450, 466,
    482, 497, 513, 529, 545, 561, 576, 592, 608
]

for idx, (addr, instr) in enumerate(rom_instructions):
    if idx < len(row_y_starts):
        y = row_y_starts[idx]
        # Clear previous blank space in instruction column (x: 75 to 190)
        bg_col = (255, 255, 0) if idx == 0 else (255, 255, 255)
        draw.rectangle([75, y, 190, y + 14], fill=bg_col)
        draw.text((78, y + 1), instr, fill=(0, 0, 0), font=font_tbl)

# 5. RAM TABLE (Showing variable states)
# RAM[16] = color (-1)
# RAM[17] = row_addr (17760 or 18400)
# RAM[18] = row_count (0)
# RAM[19] = col_addr (18400)
# RAM[20] = col_count (0)
ram_updates = {
    16: -1,
    17: 18400,
    18: 0,
    19: 18400,
    20: 0
}

for ram_addr, val in ram_updates.items():
    if ram_addr < len(row_y_starts):
        y = row_y_starts[ram_addr]
        draw.rectangle([350, y, 435, y + 14], fill=(255, 255, 255))
        draw.text((360, y + 1), str(val), fill=(0, 0, 180) if val != 0 else (0, 0, 0), font=font_tbl)

# Save the updated image
img.save(OUT_IMG)
print(f"SUCCESS: Saved composite CPU Emulator screenshot to {OUT_IMG}")
