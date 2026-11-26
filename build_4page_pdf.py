#!/usr/bin/env python3
import os
import re
import base64
import subprocess
import shutil

BASE_DIR = r"c:\Users\Surya Rao\Desktop\nand2tetris\Capstone"
SRC_HTML = os.path.join(BASE_DIR, "REPORT_4PAGES.html")
OUT_HTML = os.path.join(BASE_DIR, "REPORT_4PAGES_STANDALONE.html")
OUT_PDF = os.path.join(BASE_DIR, "Capstone_Report_2501730243_Surya_Rao.pdf")
DESKTOP_PDF = r"C:\Users\Surya Rao\Desktop\Capstone_Report_2501730243_Surya_Rao.pdf"
REPORT_PDF = os.path.join(BASE_DIR, "REPORT.pdf")

with open(SRC_HTML, "r", encoding="utf-8") as f:
    content = f.read()

def replace_img(m):
    rel = m.group(1)
    p = os.path.join(BASE_DIR, rel)
    with open(p, "rb") as f_img:
        b = base64.b64encode(f_img.read()).decode("utf-8")
    return f'src="data:image/png;base64,{b}"'

content = re.sub(r'src="(screenshots/[^"]+)"', replace_img, content)

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(content)

chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={OUT_PDF}", OUT_HTML]
subprocess.run(cmd, check=True)

shutil.copyfile(OUT_PDF, DESKTOP_PDF)
shutil.copyfile(OUT_PDF, REPORT_PDF)

with open(OUT_PDF, "rb") as f:
    pdf_bytes = f.read()

m = re.search(rb'/Count\s+(\d+)', pdf_bytes)
count = m.group(1).decode() if m else "Unknown"
print("SUCCESS!")
print(f"Page Count: {count}")
print(f"File Size: {os.path.getsize(OUT_PDF) / (1024*1024):.2f} MB")
print(f"Saved to: {OUT_PDF}")
print(f"Saved to Desktop: {DESKTOP_PDF}")
