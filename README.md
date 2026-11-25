# Nand to Tetris – I Capstone Project: Make the Computer Draw a Box
**Course:** ETCCNT301 | **School of Engineering & Technology, K.R. Mangalam University**  
**Student:** Surya Rao | **Roll Number:** 2501730243 | **Personal Number ($K$):** 43  

---

## 📌 Project Overview
This repository contains the complete Capstone Project for **Nand to Tetris – I**:
- **Part A – Build the Computer:** Synthesized `CPU.hdl`, `Memory.hdl`, and `Computer.hdl`. Verified against official test suites (`CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, `ComputerRect.tst`).
- **Part B – Hack Assembler:** Python implementation (`assembler.py`) with two-pass parsing, symbol tables, variable allocation, and the student-specific feature ($K \pmod 3 = 1$: graceful line-number error reporting). Verified bit-for-bit against official benchmarks (`Add`, `Max`, `Rect`, `Pong`).
- **Part C – Interactive Box Program:** Low-level Hack assembly (`Box.asm`) and assembled machine code (`Box.hack`). Renders a 64px × 20px black box starting at row 43 from the left edge when any key is pressed, clearing upon key release.

---

## 📐 Student-Specific Parameters ($K = 43$)

- **Roll Number:** `2501730243` $\implies$ Last two digits: **$K = 43$**
- **$K \pmod 3 = 43 \pmod 3 = 1$:** Assembler error handling feature (clear message with line number instead of crashing).
- **$K \pmod 4 = 43 \pmod 4 = 3$:** Box width: $16 \times ((3) + 1) = 64$ pixels (4 words per row from left edge).
- **Starting Row:** Row $K = 43$ (Screen RAM address: $\text{SCREEN} + 32 \times 43 = 16384 + 1376 = \mathbf{17760}$).
- **Box Height:** 20 rows tall (rows 43 to 62).
- **Total Drawing Span:** Memory words `17760` through `18371`.

---

## 📂 Folder Structure

```text
Capstone/
├── CPU.hdl                     # Part A: Hack CPU implementation
├── Memory.hdl                  # Part A: Memory-mapped I/O and RAM controller
├── Computer.hdl                # Part A: Top-level Hack Computer chip
├── assembler.py                # Part B: Custom Hack assembler with K mod 3 = 1 feature
├── test_assembler.py           # Part B: Automated regression test suite
├── Box.asm                     # Part C: Box drawing Hack assembly program
├── Box.hack                    # Part C: Assembled binary machine code
├── BoxTest.tst                 # Automated regression test for CPUEmulator
├── BoxTest.cmp                 # Expected output comparison for CPUEmulator
├── REPORT.md                   # 3-4 page Short Report (Markdown format)
├── REPORT.html                 # 3-4 page Short Report (Printable HTML format)
├── VIVA_PREPARATION.md         # 5-minute Viva defense & live modification guide
├── generate_report_visuals.py  # Visual screenshot generation script
├── screenshots/                # High-resolution test & emulator screenshots
│   ├── cpu_test_pass.png
│   ├── memory_test_pass.png
│   ├── computer_add_pass.png
│   ├── computer_max_pass.png
│   ├── computer_rect_pass.png
│   ├── assembler_verification.png
│   └── cpu_emulator_box.png
└── symbols.txt                 # Exported Hack assembler symbol table
```

---

## 🚀 How to Run & Verify

### 1. Run Part A Hardware Tests
```powershell
..\tools\HardwareSimulator.bat CPU.tst
..\tools\HardwareSimulator.bat Memory.tst
..\tools\HardwareSimulator.bat ComputerAdd.tst
..\tools\HardwareSimulator.bat ComputerMax.tst
..\tools\HardwareSimulator.bat ComputerRect.tst
```

### 2. Run Part B Assembler & Verification
```powershell
# Run the automated assembler test suite (compares Add, Max, Rect, Pong bit-for-bit):
python test_assembler.py

# Assemble any file:
python assembler.py Box.asm Box.hack --symbols
```

### 3. Run Part C Box Program
```powershell
# Automated regression test on CPU Emulator:
..\tools\CPUEmulator.bat BoxTest.tst

# Or launch CPU Emulator interactive GUI:
..\tools\CPUEmulator.bat
# (Load Box.hack, select View -> Screen, set Animation to No Animation, and run!)
```

---

## 📝 Submissions
1. **GitHub:** This `capstone/` folder contains all required files (`CPU.hdl`, `Memory.hdl`, `Computer.hdl`, `assembler.py`, `Box.asm`, `Box.hack`).
2. **ZOSIMA Report:** Open `REPORT.html` in your browser and click "Print / Save as PDF" or view `REPORT.md`.
3. **Viva Prep:** Review `VIVA_PREPARATION.md` for fast answers and live modification recipes.
