import argparse
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


def build(pdf: bool = False) -> None:
    base = Path(__file__).parent
    data = yaml.safe_load((base / "resume_data.yaml").read_text(encoding="utf-8"))

    env = Environment(loader=FileSystemLoader(str(base)), autoescape=False)
    template = env.get_template("template.html")
    html = template.render(**data)

    output = base / "index.html"
    output.write_text(html, encoding="utf-8")
    print(f"Built: {output}")

    if pdf:
        from playwright.sync_api import sync_playwright

        # A4 高度（px，96 DPI）
        A4_H_PX = 297 / 25.4 * 96

        with sync_playwright() as p:
            # 以 A4 寬度作為 viewport，讓列印版面與 PDF 一致
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 794, "height": 1123})
            page.goto(f"file://{output.absolute()}")
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")   # 等字型載入

            # 重置所有 JS 套用的 zoom，讓 page.pdf(scale=) 單獨處理縮放
            # → Playwright 的 scale 參數能正確保留 PDF 連結 annotation
            page.evaluate("""() => {
                document.querySelector('.page-container').style.zoom = '';
                document.getElementById('print-scale-style').textContent = '';
            }""")

            # 量內容自然高度，計算縮放比例
            content_h = page.evaluate(
                "document.querySelector('.page-container').scrollHeight"
            )
            scale = min(1.0, A4_H_PX / content_h)
            print(f"Scale: {scale:.4f} (content {content_h:.0f}px → A4 {A4_H_PX:.0f}px)")

            pdf_path = base / "resume.pdf"
            page.pdf(
                path=str(pdf_path),
                format="A4",
                print_background=True,
                scale=round(scale, 5),
            )
            browser.close()
        print(f"PDF:   {pdf_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build HTML resume from YAML data.")
    parser.add_argument("--pdf", action="store_true", help="Also export PDF via Playwright")
    args = parser.parse_args()
    build(pdf=args.pdf)
