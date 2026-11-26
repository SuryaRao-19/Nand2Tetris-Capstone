#!/usr/bin/env python3
import os
import re
import base64
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(BASE_DIR, "REPORT.html")
STANDALONE_HTML = os.path.join(BASE_DIR, "REPORT_STANDALONE.html")
OUTPUT_PDF = os.path.join(BASE_DIR, "Capstone_Report_2501730243_Surya_Rao.pdf")
DESKTOP_PDF = os.path.join("C:\\Users\\Surya Rao\\Desktop", "Capstone_Report_2501730243_Surya_Rao.pdf")
REPORT_PDF = os.path.join(BASE_DIR, "REPORT.pdf")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace image sources with base64 data URIs
def img_replace(match):
    src = match.group(1)
    full_path = os.path.join(BASE_DIR, src)
    if os.path.exists(full_path):
        with open(full_path, "rb") as img_f:
            b64 = base64.b64encode(img_f.read()).decode("utf-8")
        return f'src="data:image/png;base64,{b64}"'
    return match.group(0)

standalone_content = re.sub(r'src="(screenshots/[^"]+)"', img_replace, content)

# Enhance print styling
print_style = """
<style>
@page {
  size: A4;
  margin: 12mm 15mm 15mm 15mm;
}
@media print {
  body {
    font-size: 11pt;
    line-height: 1.45;
  }
  h1 { font-size: 19pt; margin-bottom: 4px; }
  h2 { font-size: 14pt; margin-top: 16px; margin-bottom: 6px; }
  h3 { font-size: 12pt; margin-top: 12px; margin-bottom: 4px; }
  .img-card {
    page-break-inside: avoid;
    margin: 10px 0;
    padding: 6px;
  }
  .img-card img {
    max-height: 250px;
    width: auto;
  }
  .data-table, .meta-table, .callout, .callout-warning {
    page-break-inside: avoid;
    font-size: 9.5pt;
  }
  .callout, .callout-warning {
    padding: 8px 12px;
    margin: 10px 0;
  }
}
</style>
"""
standalone_content = standalone_content.replace("</head>", f"{print_style}\n</head>")

with open(STANDALONE_HTML, "w", encoding="utf-8") as f:
    f.write(standalone_content)

print(f"Generated standalone HTML: {STANDALONE_HTML}")

# Try Chrome first, then Edge
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
browser_path = chrome_path if os.path.exists(chrome_path) else edge_path

cmd = [
    browser_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={OUTPUT_PDF}",
    STANDALONE_HTML
]

print(f"Running browser to compile PDF: {browser_path}")
res = subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(OUTPUT_PDF):
    size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    print(f"SUCCESS: Created PDF at {OUTPUT_PDF} ({size_mb:.2f} MB)")
    
    # Copy to Desktop and REPORT.pdf
    import shutil
    shutil.copyfile(OUTPUT_PDF, DESKTOP_PDF)
    shutil.copyfile(OUTPUT_PDF, REPORT_PDF)
    print(f"Copied to Desktop: {DESKTOP_PDF}")
    print(f"Copied to REPORT.pdf: {REPORT_PDF}")
else:
    print(f"Failed to generate PDF: {res.stderr}")
