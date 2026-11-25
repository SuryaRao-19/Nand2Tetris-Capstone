# 5-Minute Viva Defense & On-The-Spot Modification Guide
**Nand to Tetris – I (ETCCNT301) Capstone Project**  
**Student:** Surya Rao | **Roll No:** 2501730243 | **Personal Number ($K$):** 43  
**School of Engineering & Technology, K.R. Mangalam University**  

---

## 1. Quick 2-Minute Project Overview (What to Say)

> *"Good morning/afternoon, Sir/Ma'am. My capstone project implements the complete Hack computing stack for personal number K = 43 (derived from the last two digits of my roll number 2501730243):*
>
> 1. *In **Part A**, I integrated registers, ALU, RAM, Screen, and PC into `CPU.hdl`, `Memory.hdl`, and `Computer.hdl`. All five official test suites (`CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, and `ComputerRect.tst`) pass with 100% success.*
> 2. *In **Part B**, I wrote a two-pass assembler in Python (`assembler.py`). It resolves labels in pass 1, allocates variables starting at RAM address 16, and encodes C-instructions. For $K \pmod 3 = 43 \pmod 3 = 1$, I implemented clear line-numbered error reporting instead of crashing. It was verified bit-for-bit against the official Nand2Tetris assembler on `Add`, `Max`, `Rect`, and `Pong` (27,483 instructions).*
> 3. *In **Part C**, I wrote `Box.asm` to draw a black box starting at row K = 43, 20 rows tall, and 64 pixels wide ($16 \times ((43 \pmod 4) + 1) = 64$ pixels, which is 4 words per row from the left edge). It polls `RAM[24576]` (`KBD`) and dynamically toggles the box on key press and key release.*
> 4. *All files are organized in the `capstone/` folder."*

---

## 2. On-The-Spot Code Modifications (High Priority for Viva)

Examiners usually ask you to open your files and make one small change on the spot. Here are the exact modifications:

### Modification 1: "Move the box down (e.g. by 10 rows)"
- **Concept:** Screen row $r$ starts at `SCREEN + 32 * r`.
  - Currently row 43 starts at: `16384 + 32 * 43 = 17760`.
  - To move down by 10 rows (to row 53):
    `16384 + 32 * 53 = 16384 + 1696 = 18080` (or `17760 + 32 * 10 = 18080`).
- **Code change in `Box.asm` (around line 31):**
  ```assembly
  // ORIGINAL:
  (DRAW)
      @17760
      D=A
      @row_addr
      M=D

  // MODIFIED (Move down 10 rows):
  (DRAW)
      @18080      // SCREEN + 32 * 53 = 18080
      D=A
      @row_addr
      M=D
  ```
- **How to recompile & run:**
  ```powershell
  python assembler.py Box.asm Box.hack
  ```
  In CPU Emulator: Reload `Box.hack`, press key, box appears 10 rows lower!

---

### Modification 2: "Make the box wider (e.g. 5 words / 80 pixels)"
- **Concept:** The column counter controls how many 16-bit words are drawn per row.
- **Code change in `Box.asm` (around line 49):**
  ```assembly
  // ORIGINAL (4 words = 64 pixels):
      @4
      D=A
      @col_count
      M=D

  // MODIFIED (5 words = 80 pixels):
      @5
      D=A
      @col_count
      M=D
  ```

---

### Modification 3: "Make the box taller (e.g. 40 rows tall)"
- **Concept:** The row counter controls how many screen rows are rendered.
- **Code change in `Box.asm` (around line 37):**
  ```assembly
  // ORIGINAL (20 rows tall):
      @20
      D=A
      @row_count
      M=D

  // MODIFIED (40 rows tall):
      @40
      D=A
      @row_count
      M=D
  ```

---

### Modification 4: "Invert the behavior (box is normally black, disappears when key is pressed)"
- **Concept:** Swap the color values assigned during the keyboard branch.
- **Code change in `Box.asm` (lines 16-27):**
  ```assembly
  // ORIGINAL:
  (SET_BLACK)
      @color
      M=-1        // Key pressed -> Black
      @DRAW
      0;JMP
  (SET_WHITE)
      @color
      M=0         // Key released -> White

  // INVERTED:
  (SET_BLACK)
      @color
      M=0         // Key pressed -> White (box disappears)
      @DRAW
      0;JMP
  (SET_WHITE)
      @color
      M=-1        // Key released -> Black (box visible)
  ```

---

### Modification 5: "Shift the box horizontally away from the left edge (e.g., offset by 2 words / 32 pixels)"
- **Concept:** Instead of initializing `col_addr = row_addr`, add an offset of 2 words.
- **Code change in `Box.asm` (around line 45):**
  ```assembly
  // ORIGINAL:
      @row_addr
      D=M
      @col_addr
      M=D

  // MODIFIED (Offset 2 words to the right):
      @row_addr
      D=M
      @2
      D=D+A       // Add 2 words (32 pixels offset)
      @col_addr
      M=D
  ```

---

## 3. Frequently Asked Examiner Questions & Model Answers

### Q1: "Why does row r start at address SCREEN + 32 * r?"
**Answer:**
> *"The Hack screen has a resolution of 512 pixels horizontally by 256 pixels vertically. In the memory-mapped I/O scheme, each memory word contains 16 bits, representing 16 consecutive horizontal black/white pixels. Therefore, one complete row requires $512 / 16 = 32$ memory words. Because the screen memory map begins at RAM address 16384 (`0x4000`), row $r$ begins at address $16384 + 32 \times r$."*

### Q2: "How does your assembler handle symbols and labels?"
**Answer:**
> *"The assembler operates in two passes:*
> - *In **Pass 1**, it strips comments and whitespace. When it encounters a label declaration like `(LOOP)`, it adds `LOOP` to the symbol table with a value equal to the current ROM address of the very next instruction. Label declarations do not increment the ROM address.*
> - *In **Pass 2**, when encountering an `@symbol`, it first checks predefined symbols (like `SCREEN`, `KBD`, `R0-R15`) and label symbols. If the symbol is not in the table, it is a new variable; the assembler allocates the next free RAM address starting at 16, increments the variable counter, and records it in the symbol table."*

### Q3: "What extra feature did you implement in Part B and why?"
**Answer:**
> *"Based on my roll number 2501730243, my personal number is K = 43. $43 \pmod 3 = 1$. The required feature for remainder 1 is: 'For a wrong line, print a clear message with the line number instead of crashing.'*
> *My assembler tracks original source line numbers and checks for syntax errors, out-of-bounds constants, unrecognized computation mnemonics, or invalid jump directives. When an invalid instruction is encountered, it reports e.g. `Line 7: invalid instruction '...' (unrecognized computation)` to `stderr` and exits cleanly with returncode 1 without dumping Python stack traces."*

### Q4: "In CPU.hdl, how do you prevent A-instructions from causing accidental jumps?"
**Answer:**
> *"An A-instruction has bit 15 = 0, meaning bits 0 to 14 are address bits, not jump control lines. In my `CPU.hdl`, the jump evaluation logic combines ALU flags `zr` and `ng` with jump bits `instruction[0..2]`. However, this jump condition is gated using an `And` gate with `isC` (`instruction[15]`):*
> ```hdl
> And(a=isC, b=jumpCond, out=loadPC);
> ```
> *This ensures that jumps can only occur during C-instructions. For A-instructions, `loadPC` is always 0, and `incPC` is 1, so the Program Counter simply advances to the next instruction."*

### Q5: "How does Memory.hdl distinguish between RAM, Screen, and Keyboard?"
**Answer:**
> *"It uses the two highest address bits, `address[13..14]` (since total memory is 15-bit addressable):*
> - *`00` and `01`: Addresses 0 to 16,383 (RAM16K).*
> - *`10`: Addresses 16,384 to 24,575 (Screen memory map).*
> - *`11`: Address 24,576 (Keyboard register).*
> *A `DMux4Way` routes the `load` signal to the correct device, and a `Mux4Way16` selects the appropriate device output for the `out` bus."*

---

## 4. Key Commands Reference

To test everything in the terminal during the viva:

```powershell
# 1. Run all Part B assembler tests:
python test_assembler.py

# 2. Assemble Box.asm into Box.hack:
python assembler.py Box.asm Box.hack

# 3. Run CPU Emulator automated test on Box.hack:
..\tools\CPUEmulator.bat BoxTest.tst

# 4. Run Hardware Simulator on CPU tests:
..\tools\HardwareSimulator.bat CPU.tst
..\tools\HardwareSimulator.bat ComputerAdd.tst
..\tools\HardwareSimulator.bat ComputerMax.tst
..\tools\HardwareSimulator.bat ComputerRect.tst
```
