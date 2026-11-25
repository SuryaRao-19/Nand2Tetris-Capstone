#!/usr/bin/env python3
import sys
import os
import re

PREDEFINED_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}
for i in range(16):
    PREDEFINED_SYMBOLS[f"R{i}"] = i

COMP_TABLE = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}

DEST_TABLE = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "DM":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111",
}

JUMP_TABLE = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


class HackAssembler:
    def __init__(self, save_symbols=False, warn_duplicate_labels=True):
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.next_var_address = 16
        self.save_symbols = save_symbols
        self.warn_duplicate_labels = warn_duplicate_labels
        self.errors = []

    def clean_line(self, line: str) -> str:
        comment_idx = line.find("//")
        if comment_idx != -1:
            line = line[:comment_idx]
        return line.strip()

    def assemble(self, asm_filepath: str, output_filepath: str = None) -> bool:
        if not os.path.exists(asm_filepath):
            print(f"Error: File '{asm_filepath}' not found.", file=sys.stderr)
            return False

        if output_filepath is None:
            base, _ = os.path.splitext(asm_filepath)
            output_filepath = base + ".hack"

        with open(asm_filepath, "r", encoding="utf-8", errors="replace") as f:
            raw_lines = f.readlines()

        self.errors = []
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.next_var_address = 16

        rom_address = 0
        cleaned_instructions = []

        for line_num, raw_line in enumerate(raw_lines, start=1):
            cleaned = self.clean_line(raw_line)
            if not cleaned:
                continue

            if cleaned.startswith("(") and cleaned.endswith(")"):
                label = cleaned[1:-1].strip()
                if not label:
                    self.errors.append(f"Line {line_num}: invalid empty label declaration '()'")
                    continue

                if not re.match(r"^[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$", label):
                    self.errors.append(f"Line {line_num}: invalid label identifier '{label}'")
                    continue

                if label in self.symbol_table:
                    if self.warn_duplicate_labels:
                        print(f"Warning: Line {line_num}: label '({label})' already defined. Overwriting.", file=sys.stderr)
                self.symbol_table[label] = rom_address
            else:
                cleaned_instructions.append((line_num, cleaned))
                rom_address += 1

        machine_code_lines = []

        for line_num, instr in cleaned_instructions:
            if instr.startswith("@"):
                value_part = instr[1:].strip()
                if not value_part:
                    self.errors.append(f"Line {line_num}: invalid instruction '{instr}' (missing address/symbol after '@')")
                    continue

                if value_part.isdigit():
                    val = int(value_part)
                    if val < 0 or val > 32767:
                        self.errors.append(f"Line {line_num}: constant out of range 0..32767: '{instr}'")
                        continue
                    binary_code = format(val, "016b")
                    machine_code_lines.append(binary_code)
                else:
                    if not re.match(r"^[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$", value_part):
                        self.errors.append(f"Line {line_num}: invalid symbol name in instruction '{instr}'")
                        continue

                    if value_part not in self.symbol_table:
                        self.symbol_table[value_part] = self.next_var_address
                        self.next_var_address += 1

                    val = self.symbol_table[value_part]
                    binary_code = format(val, "016b")
                    machine_code_lines.append(binary_code)

            else:
                dest_part = ""
                comp_part = ""
                jump_part = ""

                rest = instr
                if "=" in rest:
                    dest_part, rest = rest.split("=", 1)
                    dest_part = dest_part.strip()

                if ";" in rest:
                    comp_part, jump_part = rest.split(";", 1)
                    comp_part = comp_part.strip()
                    jump_part = jump_part.strip()
                else:
                    comp_part = rest.strip()

                if comp_part not in COMP_TABLE:
                    self.errors.append(f"Line {line_num}: invalid instruction '{instr}' (unrecognized computation '{comp_part}')")
                    continue

                if dest_part not in DEST_TABLE:
                    self.errors.append(f"Line {line_num}: invalid instruction '{instr}' (unrecognized destination '{dest_part}')")
                    continue

                if jump_part not in JUMP_TABLE:
                    self.errors.append(f"Line {line_num}: invalid instruction '{instr}' (unrecognized jump directive '{jump_part}')")
                    continue

                comp_bits = COMP_TABLE[comp_part]
                dest_bits = DEST_TABLE[dest_part]
                jump_bits = JUMP_TABLE[jump_part]

                binary_code = "111" + comp_bits + dest_bits + jump_bits
                machine_code_lines.append(binary_code)

        if self.errors:
            print(f"Assembly failed with {len(self.errors)} error(s):", file=sys.stderr)
            for err in self.errors:
                print(f"  {err}", file=sys.stderr)
            return False

        with open(output_filepath, "w", encoding="utf-8") as f:
            for code in machine_code_lines:
                f.write(code + "\n")

        if self.save_symbols:
            symbols_file = os.path.join(os.path.dirname(output_filepath) or ".", "symbols.txt")
            with open(symbols_file, "w", encoding="utf-8") as f:
                f.write("# Symbol\tAddress\n")
                for sym, addr in sorted(self.symbol_table.items(), key=lambda item: (item[1], item[0])):
                    f.write(f"{sym}\t{addr}\n")

        return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <source.asm> [output.hack] [--symbols]")
        sys.exit(1)

    asm_file = sys.argv[1]
    out_file = None
    save_sym = "--symbols" in sys.argv

    if len(sys.argv) >= 3 and not sys.argv[2].startswith("--"):
        out_file = sys.argv[2]

    assembler = HackAssembler(save_symbols=save_sym)
    success = assembler.assemble(asm_file, out_file)
    if success:
        target = out_file if out_file else os.path.splitext(asm_file)[0] + ".hack"
        print(f"Success: Generated {target}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
