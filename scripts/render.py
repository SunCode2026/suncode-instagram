"""Render every <section class="sc-slide"> of an HTML file to 1080x1350 PNGs.
usage: python3 render.py slides.html outdir [brand_dir]
brand_dir holds tokens.json, bundle.css, fonts/ClashDisplay-*.otf, logo-blanco.png, logo-color.png.
In the slides, write <img class="sc-logo" src="LOGO">: white logo on gradient, colour logo on cream."""
import json, re, sys, pathlib
from playwright.sync_api import sync_playwright

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
brand = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else pathlib.Path(__file__).parent.parent / "brand").resolve()
tokens = json.loads((brand / "tokens.json").read_text())
css = (brand / "bundle.css").read_text().replace("../fonts/", "fonts/")
vars_ = "".join(f"--{t['name']}:{t['value']};" for fam in ("color", "radius", "spacing") for t in tokens[fam]["tokens"])

slides = re.findall(r'<section class="sc-slide.*?</section>', src.read_text(), re.S)
assert slides, "no sc-slide sections found"
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, s in enumerate(slides, 1):
        logo = "logo-color.png" if "sc-cream" in s.split(">", 1)[0] else "logo-blanco.png"
        s = s.replace('src="LOGO"', f'src="{logo}"')
        page = brand / "_render.html"  # file:// page so fonts and logos load from brand_dir
        page.write_text(f'<html><head><meta charset="utf-8"><style>:root{{{vars_}}}body{{margin:0}}{css}</style></head><body>{s}</body></html>')
        pg.goto(page.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        assert pg.evaluate("document.fonts.check('500 40px \"Clash Display\"')"), "Clash Display did not load"
        pg.locator(".sc-slide").screenshot(path=str(out / f"{i:02d}.jpg"), type="jpeg", quality=95)  # Instagram API only takes JPEG
    b.close()
print(f"{len(slides)} slides -> {out}")
