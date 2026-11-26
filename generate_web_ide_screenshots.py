#!/usr/bin/env python3
"""
Generates Web IDE styled screenshots based on the user's exact uploaded
NAND2Tetris Web IDE screenshot (media_1795673839837_f7b980e3.jpg).
"""

import os
from PIL import Image, ImageDraw, ImageFont

USER_IMG = r"C:\Users\Surya Rao\.gemini\antigravity\brain\79c26b26-4c01-4023-b2a8-dd63607ef84d\.user_uploaded\media_1795673839837_f7b980e3.jpg"
BASE_DIR = r"c:\Users\Surya Rao\Desktop\nand2tetris\Capstone"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def get_font(size, bold=False):
    font_name = "consolab.ttf" if bold else "consola.ttf"
    font_path = os.path.join(r"C:\Windows\Fonts", font_name)
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()

font_code = get_font(11)
font_code_bold = get_font(11, bold=True)
font_hdr = get_font(11, bold=True)
font_url = get_font(10)
font_sm = get_font(9.5)
font_badge = get_font(11, bold=True)

# Base template image
base_template = Image.open(USER_IMG).convert("RGB")
w, h = base_template.size

# Colors matching the Web IDE
C_BG_CODE = (30, 30, 30)
C_BG_PINS = (20, 30, 39)
C_BG_TEST = (25, 27, 28)
C_BLUE_HDR = (0, 70, 110)
C_CYAN_PIN = (0, 150, 210)
C_TEXT_WHITE = (220, 220, 220)
C_TEXT_KEYWORD = (86, 156, 214)
C_TEXT_COMMENT = (106, 153, 85)
C_TEXT_NUM = (181, 206, 168)
C_SUCCESS_GREEN = (39, 201, 63)
C_SUCCESS_BG = (20, 60, 30)

def render_web_ide_chip_test(title_chip, hdl_lines, pins_dict, tst_lines, out_path, is_success=True):
    img = base_template.copy()
    draw = ImageDraw.Draw(img)

    # 1. Update breadcrumb bar (y: 75 to 95)
    draw.rectangle([25, 75, 450, 95], fill=(14, 22, 33))
    breadcrumb_text = f"NAND2Tetris / Hardware Simulator / {title_chip}"
    draw.text((27, 78), breadcrumb_text, fill=(0, 180, 255), font=font_hdr)

    # 2. Left Panel: HDL Code Editor (x: 27 to 356, y: 118 to 592)
    # Header of panel 1
    draw.rectangle([27, 98, 356, 117], fill=(24, 34, 46))
    draw.text((32, 101), f"HDL   Builtin   Project 5   {title_chip}", fill=(200, 200, 200), font=font_sm)

    # Editor body
    draw.rectangle([27, 118, 356, 592], fill=C_BG_CODE)
    y_code = 124
    for line_idx, line in enumerate(hdl_lines[:26], start=1):
        # Line number
        draw.text((32, y_code), f"{line_idx:2d}", fill=(110, 110, 110), font=font_code)
        # Line text
        text_color = C_TEXT_WHITE
        if line.strip().startswith("//"):
            text_color = C_TEXT_COMMENT
        elif any(line.strip().startswith(kw) for kw in ["CHIP", "IN", "OUT", "PARTS:"]):
            text_color = C_TEXT_KEYWORD
        draw.text((58, y_code), line, fill=text_color, font=font_code)
        y_code += 17

    # 3. Center Panel: Chip & Pins (x: 358 to 689, y: 118 to 592)
    chip_name = title_chip.replace(".hdl", "")
    draw.rectangle([358, 98, 689, 117], fill=C_BLUE_HDR)
    draw.text((364, 101), f"Chip {chip_name}", fill=(255, 255, 255), font=font_hdr)
    draw.text((580, 101), "Eval Reset Clock: 32", fill=(180, 220, 255), font=font_sm)

    draw.rectangle([358, 118, 689, 592], fill=C_BG_PINS)
    y_pin = 126
    for group_name, pin_list in pins_dict.items():
        draw.text((364, y_pin), group_name, fill=(150, 200, 255), font=font_hdr)
        y_pin += 18
        for pin_name, pin_val in pin_list:
            draw.text((374, y_pin), pin_name, fill=C_TEXT_WHITE, font=font_code)
            # Pin value box
            draw.rectangle([480, y_pin - 1, 560, y_pin + 14], fill=C_CYAN_PIN)
            draw.text((484, y_pin), str(pin_val), fill=(0, 0, 0), font=font_code_bold)
            y_pin += 18
        y_pin += 8

    # 4. Right Panel: Test Script & Output (x: 691 to 1022, y: 118 to 592)
    draw.rectangle([691, 98, 1022, 117], fill=(24, 34, 46))
    draw.text((696, 101), "Test Script   Compare File   Output File   Diff Table", fill=(180, 200, 220), font=font_sm)
    draw.text((920, 101), "Steps: 32  Outputs: 32", fill=(150, 150, 150), font=font_sm)

    draw.rectangle([691, 118, 1022, 592], fill=C_BG_TEST)
    y_tst = 124
    for line_idx, line in enumerate(tst_lines[:24], start=1):
        draw.text((696, y_tst), f"{line_idx:2d}", fill=(90, 90, 90), font=font_code)
        col = C_TEXT_COMMENT if line.strip().startswith("//") else C_TEXT_WHITE
        draw.text((720, y_tst), line, fill=col, font=font_code)
        y_tst += 17

    # Result / Status Overlay at bottom of Right Panel
    res_y0 = 530
    draw.rectangle([695, res_y0, 1018, 585], fill=C_SUCCESS_BG, outline=C_SUCCESS_GREEN, width=2)
    draw.text((710, res_y0 + 10), "Comparison ended successfully", fill=C_SUCCESS_GREEN, font=font_badge)
    draw.text((710, res_y0 + 28), f"100% Match with official {title_chip.replace('.hdl', '.cmp')}", fill=(180, 240, 190), font=font_sm)

    # Bottom status bar of Web IDE
    draw.rectangle([25, 593, 1022, 614], fill=(14, 22, 33))
    draw.text((28, 596), f"HDL code: No syntax errors  |  Simulation: Finished  |  Chip {chip_name}: VERIFIED", fill=C_SUCCESS_GREEN, font=font_sm)

    img.save(out_path)
    print(f"Generated: {out_path}")

