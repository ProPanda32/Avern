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
    subprocess.run(
        ["libreoffice", f"-env:UserInstallation=file://{work / 'profile'}",
         "--headless", "--convert-to", "pdf", "--outdir", str(work), str(source)],
        check=True,
    )
    pdf = work / (source.stem + ".pdf")
    if not pdf.is_file():
        raise SystemExit("PowerPoint conversion did not produce a PDF")
    subprocess.run(
        ["pdftoppm", "-png", "-scale-to", "1600", str(pdf), str(output / "slide")],
        check=True,
    )

slides = sorted(output.glob("slide-*.png"), key=lambda p: int(p.stem.split("-")[-1]))
if not slides:
    raise SystemExit("No slide images were rendered")
(output / "manifest.json").write_text(json.dumps([p.name for p in slides]), encoding="utf-8")
print(f"Rendered {len(slides)} presentation slides")
