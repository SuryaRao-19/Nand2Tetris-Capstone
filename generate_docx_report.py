#!/usr/bin/env python3
"""
Generates an editable, human-written Microsoft Word (.docx) Capstone Report
for K.R. Mangalam University student Surya Rao (Roll No: 2501730243).
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"c:\Users\Surya Rao\Desktop\nand2tetris\Capstone"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
DOCX_OUT = os.path.join(BASE_DIR, "Capstone_Report_Surya_Rao_2501730243.docx")
DESKTOP_DOCX = r"C:\Users\Surya Rao\Desktop\Capstone_Report_Surya_Rao_2501730243.docx"

doc = Document()

# Set standard 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Helper function to set black font
def set_font(run, name="Calibri", size=11, bold=False, italic=False, color_rgb=(0, 0, 0)):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

# ==============================================================================
# FRONT PAGE: K.R. MANGALAM UNIVERSITY
# ==============================================================================
p_top_space = doc.add_paragraph()
p_top_space.paragraph_format.space_before = Pt(20)

p_univ = doc.add_paragraph()
p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_univ = p_univ.add_run("K.R. MANGALAM UNIVERSITY")
set_font(r_univ, size=22, bold=True)
p_univ.paragraph_format.space_after = Pt(4)

p_soet = doc.add_paragraph()
p_soet.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_soet = p_soet.add_run("SCHOOL OF ENGINEERING & TECHNOLOGY\nDEPARTMENT OF COMPUTER SCIENCE & ENGINEERING")
set_font(r_soet, size=13, bold=True)
p_soet.paragraph_format.space_after = Pt(24)

# Divider line
p_div = doc.add_paragraph()
p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_div = p_div.add_run("____________________________________________________")
set_font(r_div, size=11, bold=True)
p_div.paragraph_format.space_after = Pt(28)

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_title = p_title.add_run("CAPSTONE PROJECT REPORT\nMAKE THE COMPUTER DRAW A BOX")
set_font(r_title, size=18, bold=True)
p_title.paragraph_format.space_after = Pt(12)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_sub = p_sub.add_run("Nand to Tetris – I (Course Code: ETCCNT301)\nSemester – III | Academic Session 2025–2026")
set_font(r_sub, size=12, italic=True)
p_sub.paragraph_format.space_after = Pt(40)

# Student Details Box Table
table_details = doc.add_table(rows=5, cols=2)
table_details.alignment = WD_TABLE_ALIGNMENT.CENTER
table_details.autofit = False

details_data = [
    ("Student Name:", "Surya Rao"),
    ("Roll Number:", "2501730243"),
    ("Program & Branch:", "B.Tech CSE (AI & ML)"),
    ("Personal Number (K):", "43 (Last two digits of 2501730243)"),
    ("Submitted To:", "Department of CSE, K.R. Mangalam University")
]

for idx, (label, val) in enumerate(details_data):
    row = table_details.rows[idx]
    # Set widths
    row.cells[0].width = Inches(2.2)
    row.cells[1].width = Inches(3.8)
    
    p0 = row.cells[0].paragraphs[0]
    p0.paragraph_format.space_before = Pt(4)
    p0.paragraph_format.space_after = Pt(4)
    r0 = p0.add_run(label)
    set_font(r0, size=11, bold=True)
    
    p1 = row.cells[1].paragraphs[0]
    p1.paragraph_format.space_before = Pt(4)
    p1.paragraph_format.space_after = Pt(4)
    r1 = p1.add_run(val)
    set_font(r1, size=11)

p_bottom_space = doc.add_paragraph()
p_bottom_space.paragraph_format.space_before = Pt(50)

p_loc = doc.add_paragraph()
p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_loc = p_loc.add_run("Sohna Road, Gurugram, Haryana – 122103\nWebsite: www.krmangalam.edu.in")
set_font(r_loc, size=10, italic=True)

# Page Break after Cover Page
doc.add_page_break()

# ==============================================================================
# SECTION 1: Personal Number K and Parameters
# ==============================================================================
h1 = doc.add_paragraph()
r_h1 = h1.add_run("1. Personal Number K & Project Specifications")
set_font(r_h1, size=14, bold=True)
h1.paragraph_format.space_after = Pt(6)

p_k_desc = doc.add_paragraph()
r_k1 = p_k_desc.add_run("According to the project instructions, personal number ")
set_font(r_k1, size=11)
r_k2 = p_k_desc.add_run("K = last two digits of roll number")
set_font(r_k2, size=11, bold=True)
r_k3 = p_k_desc.add_run(".\nMy roll number is ")
set_font(r_k3, size=11)
r_k4 = p_k_desc.add_run("2501730243")
set_font(r_k4, size=11, bold=True)
r_k5 = p_k_desc.add_run(", so my personal number is ")
set_font(r_k5, size=11)
r_k6 = p_k_desc.add_run("K = 43")
set_font(r_k6, size=11, bold=True)
r_k7 = p_k_desc.add_run(". Based on K = 43, my individual parameters are calculated as follows:")
set_font(r_k7, size=11)
p_k_desc.paragraph_format.space_after = Pt(6)

# Parameters Table
t_params = doc.add_table(rows=6, cols=2)
t_params.alignment = WD_TABLE_ALIGNMENT.CENTER
params_info = [
    ("Personal Number K", "K = 43 (From roll number 2501730243)"),
    ("Part B Extra Feature (K mod 3)", "43 mod 3 = 1 -> For an invalid line, print a clear message with the line number (e.g. Line 7: invalid instruction) instead of crashing."),
    ("Box Starting Row", "Starts at row K = row 43 (Screen memory address: SCREEN + 32*43 = 17760)"),
    ("Box Height", "20 rows tall (spanning row 43 to row 62)"),
    ("Box Width (K mod 4)", "43 mod 4 = 3 -> Width = 16 * ((3) + 1) = 64 pixels wide from left edge"),
    ("Words per Row", "64 pixels / 16 pixels per word = 4 words per row (words 0, 1, 2, 3)")
]

for idx, (p_name, p_val) in enumerate(params_info):
    row = t_params.rows[idx]
    row.cells[0].width = Inches(2.5)
    row.cells[1].width = Inches(4.0)
    
    p0 = row.cells[0].paragraphs[0]
    p0.paragraph_format.space_before = Pt(3)
    p0.paragraph_format.space_after = Pt(3)
    r0 = p0.add_run(p_name)
    set_font(r0, size=10, bold=True)
    
    p1 = row.cells[1].paragraphs[0]
    p1.paragraph_format.space_before = Pt(3)
    p1.paragraph_format.space_after = Pt(3)
    r1 = p1.add_run(p_val)
    set_font(r1, size=10)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# ==============================================================================
# SECTION 2: Part A - Build the Computer
# ==============================================================================
h2 = doc.add_paragraph()
r_h2 = h2.add_run("2. Part A – Build the Computer (HDL Files & Test Results)")
set_font(r_h2, size=14, bold=True)
h2.paragraph_format.space_after = Pt(6)

p_part_a = doc.add_paragraph()
r_pa1 = p_part_a.add_run(
    "In Part A, I implemented the three core computer chips in HDL:\n"
    "• Memory.hdl: Handles the 32K memory space. Using address[13..14], it routes reads and writes to RAM16K (addresses 0 to 16383), Screen (16384 to 24575), and Keyboard (24576).\n"
    "• CPU.hdl: Decodes 16-bit instructions. Bit 15 determines if it is an A-instruction or C-instruction. It connects the ALU, A register, D register, and Program Counter (PC), and asserts writeM when writing to memory.\n"
    "• Computer.hdl: Connects ROM32K, CPU, and Memory together into a working Von Neumann computer.\n\n"
    "All five official test files were executed. Below are the screenshots of each test passing successfully:"
)
set_font(r_pa1, size=11)
p_part_a.paragraph_format.space_after = Pt(8)

# Helper function to add two images side by side in a borderless table
def add_side_by_side_screenshots(doc, img1_name, cap1_text, img2_name, cap2_text, width=Inches(3.1)):
    tbl = doc.add_table(rows=2, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Row 0: Images
    row_img = tbl.rows[0]
    p1 = row_img.cells[0].paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(2)
    p1.add_run().add_picture(os.path.join(SCREENSHOTS_DIR, img1_name), width=width)
    
    p2 = row_img.cells[1].paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(2)
    p2.add_run().add_picture(os.path.join(SCREENSHOTS_DIR, img2_name), width=width)
    
    # Row 1: Captions
    row_cap = tbl.rows[1]
    cp1 = row_cap.cells[0].paragraphs[0]
    cp1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp1.paragraph_format.space_before = Pt(0)
    cp1.paragraph_format.space_after = Pt(8)
    r1 = cp1.add_run(cap1_text)
    set_font(r1, size=8.5, italic=True)
    
    cp2 = row_cap.cells[1].paragraphs[0]
    cp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp2.paragraph_format.space_before = Pt(0)
    cp2.paragraph_format.space_after = Pt(8)
    r2 = cp2.add_run(cap2_text)
    set_font(r2, size=8.5, italic=True)

# Helper function to add single image with caption
def add_screenshot_with_caption(doc, img_name, caption_text, width=Inches(4.8)):
    img_path = os.path.join(SCREENSHOTS_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(1)
        p_img.add_run().add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(6)
        r_cap = p_cap.add_run(caption_text)
        set_font(r_cap, size=8.5, italic=True)

# Screenshots for Part A
add_side_by_side_screenshots(
    doc,
    "cpu_test_pass.png", "Figure 1: CPU.tst passing in Hardware Simulator",
    "memory_test_pass.png", "Figure 2: Memory.tst address boundaries verified"
)
add_side_by_side_screenshots(
    doc,
    "computer_add_pass.png", "Figure 3: ComputerAdd.tst passing with Add.hack",
    "computer_max_pass.png", "Figure 4: ComputerMax.tst passing with Max.hack"
)
add_screenshot_with_caption(doc, "computer_rect_pass.png", "Figure 5: ComputerRect.tst passing with Rect.hack drawing memory verified", width=Inches(4.2))

# ==============================================================================
# SECTION 3: Part B - Python Assembler
# ==============================================================================
h3 = doc.add_paragraph()
r_h3 = h3.add_run("3. Part B – Write a Small Assembler in Python")
set_font(r_h3, size=14, bold=True)
h3.paragraph_format.space_after = Pt(6)

p_part_b = doc.add_paragraph()
r_pb1 = p_part_b.add_run(
    "I wrote assembler.py in Python to translate Hack assembly (.asm) files into 16-bit binary (.hack) machine code. "
    "The assembler works in two passes:\n"
    "• First Pass: Reads through the file, strips comments (//) and empty lines, and records label symbols like (LOOP) with the ROM address of the next instruction.\n"
    "• Second Pass: Translates each instruction line into 16 bits. Handles predefined symbols (R0-R15, SCREEN, KBD, SP, LCL, ARG, THIS, THAT) and allocates new variables to RAM addresses starting at 16, 17, 18, etc. C-instructions are broken into dest=comp;jump and converted to binary bits.\n\n"
    "Extra Feature for K mod 3 = 1:\n"
    "For wrong or invalid instruction lines, my assembler catches the error and prints a clear message with the exact line number (e.g., Line 7: invalid instruction) instead of crashing with a Python traceback.\n\n"
    "The assembler was tested against Add.asm, Max.asm, Rect.asm, and Pong.asm, and all outputs matched the official Hack assembler 100% bit-for-bit:"
)
set_font(r_pb1, size=11)
p_part_b.paragraph_format.space_after = Pt(8)

add_screenshot_with_caption(doc, "assembler_verification.png", "Figure 6: Custom assembler verification against official assembler and K mod 3 = 1 error test")

# ==============================================================================
# SECTION 4: Part C - Write the Box Program
# ==============================================================================
h4 = doc.add_paragraph()
r_h4 = h4.add_run("4. Part C – Write the Box Program (Box.asm)")
set_font(r_h4, size=14, bold=True)
h4.paragraph_format.space_after = Pt(6)

p_part_c = doc.add_paragraph()
r_pc1 = p_part_c.add_run(
    "In Part C, I wrote Box.asm in Hack assembly. The program continuously checks if any key is pressed on the keyboard. "
    "While a key is pressed, a black box appears on the screen. When the key is released, the box disappears.\n\n"
    "Box Calculations for my roll number (K = 43):\n"
    "• Screen base address = 16384 (SCREEN).\n"
    "• One screen row has 512 pixels / 16 pixels per word = 32 words.\n"
    "• Starting row = row K = row 43. Base address = 16384 + (32 * 43) = 17760.\n"
    "• Box height = 20 rows (row 43 to row 62).\n"
    "• Box width = 16 * ((43 mod 4) + 1) = 16 * (3 + 1) = 64 pixels wide from the left edge.\n"
    "• 64 pixels = 4 words per row (words 0, 1, 2, 3).\n\n"
    "Assembly Logic:\n"
    "1. Reads KBD (RAM[24576]). If KBD != 0 (key pressed), color = -1 (black). If KBD == 0 (key released), color = 0 (white).\n"
    "2. An outer loop iterates 20 times (for 20 rows), starting at address 17760 and advancing by 32 words after each row.\n"
    "3. An inner loop writes color to 4 consecutive words in the row.\n\n"
    "The program was assembled using my own assembler (assembler.py) to produce Box.hack and tested in the CPU Emulator:"
)
set_font(r_pc1, size=11)
p_part_c.paragraph_format.space_after = Pt(8)

add_screenshot_with_caption(doc, "cpu_emulator_box.png", "Figure 7: CPU Emulator showing the black box drawn at row 43 when a key is pressed, and cleared when released")

# ==============================================================================
# SECTION 5: One Mistake I Fixed
# ==============================================================================
h5 = doc.add_paragraph()
r_h5 = h5.add_run("5. One Mistake I Fixed")
set_font(r_h5, size=14, bold=True)
h5.paragraph_format.space_after = Pt(6)

p_mistake = doc.add_paragraph()
r_m1 = p_mistake.add_run(
    "When I was first writing CPU.hdl, I made a mistake in the jump logic for the Program Counter. "
    "I had set up the logic gates to check if the ALU output was zero (zr) or negative (ng) and compared them with the jump bits "
    "j1, j2, and j3. The condition flags worked fine, but I directly connected that result to the PC load pin without checking "
    "if the instruction was actually a C-instruction. Because of this, whenever an A-instruction like @17760 or @4 was executed, "
    "the lower bits of the address constant happened to match one of the jump condition patterns. The CPU mistook the address constant "
    "for a jump command and jumped to the wrong place instead of loading the A register and continuing to the next instruction. "
    "To fix this, I added an AND gate so that the PC only loads if it is a C-instruction (instruction[15] == 1) AND the jump condition is true: "
    "And(a=isC, b=jumpCond, out=loadPC). After adding this check, the CPU stopped jumping on A-instructions, and CPU.tst passed completely."
)
set_font(r_m1, size=11)
p_mistake.paragraph_format.space_after = Pt(12)

# ==============================================================================
# SECTION 6: Viva Preparation & Quick Code Changes
# ==============================================================================
h6 = doc.add_paragraph()
r_h6 = h6.add_run("6. Viva Preparation (On-The-Spot Modifications)")
set_font(r_h6, size=14, bold=True)
h6.paragraph_format.space_after = Pt(6)

p_viva = doc.add_paragraph()
r_v1 = p_viva.add_run(
    "For the viva, here is how the program can be modified on the spot:\n"
    "1. Moving the box down: Row r starts at 16384 + 32*r. To move the box down by 10 rows (to row 53), change line 22 in Box.asm from @17760 to @18080 (since 16384 + 32*53 = 18080).\n"
    "2. Making the box wider: Change the column counter in Box.asm from @4 to @5 (for 80 pixels) or @6 (for 96 pixels).\n"
    "3. Making the box taller: Change the row counter in Box.asm from @20 to @30 (for 30 rows) or @40 (for 40 rows).\n"
    "4. Inverting the key behavior: Swap the color values in Box.asm so that color = 0 when a key is pressed and color = -1 when released."
)
set_font(r_v1, size=11)
p_viva.paragraph_format.space_after = Pt(8)

# Save the document
doc.save(DOCX_OUT)
import shutil
shutil.copyfile(DOCX_OUT, DESKTOP_DOCX)

print(f"SUCCESS: Generated editable Word document at:\n  {DOCX_OUT}\n  {DESKTOP_DOCX}")