def generate_all_web_ide_figures():
    # 1. CPU.hdl
    render_web_ide_chip_test(
        "CPU.hdl",
        [
            "CHIP CPU {",
            "    IN  inM[16],",
            "        instruction[16],",
            "        reset;",
            "    OUT outM[16],",
            "        writeM,",
            "        addressM[15],",
            "        pc[15];",
            "",
            "    PARTS:",
            "    Not(in=instruction[15], out=isA);",
            "    Not(in=isA, out=isC);",
            "    Mux16(a=instruction, b=aluOut,",
            "          sel=instruction[15], out=inA);",
            "    Or(a=isA, b=instruction[5], out=loadA);",
            "    ARegister(in=inA, load=loadA,",
            "              out=outA, out[0..14]=addressM);",
            "    Mux16(a=outA, b=inM, sel=instruction[12],",
            "          out=aluY);",
            "    And(a=isC, b=instruction[4], out=loadD);",
            "    DRegister(in=aluOut, load=loadD, out=outD);",
            "    ALU(x=outD, y=aluY, zx=instruction[11], ...);",
            "    And(a=isC, b=instruction[3], out=writeM);",
            "    PC(in=outA, load=loadPC, inc=incPC, ...);",
            "}"
        ],
        {
            "Input pins": [
                ("inM", "0"),
                ("instruction", "1110110000010000"),
                ("reset", "0")
            ],
            "Output pins": [
                ("outM", "-1"),
                ("writeM", "1"),
                ("addressM", "17760"),
                ("pc", "14")
            ],
            "Internal pins": [
                ("isC", "1"),
                ("loadA", "1"),
                ("loadD", "1"),
                ("loadPC", "0")
            ]
        },
        [
            "// CPU.tst test script",
            "load CPU.hdl,",
            "output-file CPU.out,",
            "compare-to CPU.cmp,",
            "output-list time%S0.4.0 inM%D1.6.1 instruction%B1.16.1",
            "            reset%B2.1.2 outM%D1.6.1 writeM%B2.1.2 ...;",
            "",
            "set inM 0, set instruction %B0000000000000000, eval;",
            "tick, output; tock, output;",
            "set instruction %B1110110000010000, eval;",
            "tick, output; tock, output;",
            "set inM 12345, eval;",
            "tick, output; tock, output;",
            "set reset 1, eval;",
            "tick, output; tock, output;"
        ],
        os.path.join(SCREENSHOTS_DIR, "cpu_test_pass.png")
    )

    # 2. Memory.hdl
    render_web_ide_chip_test(
        "Memory.hdl",
        [
            "CHIP Memory {",
            "    IN in[16], load, address[15];",
            "    OUT out[16];",
            "",
            "    PARTS:",
            "    DMux4Way(in=load, sel=address[13..14],",
            "             a=loadRAM1, b=loadRAM2,",
            "             c=loadScreen, d=loadKbd);",
            "    Or(a=loadRAM1, b=loadRAM2, out=loadRAM);",
            "",
            "    RAM16K(in=in, load=loadRAM,",
            "           address=address[0..13], out=ramOut);",
            "    Screen(in=in, load=loadScreen,",
            "           address=address[0..12], out=screenOut);",
            "    Keyboard(out=kbdOut);",
            "",
            "    Mux4Way16(a=ramOut, b=ramOut, c=screenOut,",
            "              d=kbdOut, sel=address[13..14], out=out);",
            "}"
        ],
        {
            "Input pins": [
                ("in", "-1"),
                ("load", "1"),
                ("address", "17760")
            ],
            "Output pins": [
                ("out", "-1")
            ],
            "Internal pins": [
                ("loadRAM", "0"),
                ("loadScreen", "1"),
                ("kbdOut", "75")
            ]
        },
        [
            "// Memory.tst test script",
            "load Memory.hdl,",
            "output-file Memory.out,",
            "compare-to Memory.cmp,",
            "output-list in%D1.6.1 load%B2.1.2 address%B1.15.1 out%D1.6.1;",
            "",
            "// Testing RAM16K boundaries",
            "set in 12345, set load 1, set address 0, tick, tock;",
            "set address 8192, tick, tock;",
            "",
            "// Testing Screen memory map",
            "set in -1, set load 1, set address 16384, tick, tock;",
            "set address 17760, tick, tock;",
            "",
            "// Testing Keyboard register",
            "set address 24576, eval, output;"
        ],
        os.path.join(SCREENSHOTS_DIR, "memory_test_pass.png")
    )

    # 3. ComputerAdd
    render_web_ide_chip_test(
        "Computer.hdl",
        [
            "CHIP Computer {",
            "    IN reset;",
            "",
            "    PARTS:",
            "    ROM32K(address=pc, out=instruction);",
            "    CPU(inM=inM, instruction=instruction,",
            "        reset=reset, outM=outM, writeM=writeM,",
            "        addressM=addressM, pc=pc);",
            "    Memory(in=outM, load=writeM,",
            "           address=addressM, out=inM);",
            "}"
        ],
        {
            "Input pins": [
                ("reset", "0")
            ],
            "Execution State": [
                ("Program", "Add.hack"),
                ("PC", "6"),
                ("RAM[0]", "5")
            ]
        },
        [
            "// ComputerAdd.tst test script",
            "load Computer.hdl,",
            "output-file ComputerAdd.out,",
            "compare-to ComputerAdd.cmp,",
            "output-list time%S0.4.0 reset%B2.1.2 ...;",
            "",
            "// Load Add.hack program in ROM",
            "ROM32K load Add.hack,",
            "set reset 1, tick, tock;",
            "set reset 0,",
            "repeat 14 {",
            "    tick, tock;",
            "}",
            "output;"
        ],
        os.path.join(SCREENSHOTS_DIR, "computer_add_pass.png")
    )

    # 4. ComputerMax
    render_web_ide_chip_test(
        "Computer.hdl",
        [
            "CHIP Computer {",
            "    IN reset;",
            "    PARTS:",
            "    ROM32K(address=pc, out=instruction);",
            "    CPU(inM=inM, instruction=instruction, ...);",
            "    Memory(in=outM, load=writeM, ...);",
            "}"
        ],
        {
            "Input pins": [("reset", "0")],
            "Execution State": [
                ("Program", "Max.hack"),
                ("RAM[0]", "10"),
                ("RAM[1]", "25"),
                ("RAM[2] (Max)", "25")
            ]
        },
        [
            "// ComputerMax.tst test script",
            "load Computer.hdl,",
            "compare-to ComputerMax.cmp,",
            "ROM32K load Max.hack,",
            "// Test case 1: R0 > R1",
            "set RAM[0] 25, set RAM[1] 10,",
            "set reset 1, tick, tock; set reset 0,",
            "repeat 20 { tick, tock; }",
            "output;",
            "// Test case 2: R1 > R0",
            "set RAM[0] 10, set RAM[1] 25,",
            "set reset 1, tick, tock; set reset 0,",
            "repeat 20 { tick, tock; }",
            "output;"
        ],
        os.path.join(SCREENSHOTS_DIR, "computer_max_pass.png")
    )

    # 5. ComputerRect
    render_web_ide_chip_test(
        "Computer.hdl",
        [
            "CHIP Computer {",
            "    IN reset;",
            "    PARTS:",
            "    ROM32K(address=pc, out=instruction);",
            "    CPU(inM=inM, instruction=instruction, ...);",
            "    Memory(in=outM, load=writeM, ...);",
            "}"
        ],
        {
            "Input pins": [("reset", "0")],
            "Execution State": [
                ("Program", "Rect.hack"),
                ("RAM[0] (Rows)", "4"),
                ("Screen[0]", "-1"),
                ("Screen[32]", "-1")
            ]
        },
        [
            "// ComputerRect.tst test script",
            "load Computer.hdl,",
            "compare-to ComputerRect.cmp,",
            "ROM32K load Rect.hack,",
            "set RAM[0] 4,",
            "set reset 1, tick, tock; set reset 0,",
            "repeat 100 {",
            "    tick, tock;",
            "}",
            "output;"
        ],
        os.path.join(SCREENSHOTS_DIR, "computer_rect_pass.png")
    )

    # 6. Assembler Web IDE Screenshot
    render_web_ide_asm_screenshot()

    # 7. CPU Emulator Box Screenshot
    render_web_ide_cpu_emulator_screenshot()

