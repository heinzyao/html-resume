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

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{output.absolute()}")
            page.wait_for_load_state("networkidle")
            pdf_path = base / "resume.pdf"
            page.pdf(path=str(pdf_path), format="A4", print_background=True)
            browser.close()
        print(f"PDF:   {pdf_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build HTML resume from YAML data.")
    parser.add_argument("--pdf", action="store_true", help="Also export PDF via Playwright")
    args = parser.parse_args()
    build(pdf=args.pdf)
