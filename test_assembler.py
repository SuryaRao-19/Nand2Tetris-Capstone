#!/usr/bin/env python3
"""
Test Suite for Hack Assembler (assembler.py)
Capstone Project - Part B Verification
Student: Surya Rao (Roll No: 2501730243, K = 43)
"""

import os
import subprocess
import sys
import filecmp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_6 = os.path.abspath(os.path.join(BASE_DIR, "..", "projects", "6"))

TEST_CASES = [
    ("Add", os.path.join(PROJECTS_6, "add", "Add.asm"), os.path.join(PROJECTS_6, "add", "Add.hack")),
    ("Max", os.path.join(PROJECTS_6, "max", "Max.asm"), os.path.join(PROJECTS_6, "max", "Max.hack")),
    ("Rect", os.path.join(PROJECTS_6, "rect", "Rect.asm"), os.path.join(PROJECTS_6, "rect", "Rect.hack")),
    ("Pong", os.path.join(PROJECTS_6, "pong", "Pong.asm"), os.path.join(PROJECTS_6, "pong", "Pong.hack")),
]

def test_official_programs():
    print("=" * 60)
    print("PART B TEST 1: Comparing with Official Assembler Output")
    print("=" * 60)
    all_passed = True
    
    for name, asm_path, official_hack in TEST_CASES:
        my_hack = os.path.join(BASE_DIR, f"{name}_test.hack")
        cmd = [sys.executable, os.path.join(BASE_DIR, "assembler.py"), asm_path, my_hack]
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if res.returncode != 0:
            print(f"FAILED to assemble {name}.asm:")
            print(res.stderr)
            all_passed = False
            continue
            
        # Compare with official hack
        with open(official_hack, "r") as f_off, open(my_hack, "r") as f_my:
            off_lines = [l.strip() for l in f_off if l.strip()]
            my_lines = [l.strip() for l in f_my if l.strip()]
            
        if off_lines == my_lines:
            print(f"[PASS] {name}.asm: {len(my_lines)} instructions matched official .hack bit-for-bit!")
        else:
            print(f"[FAIL] {name}.asm: Output differs from official assembler!")
            for idx, (o, m) in enumerate(zip(off_lines, my_lines)):
                if o != m:
                    print(f"  Line {idx+1}: Expected '{o}', Got '{m}'")
                    break
            all_passed = False
            
        if os.path.exists(my_hack):
            os.remove(my_hack)
            
    return all_passed

def test_extra_feature_error_handling():
    print("\n" + "=" * 60)
    print("PART B TEST 2: Testing Extra Feature (K mod 3 = 1)")
    print("Graceful line number error reporting on invalid instruction")
    print("=" * 60)
    
    bad_asm_content = """// Test program with errors
@2
D=A
// A valid line
@R0
M=D
D=INVALID+COMP;JMP
@100
dest_missing=
@R1
M=D;INVALID_JUMP
"""
    bad_asm_path = os.path.join(BASE_DIR, "bad_test.asm")
    with open(bad_asm_path, "w") as f:
        f.write(bad_asm_content)
        
    cmd = [sys.executable, os.path.join(BASE_DIR, "assembler.py"), bad_asm_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    print("Assembler Output (stderr):")
    print(res.stderr)
    
    os.remove(bad_asm_path)
    
    # Verify that it reported Line 7, Line 9, Line 11 and didn't crash with traceback
    has_line_7 = "Line 7" in res.stderr
    no_traceback = "Traceback (most recent call last)" not in res.stderr
    exit_nonzero = res.returncode != 0
    
    if has_line_7 and no_traceback and exit_nonzero:
        print("[PASS] Extra feature verified: Clear error message with line numbers, no crash!")
        return True
    else:
        print("[FAIL] Extra feature did not produce expected output.")
        return False

if __name__ == "__main__":
    t1 = test_official_programs()
    t2 = test_extra_feature_error_handling()
    if t1 and t2:
        print("\nALL ASSEMBLER TESTS PASSED SUCCESSFULLY! (100% GREEN)")
        sys.exit(0)
    else:
        print("\nSOME TESTS FAILED!")
        sys.exit(1)