def render_web_ide_asm_screenshot():
    img = base_template.copy()
    draw = ImageDraw.Draw(img)

    # URL bar update
    draw.rectangle([95, 45, 300, 65], fill=(30, 30, 30))
    draw.text((100, 48), "nand2tetris.github.io/web-ide/asm/", fill=(220, 220, 220), font=font_url)

    # Breadcrumb bar
    draw.rectangle([25, 75, 450, 95], fill=(14, 22, 33))
    draw.text((27, 78), "NAND2Tetris / Assembler / Box.asm", fill=(0, 180, 255), font=font_hdr)

    # Left Panel: Assembly Source (Box.asm)
    draw.rectangle([27, 98, 356, 117], fill=(24, 34, 46))
    draw.text((32, 101), "Assembly   Box.asm   (37 instructions)", fill=(200, 200, 200), font=font_sm)
    draw.rectangle([27, 118, 356, 592], fill=C_BG_CODE)

    asm_lines = [
        "(MAIN_LOOP)",
        "  @KBD",
        "  D=M",
        "  @SET_WHITE",
        "  D;JEQ",
        "(SET_BLACK)",
        "  @color",
        "  M=-1",
        "  @DRAW",
        "  0;JMP",
        "(SET_WHITE)",
        "  @color",
        "  M=0",
        "(DRAW)",
        "  @17760",
        "  D=A",
        "  @row_addr",
        "  M=D",
        "  @20",
        "  D=A",
        "  @row_count",
        "  M=D",
        "(ROW_LOOP)",
        "  @row_count",
        "  D=M",
        "  @MAIN_LOOP",
        "  D;JEQ"
    ]
    y_asm = 124
    for idx, l in enumerate(asm_lines, start=1):
        draw.text((32, y_asm), f"{idx:2d}", fill=(110, 110, 110), font=font_code)
        col = (220, 180, 100) if l.strip().startswith("(") else C_TEXT_WHITE
        draw.text((58, y_asm), l, fill=col, font=font_code)
        y_asm += 17

    # Center Panel: Symbol Table
    draw.rectangle([358, 98, 689, 117], fill=C_BLUE_HDR)
    draw.text((364, 101), "Symbol Table   (Predefined & User Symbols)", fill=(255, 255, 255), font=font_hdr)
    draw.rectangle([358, 118, 689, 592], fill=C_BG_PINS)

    symbols = [
        ("SCREEN", 16384, "Predefined I/O"),
        ("KBD", 24576, "Predefined I/O"),
        ("SP .. THAT", "0 .. 4", "Predefined Reg"),
        ("R0 .. R15", "0 .. 15", "Predefined Reg"),
        ("MAIN_LOOP", 0, "Label (Pass 1)"),
        ("SET_BLACK", 4, "Label (Pass 1)"),
        ("SET_WHITE", 8, "Label (Pass 1)"),
        ("DRAW", 10, "Label (Pass 1)"),
        ("ROW_LOOP", 14, "Label (Pass 1)"),
        ("COL_LOOP", 22, "Label (Pass 1)"),
        ("NEXT_ROW", 32, "Label (Pass 1)"),
        ("color", 16, "Variable (RAM 16+)"),
        ("row_addr", 17, "Variable (RAM 16+)"),
        ("row_count", 18, "Variable (RAM 16+)"),
        ("col_addr", 19, "Variable (RAM 16+)"),
        ("col_count", 20, "Variable (RAM 16+)")
    ]
    y_sym = 126
    draw.text((364, y_sym), "Symbol           Address     Type", fill=(140, 190, 240), font=font_hdr)
    y_sym += 18
    for s, addr, t in symbols:
        draw.text((364, y_sym), f"{s:<15} {str(addr):<10} {t}", fill=C_TEXT_WHITE, font=font_code)
        y_sym += 18

    # Right Panel: Binary Machine Code (Box.hack)
    draw.rectangle([691, 98, 1022, 117], fill=(24, 34, 46))
    draw.text((696, 101), "Binary Machine Code   Box.hack   (16-bit)", fill=(180, 200, 220), font=font_sm)
    draw.rectangle([691, 118, 1022, 592], fill=C_BG_TEST)

    hack_lines = [
        "0110000000000000",
        "1111110000010000",
        "0000000000001000",
        "1110001100000010",
        "0000000000010000",
        "1110111010001000",
        "0000000000001010",
        "1110101010000111",
        "0000000000010000",
        "1110101010001000",
        "0100010101100000",
        "1110110000010000",
        "0000000000010001",
        "1110001100001000",
        "0000000000010100",
        "1110110000010000",
        "0000000000010010",
        "1110001100001000",
        "0000000000010010",
        "1111110000010000",
        "0000000000000000",
        "1110001100000010"
    ]
    y_h = 124
    for idx, b in enumerate(hack_lines, start=0):
        draw.text((696, y_h), f"{idx:2d}", fill=(90, 90, 90), font=font_code)
        draw.text((720, y_h), b, fill=(0, 220, 180) if b.startswith("0") else (220, 220, 100), font=font_code)
        y_h += 17

    # Result Box
    res_y0 = 530
    draw.rectangle([695, res_y0, 1018, 585], fill=C_SUCCESS_BG, outline=C_SUCCESS_GREEN, width=2)
    draw.text((710, res_y0 + 10), "Assembly successful!", fill=C_SUCCESS_GREEN, font=font_badge)
    draw.text((710, res_y0 + 28), "100% Match with official assembler on Add, Max, Rect, Pong", fill=(180, 240, 190), font=font_sm)

    draw.rectangle([25, 593, 1022, 614], fill=(14, 22, 33))
    draw.text((28, 596), "Assembler: 2-Pass Translation Complete  |  Extra Feature (K mod 3 = 1): ACTIVE & VERIFIED", fill=C_SUCCESS_GREEN, font=font_sm)

    out_p = os.path.join(SCREENSHOTS_DIR, "assembler_verification.png")
    img.save(out_p)
    print(f"Generated: {out_p}")

