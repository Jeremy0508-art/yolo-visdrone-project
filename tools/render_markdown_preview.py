"""Render a simple standalone HTML preview for the paper Markdown draft.

This intentionally avoids external dependencies so the paper can be previewed
on a clean Windows environment.
"""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import re


CSS = """
body {
  max-width: 980px;
  margin: 40px auto;
  padding: 0 24px;
  font-family: "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif;
  line-height: 1.75;
  color: #1f2933;
}
h1 {
  text-align: center;
  margin-bottom: 28px;
}
h1, h2, h3 {
  color: #102a43;
  line-height: 1.35;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 18px 0 28px;
  font-size: 14px;
}
th, td {
  border: 1px solid #bcccdc;
  padding: 7px 9px;
  text-align: left;
  vertical-align: top;
}
th {
  background: #f0f4f8;
}
p {
  margin: 0 0 14px;
}
ol {
  margin: 0 0 18px 24px;
}
code {
  background: #f0f4f8;
  border-radius: 4px;
  padding: 1px 4px;
}
figure {
  margin: 24px 0 30px;
  text-align: center;
}
figure img {
  max-width: 100%;
  height: auto;
  border: 1px solid #d9e2ec;
}
figcaption {
  margin-top: 8px;
  color: #52606d;
  font-size: 14px;
}
"""


def convert_inline(text: str) -> str:
    """Escape text and handle simple inline code spans."""
    parts = text.split("`")
    rendered: list[str] = []
    for index, part in enumerate(parts):
        if index % 2:
            rendered.append(f"<code>{escape(part)}</code>")
        else:
            rendered.append(escape(part))
    return "".join(rendered)


def render_image(stripped: str) -> str | None:
    match = re.fullmatch(r"!\[(?P<alt>.*)\]\((?P<src>[^)]+)\)", stripped)
    if not match:
        return None
    alt = match.group("alt").strip()
    src = match.group("src").strip()
    return (
        "<figure>"
        f"<img src='{escape(src, quote=True)}' alt='{escape(alt, quote=True)}'>"
        f"<figcaption>{convert_inline(alt)}</figcaption>"
        "</figure>"
    )


def is_table_separator(cells: list[str]) -> bool:
    return all(set(cell.replace(":", "").replace("-", "").strip()) <= set() for cell in cells)


def render_markdown(markdown: str) -> str:
    html: list[str] = []
    in_table = False
    in_ol = False

    def close_blocks() -> None:
        nonlocal in_table, in_ol
        if in_table:
            html.append("</tbody></table>")
            in_table = False
        if in_ol:
            html.append("</ol>")
            in_ol = False

    for raw in markdown.splitlines():
        stripped = raw.strip()
        if not stripped:
            close_blocks()
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if is_table_separator(cells):
                continue
            if not in_table:
                close_blocks()
                html.append("<table><tbody>")
                in_table = True
                html.append("<tr>" + "".join(f"<th>{convert_inline(cell)}</th>" for cell in cells) + "</tr>")
            else:
                html.append("<tr>" + "".join(f"<td>{convert_inline(cell)}</td>" for cell in cells) + "</tr>")
            continue

        image_html = render_image(stripped)
        if image_html is not None:
            close_blocks()
            html.append(image_html)
        elif len(stripped) > 3 and stripped[0].isdigit() and stripped[1:3] == ". ":
            if in_table:
                html.append("</tbody></table>")
                in_table = False
            if not in_ol:
                html.append("<ol>")
                in_ol = True
            html.append(f"<li>{convert_inline(stripped[3:])}</li>")
        elif stripped.startswith("# "):
            close_blocks()
            html.append(f"<h1>{convert_inline(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            close_blocks()
            html.append(f"<h2>{convert_inline(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            close_blocks()
            html.append(f"<h3>{convert_inline(stripped[4:])}</h3>")
        else:
            close_blocks()
            html.append(f"<p>{convert_inline(stripped)}</p>")

    close_blocks()
    return "".join(html)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="paper/manuscript_polished.md", help="Markdown input file.")
    parser.add_argument("--output", default="paper/manuscript_polished.html", help="HTML output file.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    markdown = input_path.read_text(encoding="utf-8")
    body = render_markdown(markdown)
    html = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>YOLO VisDrone Manuscript</title>"
        f"<style>{CSS}</style></head><body>{body}</body></html>"
    )
    output_path.write_text(html, encoding="utf-8")
    print(output_path.resolve())


if __name__ == "__main__":
    main()
