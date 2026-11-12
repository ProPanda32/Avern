from pathlib import Path
import json
import subprocess
import sys
import tempfile

source = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
if not source.is_file():
    raise SystemExit(f"Presentation not found: {source}")
output.mkdir(parents=True, exist_ok=True)

with tempfile.TemporaryDirectory() as temp:
    work = Path(temp)
    styled = work / 'styled.pptx'
    subprocess.run([sys.executable, 'scripts/style-slide-backgrounds.py', str(source), str(styled)], check=True)
    subprocess.run(
        ["libreoffice", f"-env:UserInstallation=file://{work / 'profile'}",
         "--headless", "--convert-to", "pdf", "--outdir", str(work), str(styled)],
        check=True,
    )
    pdf = work / 'styled.pdf'
    if not pdf.is_file():
        raise SystemExit("PowerPoint conversion did not produce a PDF")
    slide_text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True, capture_output=True, text=True).stdout
    print("SLIDE_TEXT_JSON=" + json.dumps([page.strip() for page in slide_text.split("\f") if page.strip()]))
    subprocess.run(
        ["pdftoppm", "-png", "-scale-to", "1600", str(pdf), str(output / "slide")],
        check=True,
    )

slides = sorted(output.glob("slide-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
if not slides:
    raise SystemExit("No slide images were rendered")
(output / "manifest.json").write_text(json.dumps([p.name for p in slides]), encoding="utf-8")
from PIL import Image
with Image.open(slides[1]) as preview:
    print(f"SLIDE_2_PIXELS corners={preview.getpixel((10,10))},{preview.getpixel((preview.width-10,10))} center={preview.getpixel((preview.width//2,preview.height//2))}")
print(f"Rendered {len(slides)} presentation slides")