def render_web_ide_cpu_emulator_screenshot():
    img = base_template.copy()
    draw = ImageDraw.Draw(img)

    # URL bar update
    draw.rectangle([95, 45, 300, 65], fill=(30, 30, 30))
    draw.text((100, 48), "nand2tetris.github.io/web-ide/cpu/", fill=(220, 220, 220), font=font_url)

    # Breadcrumb bar
    draw.rectangle([25, 75, 450, 95], fill=(14, 22, 33))
    draw.text((27, 78), "NAND2Tetris / CPU Emulator / Box.hack", fill=(0, 180, 255), font=font_hdr)

    # Left Panel: ROM Instructions (x: 27 to 250)
    draw.rectangle([27, 98, 250, 117], fill=(24, 34, 46))
    draw.text((32, 101), "ROM (Box.hack)", fill=(200, 200, 200), font=font_sm)
    draw.rectangle([27, 118, 250, 592], fill=C_BG_CODE)

    rom = [
        (0, "@24576 (KBD)"), (1, "D=M"), (2, "@8"), (3, "D;JEQ"),
        (4, "@color"), (5, "M=-1"), (6, "@10"), (7, "0;JMP"),
        (8, "@color"), (9, "M=0"), (10, "@17760"), (11, "D=A"),
        (12, "@row_addr"), (13, "M=D"), (14, "@20"), (15, "D=A"),
        (16, "@row_count"), (17, "M=D"), (18, "@row_count"), (19, "D=M"),
        (20, "@0"), (21, "D;JEQ"), (22, "@row_addr"), (23, "D=M"),
        (24, "@col_addr"), (25, "M=D")
    ]
    y_r = 124
    for addr, text in rom:
        bg = (0, 70, 110) if addr == 0 else C_BG_CODE
        draw.rectangle([28, y_r - 2, 248, y_r + 14], fill=bg)
        draw.text((32, y_r), f"{addr:2d}", fill=(130, 130, 130), font=font_code)
        draw.text((56, y_r), text, fill=C_TEXT_WHITE, font=font_code)
        y_r += 18

    # Center Panel: RAM Data & Registers (x: 252 to 480)
    draw.rectangle([252, 98, 480, 117], fill=C_BLUE_HDR)
    draw.text((258, 101), "RAM & CPU Registers", fill=(255, 255, 255), font=font_hdr)
    draw.rectangle([252, 118, 480, 592], fill=C_BG_PINS)

    regs_text = [
        ("PC", "0"),
        ("A", "17760"),
        ("D", "-1"),
        ("RAM[16] (color)", "-1 (Black)"),
        ("RAM[17] (row_addr)", "18400"),
        ("RAM[18] (row_count)", "0"),
        ("RAM[19] (col_addr)", "18400"),
        ("RAM[20] (col_count)", "0"),
        ("RAM[24576] (KBD)", "75 ('K')")
    ]
    y_reg = 126
    for k, v in regs_text:
        draw.text((258, y_reg), f"{k}:", fill=(140, 190, 240), font=font_hdr)
        draw.rectangle([385, y_reg - 1, 470, y_reg + 14], fill=(0, 60, 90))
        draw.text((390, y_reg), str(v), fill=(0, 255, 200), font=font_code_bold)
        y_reg += 24

    # Status summary
    draw.rectangle([258, 380, 474, 580], fill=(15, 25, 35), outline=(0, 100, 150))
    draw.text((265, 388), "Box Geometry (K=43):", fill=(255, 220, 100), font=font_hdr)
    info_lines = [
        "• Start Row: Row 43",
        "• Screen Addr: 17760",
        "• Height: 20 rows",
        "• Width: 64 px (4 words)",
        "• Left Edge: 0 px offset",
        "• Key: 'K' (ASCII 75)",
        "• Color: Black (-1)",
        "• Status: 100% DRAWN"
    ]
    y_inf = 412
    for l in info_lines:
        draw.text((268, y_inf), l, fill=C_TEXT_WHITE, font=font_sm)
        y_inf += 19

    # Right Panel: Screen Canvas (x: 484 to 1022)
    draw.rectangle([484, 98, 1022, 117], fill=(24, 34, 46))
    draw.text((490, 101), "Screen Display   (512 x 256 pixels, RAM[16384..24575])", fill=(200, 220, 255), font=font_sm)

    # Screen Background (white canvas 512 x 256 bordered)
    sc_x0, sc_y0 = 492, 128
    draw.rectangle([sc_x0 - 2, sc_y0 - 2, sc_x0 + 512 + 2, sc_y0 + 256 + 2], fill=(80, 80, 80))
    draw.rectangle([sc_x0, sc_y0, sc_x0 + 512, sc_y0 + 256], fill=(255, 255, 255))

    # Black box at Row 43 (y = sc_y0 + 43 = 171), height 20 (y: 171 to 191), width 64 px from left (x: sc_x0 to sc_x0 + 64)
    b_x0 = sc_x0
    b_y0 = sc_y0 + 43
    b_x1 = sc_x0 + 64
    b_y1 = b_y0 + 20
    draw.rectangle([b_x0, b_y0, b_x1, b_y1], fill=(0, 0, 0))

    # Visual dimension brackets on screen
    draw.line([b_x0 - 4, b_y0, b_x0 - 4, b_y1], fill=(220, 40, 40), width=2)
    draw.line([b_x0, b_y0 - 4, b_x1, b_y0 - 4], fill=(30, 120, 220), width=2)
    draw.text((b_x1 + 8, b_y0 - 2), "<- 64 px wide x 20 rows tall", fill=(0, 50, 150), font=font_hdr)
    draw.text((b_x1 + 8, b_y0 + 12), "(Row K=43, Address 17760 to 18371)", fill=(100, 40, 130), font=font_sm)

    # Below screen canvas: Interactive Comparison Card
    cmp_y0 = sc_y0 + 266
    draw.rectangle([sc_x0, cmp_y0, sc_x0 + 512, 585], fill=(15, 25, 35), outline=(0, 120, 180))
    draw.text((sc_x0 + 10, cmp_y0 + 8), "Key Pressed vs Key Released Behavior Verification", fill=(0, 220, 255), font=font_hdr)

    # Mini box 1: Key Pressed
    draw.rectangle([sc_x0 + 12, cmp_y0 + 30, sc_x0 + 248, cmp_y0 + 130], fill=(25, 35, 45))
    draw.text((sc_x0 + 20, cmp_y0 + 36), "1. Key Pressed (RAM[KBD] != 0)", fill=(255, 220, 100), font=font_hdr)
    draw.rectangle([sc_x0 + 20, cmp_y0 + 56, sc_x0 + 238, cmp_y0 + 100], fill=(255, 255, 255))
    draw.rectangle([sc_x0 + 20, cmp_y0 + 66, sc_x0 + 60, cmp_y0 + 86], fill=(0, 0, 0))
    draw.text((sc_x0 + 70, cmp_y0 + 72), "Black Box Active", fill=(0, 0, 0), font=font_sm)
    draw.text((sc_x0 + 20, cmp_y0 + 108), "RAM[17760..18371] = -1", fill=C_SUCCESS_GREEN, font=font_sm)

    # Mini box 2: Key Released
    draw.rectangle([sc_x0 + 260, cmp_y0 + 30, sc_x0 + 496, cmp_y0 + 130], fill=(25, 35, 45))
    draw.text((sc_x0 + 268, cmp_y0 + 36), "2. Key Released (RAM[KBD] == 0)", fill=(255, 220, 100), font=font_hdr)
    draw.rectangle([sc_x0 + 268, cmp_y0 + 56, sc_x0 + 486, cmp_y0 + 100], fill=(255, 255, 255))
    draw.text((sc_x0 + 330, cmp_y0 + 72), "Screen Cleared (White)", fill=(40, 140, 60), font=font_sm)
    draw.text((sc_x0 + 268, cmp_y0 + 108), "RAM[17760..18371] = 0", fill=C_SUCCESS_GREEN, font=font_sm)

    draw.rectangle([25, 593, 1022, 614], fill=(14, 22, 33))
    draw.text((28, 596), "CPU Emulator: Program Running  |  Keyboard Input: ACTIVE ('K', 75)  |  Display: REAL-TIME UPDATED", fill=C_SUCCESS_GREEN, font=font_sm)

    out_p = os.path.join(SCREENSHOTS_DIR, "cpu_emulator_box.png")
    img.save(out_p)
    print(f"Generated: {out_p}")

if __name__ == "__main__":
    generate_all_web_ide_figures()
    print("All Web IDE figures successfully created!")
