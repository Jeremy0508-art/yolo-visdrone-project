from __future__ import annotations

import re
import shutil
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "paper/templates"
TEX_PATH = ROOT / "paper/manuscript_submission_candidate.tex"
OUTPUT_DIR = ROOT / "paper/cea_template_migration"
OUTPUT_DOCX = OUTPUT_DIR / "manuscript_cea_template_draft.docx"
REPORT_PATH = OUTPUT_DIR / "cea_word_migration_audit.md"


MACROS = {
    r"\YOLOBase": "YOLO11n",
    r"\YOLOPtwo": "YOLO11n-P2",
    r"\YOLOPtwoNine": "YOLO11n-P2-960",
    r"\YOLOPtwoCA": "YOLO11n-P2-CA",
    r"\YOLOPtwoCANine": "YOLO11n-P2-CA-960",
    r"\YOLOPtwoCASmall": "YOLO11n-P2-CA-SmallObjAug",
    r"\YOLOEightN": "YOLOv8n",
    r"\YOLOElevenS": "YOLO11s",
    r"\CoordAtt": "CoordAttention",
}

EN_TABLE_CAPTIONS = {
    "YOLO11n 与改进模型的结构差异对比": "Structural differences between YOLO11n and the improved model",
    "实验环境与训练配置": "Experimental environment and training configuration",
    "不同模型在 VisDrone 验证集上的检测结果对比": "Detection results of different models on the VisDrone validation set",
    "外部参考基线在 VisDrone 验证集上的结果": "Results of external reference baselines on the VisDrone validation set",
    "改进模块消融实验结果": "Ablation results of the improved modules",
    "VisDrone YOLO 格式标注中的目标尺度分布": "Object-scale distribution in VisDrone YOLO-format annotations",
    "不同尺度目标的验证集匹配结果": "Validation-set matching results for objects at different scales",
    "YOLO11n-P2-CA-960 在 VisDrone 验证集上的类别级结果": "Class-level results of YOLO11n-P2-CA-960 on the VisDrone validation set",
    "不同模型复杂度与推理速度对比": "Comparison of model complexity and inference speed",
    "复杂场景中的典型误检与漏检原因分析": "Typical false-detection and missed-detection causes in complex scenes",
}

EN_FIGURE_CAPTIONS = {
    "YOLO11n-P2-CA-960 结构示意图": "Architecture overview of YOLO11n-P2-CA-960",
    "YOLO11n-P2-CA-960 训练与验证曲线": "Training and validation curves of YOLO11n-P2-CA-960",
    "VisDrone 训练集和验证集目标尺度分布": "Object-scale distribution of the VisDrone training and validation sets",
    "YOLO11n 与 YOLO11n-P2-CA-960 在不同尺度目标上的召回率对比": "Recall comparison between YOLO11n and YOLO11n-P2-CA-960 for different object scales",
    "VisDrone 验证集密集交通场景检测示例": "Detection example for a dense traffic scene in the VisDrone validation set",
    "复杂场景下极小目标、密集遮挡和类别混淆示例": "Examples of tiny objects, dense occlusion, and class confusion in complex scenes",
}

EN_TITLE = "Lightweight YOLO11n Improvement for Small Object Detection in UAV Aerial Images"
EN_ABSTRACT = (
    "UAV aerial images usually contain small-scale objects, dense distributions, frequent occlusion, "
    "and complex backgrounds, which require real-time detectors to preserve fine spatial details. "
    "For the VisDrone detection scenario, this study takes YOLO11n as the baseline and evaluates a "
    "lightweight improved model that combines a P2 high-resolution detection branch, CoordAttention, "
    "and a 960 input resolution. The P2 branch enhances shallow high-resolution features, CoordAttention "
    "introduces direction-aware positional information, and the higher input resolution increases the "
    "effective pixels of small objects. The validation results show that the 960 input resolution is the "
    "dominant source of performance gain, while the P2 branch further improves localization quality. "
    "Among nano-scale lightweight models, YOLO11n-P2-960 achieves the best mAP50 of 0.424 and mAP50-95 "
    "of 0.256, outperforming YOLO11n-960 and YOLO11n-P2-CA-960 while maintaining 55.68 FPS. The larger "
    "YOLO11s-960 obtains 0.489 mAP50 and 0.298 mAP50-95, indicating that model capacity remains an "
    "important factor for accuracy improvement. Therefore, the results should be interpreted as an "
    "accuracy-complexity trade-off dominated by high-resolution input, supplemented by the P2 branch, "
    "with limited gains from the attention module under the current setting."
)


@dataclass
class ParagraphBlock:
    kind: str
    text: str
    level: int = 0


@dataclass
class TableBlock:
    caption: str
    rows: list[list[str]]
    label: str = ""


@dataclass
class FigureBlock:
    caption: str
    image_path: str | None
    label: str = ""
    fallback_text: list[str] = field(default_factory=list)


Block = ParagraphBlock | TableBlock | FigureBlock


def template_path() -> Path:
    templates = sorted(TEMPLATE_DIR.glob("*.docx"))
    if not templates:
        raise FileNotFoundError("No CEA Word template found in paper/templates")
    return templates[0]


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if "%" in line and not line.lstrip().startswith("%"):
            # Keep escaped percent signs.
            parts = re.split(r"(?<!\\)%", line, maxsplit=1)
            line = parts[0]
        lines.append(line)
    return "\n".join(lines)


def macro_clean(text: str) -> str:
    for macro, value in sorted(MACROS.items(), key=lambda item: len(item[0]), reverse=True):
        text = re.sub(re.escape(macro) + r"\s*\{\}", value, text)
        text = text.replace(macro, value)
    return text


def command_arg(text: str, command: str, start: int = 0) -> tuple[str, int] | None:
    pos = text.find(command, start)
    if pos < 0:
        return None
    brace = text.find("{", pos + len(command))
    if brace < 0:
        return None
    depth = 0
    for idx in range(brace, len(text)):
        ch = text[idx]
        if ch == "{" and (idx == 0 or text[idx - 1] != "\\"):
            depth += 1
        elif ch == "}" and (idx == 0 or text[idx - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return text[brace + 1 : idx], idx + 1
    return None


def clean_latex(text: str, citation_map: dict[str, int] | None = None, label_map: dict[str, str] | None = None) -> str:
    text = macro_clean(text)
    text = text.replace("~", " ")
    text = text.replace(r"\%", "%").replace(r"\_", "_").replace(r"\&", "&")
    text = text.replace("--", "-")
    text = re.sub(r"\\mbox\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\heiti\s*", "", text)
    text = re.sub(r"\\textbf\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\emph\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\url\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\Delta", "Δ", text)
    text = re.sub(r"\\times", "×", text)
    text = re.sub(r"\\quad", " ", text)
    text = re.sub(r"\\noindent", "", text)
    text = re.sub(r"\\small", "", text)
    text = re.sub(r"\\centering", "", text)
    text = re.sub(r"\\label\{[^{}]*\}", "", text)

    if citation_map:
        def repl_cite(match: re.Match[str]) -> str:
            keys = [key.strip() for key in match.group(1).split(",")]
            nums = [str(citation_map[key]) for key in keys if key in citation_map]
            return "[" + ",".join(nums) + "]" if nums else ""
        text = re.sub(r"\\cite\{([^{}]+)\}", repl_cite, text)
    else:
        text = re.sub(r"\\cite\{([^{}]+)\}", "", text)

    if label_map:
        def repl_ref(match: re.Match[str]) -> str:
            return label_map.get(match.group(1), "")
        text = re.sub(r"\\ref\{([^{}]+)\}", repl_ref, text)
    else:
        text = re.sub(r"\\ref\{([^{}]+)\}", "", text)

    text = re.sub(r"\$([^$]*)\$", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+(?:\[[^\]]*\])?(?:\{[^{}]*\})?", "", text)
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_braced(line: str, command: str) -> str:
    result = command_arg(line, command)
    return result[0].strip() if result else ""


def extract_bibliography(tex: str) -> tuple[dict[str, int], list[tuple[int, str]]]:
    citation_map: dict[str, int] = {}
    entries: list[tuple[int, str]] = []
    match = re.search(r"\\begin\{thebibliography\}\{99\}(.+?)\\end\{thebibliography\}", tex, flags=re.S)
    if not match:
        return citation_map, entries
    body = match.group(1)
    parts = re.split(r"\\bibitem\{([^{}]+)\}", body)
    number = 0
    for idx in range(1, len(parts), 2):
        key = parts[idx]
        content = parts[idx + 1].strip()
        number += 1
        citation_map[key] = number
        content = clean_latex(content)
        entries.append((number, content))
    return citation_map, entries


def first_pass_label_map(tex: str) -> dict[str, str]:
    labels: dict[str, str] = {}
    table_idx = 0
    figure_idx = 0
    for block in re.finditer(r"\\begin\{(table|figure)\}.*?\\end\{\1\}", tex, flags=re.S):
        env = block.group(1)
        content = block.group(0)
        label_match = re.search(r"\\label\{([^{}]+)\}", content)
        if env == "table":
            table_idx += 1
            if label_match:
                labels[label_match.group(1)] = str(table_idx)
        else:
            figure_idx += 1
            if label_match:
                labels[label_match.group(1)] = str(figure_idx)
    return labels


def parse_table(content: str, citation_map: dict[str, int], label_map: dict[str, str]) -> TableBlock:
    caption_result = command_arg(content, r"\caption")
    caption = clean_latex(caption_result[0], citation_map, label_map) if caption_result else "未命名表"
    label_match = re.search(r"\\label\{([^{}]+)\}", content)
    tab_begin = content.find(r"\begin{tabular}")
    tab_end = content.find(r"\end{tabular}")
    rows: list[list[str]] = []
    if tab_begin >= 0 and tab_end > tab_begin:
        first_line_end = content.find("\n", tab_begin)
        if first_line_end < 0 or first_line_end > tab_end:
            first_line_end = tab_begin
        tab = content[first_line_end:tab_end]
        tab = re.sub(r"\\(toprule|midrule|bottomrule)", "", tab)
        raw_rows = re.split(r"\\\\", tab)
        for raw in raw_rows:
            raw = raw.strip()
            if not raw:
                continue
            cells = [clean_latex(cell.strip(), citation_map, label_map) for cell in raw.split("&")]
            cells = [cell for cell in cells if cell]
            if cells:
                rows.append(cells)
    return TableBlock(caption=caption, rows=rows, label=label_match.group(1) if label_match else "")


def parse_figure(content: str, citation_map: dict[str, int], label_map: dict[str, str]) -> FigureBlock:
    caption_result = command_arg(content, r"\caption")
    caption = clean_latex(caption_result[0], citation_map, label_map) if caption_result else "未命名图"
    label_match = re.search(r"\\label\{([^{}]+)\}", content)
    img_match = re.search(r"\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}", content)
    image_path = img_match.group(1) if img_match else None
    if image_path is None and label_match and label_match.group(1) == "fig:method_overview":
        image_path = "figures/method/hrpca_yolo11n_overview.png"

    fallback: list[str] = []
    if image_path is None:
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("\\"):
                continue
            cleaned = clean_latex(line, citation_map, label_map)
            if cleaned:
                fallback.append(cleaned)
    return FigureBlock(caption=caption, image_path=image_path, label=label_match.group(1) if label_match else "", fallback_text=fallback)


def parse_blocks(tex: str, citation_map: dict[str, int], label_map: dict[str, str]) -> tuple[str, str, list[Block], list[tuple[int, str]]]:
    title = ""
    title_result = command_arg(tex, r"\title")
    if title_result:
        title = clean_latex(title_result[0], citation_map, label_map)

    abstract = ""
    abs_match = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", tex, flags=re.S)
    if abs_match:
        abstract_text = abs_match.group(1)
        keyword_match = re.search(r"\\textbf\{关键词：\}(.+)", abstract_text)
        if keyword_match:
            abstract_text = abstract_text[: keyword_match.start()]
        abstract = clean_latex(abstract_text, citation_map, label_map)

    keywords = "无人机目标检测；小目标检测；YOLO11n；CoordAttention；VisDrone"
    if abs_match:
        keyword_match = re.search(r"关键词：\}(.+)", abs_match.group(1))
        if keyword_match:
            keywords = clean_latex(keyword_match.group(1), citation_map, label_map)

    body_match = re.search(r"\\end\{abstract\}(.+?)\\begin\{thebibliography\}", tex, flags=re.S)
    body = body_match.group(1) if body_match else tex

    blocks: list[Block] = []
    section_counter = 0
    subsection_counter = 0
    intro_mode = False

    lines = body.splitlines()
    i = 0
    pending_para: list[str] = []

    def flush_para() -> None:
        nonlocal pending_para
        if not pending_para:
            return
        text = clean_latex(" ".join(pending_para), citation_map, label_map)
        if text:
            blocks.append(ParagraphBlock("p", text))
        pending_para = []

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            flush_para()
            i += 1
            continue

        if line.startswith(r"\section{"):
            flush_para()
            title_text = clean_latex(extract_braced(line, r"\section"), citation_map, label_map)
            if title_text == "引言":
                intro_mode = True
            else:
                intro_mode = False
                section_counter += 1
                subsection_counter = 0
                blocks.append(ParagraphBlock("heading1", f"{section_counter} {title_text}", level=1))
            i += 1
            continue

        if line.startswith(r"\subsection{"):
            flush_para()
            subsection_counter += 1
            title_text = clean_latex(extract_braced(line, r"\subsection"), citation_map, label_map)
            if section_counter:
                blocks.append(ParagraphBlock("heading2", f"{section_counter}.{subsection_counter} {title_text}", level=2))
            else:
                blocks.append(ParagraphBlock("heading2", title_text, level=2))
            i += 1
            continue

        if line.startswith(r"\begin{table}"):
            flush_para()
            env = [line]
            i += 1
            while i < len(lines):
                env.append(lines[i])
                if r"\end{table}" in lines[i]:
                    break
                i += 1
            blocks.append(parse_table("\n".join(env), citation_map, label_map))
            i += 1
            continue

        if line.startswith(r"\begin{figure}"):
            flush_para()
            env = [line]
            i += 1
            while i < len(lines):
                env.append(lines[i])
                if r"\end{figure}" in lines[i]:
                    break
                i += 1
            blocks.append(parse_figure("\n".join(env), citation_map, label_map))
            i += 1
            continue

        if line.startswith(r"\begin{enumerate}"):
            flush_para()
            i += 1
            item_idx = 0
            while i < len(lines) and not lines[i].strip().startswith(r"\end{enumerate}"):
                item_line = lines[i].strip()
                if item_line.startswith(r"\item"):
                    item_idx += 1
                    text = item_line.replace(r"\item", "", 1)
                    blocks.append(ParagraphBlock("list", f"{item_idx}. {clean_latex(text, citation_map, label_map)}"))
                i += 1
            i += 1
            continue

        if line.startswith("\\") and not line.startswith(r"\url"):
            i += 1
            continue

        pending_para.append(line)
        i += 1

    flush_para()
    _, references = extract_bibliography(tex)
    return title, abstract, blocks, references


def qn(name: str) -> str:
    return f"w:{name}"


def paragraph_xml(text: str, style: str = "Normal", align: str | None = None, bold: bool = False, size: int = 21) -> str:
    jc = f'<w:jc w:val="{align}"/>' if align else ""
    style_xml = f'<w:pStyle w:val="{style}"/>' if style else ""
    bold_xml = "<w:b/>" if bold else ""
    return (
        "<w:p>"
        f"<w:pPr>{style_xml}{jc}</w:pPr>"
        "<w:r><w:rPr>"
        '<w:rFonts w:ascii="Times New Roman" w:eastAsia="SimSun" w:hAnsi="Times New Roman"/>'
        f"{bold_xml}<w:sz w:val=\"{size}\"/><w:szCs w:val=\"{size}\"/>"
        "</w:rPr>"
        f'<w:t xml:space="preserve">{escape(text)}</w:t>'
        "</w:r></w:p>"
    )


def image_xml(rel_id: str, name: str, width_px: int, height_px: int, max_width_in: float = 5.8) -> str:
    emu_per_in = 914400
    dpi = 96
    width_in = width_px / dpi
    height_in = height_px / dpi
    if width_in > max_width_in:
        scale = max_width_in / width_in
        width_in *= scale
        height_in *= scale
    cx = int(width_in * emu_per_in)
    cy = int(height_in * emu_per_in)
    doc_pr_id = abs(hash((rel_id, name))) % 100000 + 1000
    return f"""
<w:p>
  <w:pPr><w:jc w:val="center"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{doc_pr_id}" name="{escape(name)}"/>
        <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr>
                <pic:cNvPr id="{doc_pr_id + 1}" name="{escape(name)}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
"""


def table_xml(rows: list[list[str]]) -> str:
    if not rows:
        return paragraph_xml("表格内容未能从 LaTeX 源文件解析。", align=None)
    max_cols = max(len(row) for row in rows)
    width = max(1200, int(9000 / max_cols))
    grid = "".join(f'<w:gridCol w:w="{width}"/>' for _ in range(max_cols))
    row_xml_parts: list[str] = []
    for ridx, row in enumerate(rows):
        row = row + [""] * (max_cols - len(row))
        cells = []
        for cell in row:
            cells.append(
                "<w:tc>"
                f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/></w:tcPr>'
                + paragraph_xml(cell, style="", size=18)
                + "</w:tc>"
            )
        tr_pr = "<w:trPr><w:tblHeader/></w:trPr>" if ridx == 0 else ""
        row_xml_parts.append(f"<w:tr>{tr_pr}{''.join(cells)}</w:tr>")
    return (
        "<w:tbl>"
        "<w:tblPr><w:tblStyle w:val=\"TableGrid\"/><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders>"
        "<w:top w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"000000\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"8\" w:space=\"0\" w:color=\"000000\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"808080\"/>"
        "</w:tblBorders></w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>"
        + "".join(row_xml_parts)
        + "</w:tbl>"
    )


def section_break_xml(columns: int) -> str:
    cols = '<w:cols w:space="397"/>' if columns == 1 else '<w:cols w:num="2" w:space="397"/>'
    return (
        "<w:p><w:pPr>"
        "<w:sectPr>"
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="900" w:bottom="900" w:left="900" w:header="720" w:footer="720" w:gutter="0"/>'
        f"{cols}"
        '<w:docGrid w:type="lines" w:linePitch="290"/>'
        "</w:sectPr>"
        "</w:pPr></w:p>"
    )


def final_section_xml(columns: int) -> str:
    cols = '<w:cols w:space="397"/>' if columns == 1 else '<w:cols w:num="2" w:space="397"/>'
    return (
        "<w:sectPr>"
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1440" w:right="900" w:bottom="900" w:left="900" w:header="720" w:footer="720" w:gutter="0"/>'
        f"{cols}"
        '<w:docGrid w:type="lines" w:linePitch="290"/>'
        "</w:sectPr>"
    )


def build_document_xml(title: str, abstract: str, blocks: list[Block], references: list[tuple[int, str]], image_rels: dict[str, tuple[str, str]]) -> tuple[str, list[tuple[str, Path]]]:
    body: list[str] = []
    media: list[tuple[str, Path]] = []
    body.append(paragraph_xml(title, style="Title", align="center", bold=True, size=32))
    body.append(paragraph_xml("作者名1，作者名2+，作者名3（待导师确认）", align="center", size=21))
    body.append(paragraph_xml("1. 单位全名 部门全名，省 市 邮政编码（待确认）", align="center", size=18))
    body.append(paragraph_xml("+ 通信作者 E-mail：待确认", align="center", size=18))
    body.append(paragraph_xml("摘  要：" + abstract, size=19))
    body.append(paragraph_xml("关键词：无人机目标检测；小目标检测；YOLO11n；CoordAttention；VisDrone", size=19))
    body.append(paragraph_xml("文献标志码：A    中图分类号：TP391.4（待导师确认）", size=19))
    body.append(paragraph_xml(EN_TITLE, align="center", bold=True, size=28))
    body.append(paragraph_xml("NAME Namename1, NAME Name2+, NAME Namename3 (to be confirmed)", align="center", size=19))
    body.append(paragraph_xml("1. Department, University, City ZipCode, China (to be confirmed)", align="center", size=18))
    body.append(paragraph_xml("Abstract: " + EN_ABSTRACT, size=19))
    body.append(paragraph_xml("Key words: UAV object detection; small object detection; YOLO11n; CoordAttention; VisDrone", size=19))
    body.append(section_break_xml(columns=1))

    table_idx = 0
    fig_idx = 0
    rel_counter = 100
    missing_images: list[str] = []

    for block in blocks:
        if isinstance(block, ParagraphBlock):
            if block.kind == "heading1":
                body.append(paragraph_xml(block.text, style="Heading1", bold=True, size=24))
            elif block.kind == "heading2":
                body.append(paragraph_xml(block.text, style="Heading2", bold=True, size=22))
            elif block.kind == "list":
                body.append(paragraph_xml(block.text, size=20))
            else:
                body.append(paragraph_xml(block.text, size=20))
        elif isinstance(block, TableBlock):
            table_idx += 1
            en = EN_TABLE_CAPTIONS.get(block.caption, block.caption)
            body.append(paragraph_xml(f"表{table_idx} {block.caption}", align="center", bold=True, size=18))
            body.append(paragraph_xml(f"Table {table_idx} {en}", align="center", size=18))
            body.append(table_xml(block.rows))
        elif isinstance(block, FigureBlock):
            fig_idx += 1
            if block.image_path:
                image_path = ROOT / "paper" / block.image_path
                if image_path.exists():
                    rel_counter += 1
                    ext = image_path.suffix.lower().lstrip(".")
                    target_name = f"image{rel_counter}.{ext}"
                    rel_id = f"rIdCeaImage{rel_counter}"
                    with Image.open(image_path) as img:
                        width, height = img.size
                    body.append(image_xml(rel_id, image_path.name, width, height))
                    image_rels[rel_id] = (target_name, ext)
                    media.append((target_name, image_path))
                else:
                    missing_images.append(block.image_path)
                    body.append(paragraph_xml(f"[图像文件缺失：{block.image_path}]", align="center", size=18))
            elif block.fallback_text:
                for item in block.fallback_text:
                    body.append(paragraph_xml(item, align="center", size=18))
            en = EN_FIGURE_CAPTIONS.get(block.caption, block.caption)
            body.append(paragraph_xml(f"图{fig_idx} {block.caption}", align="center", bold=True, size=18))
            body.append(paragraph_xml(f"Fig.{fig_idx} {en}", align="center", size=18))

    body.append(paragraph_xml("参考文献:", style="Heading1", bold=True, size=24))
    for number, ref in references:
        body.append(paragraph_xml(f"[{number}] {ref}", size=18))

    body.append(paragraph_xml("联系人：待确认；通讯地址（邮政编码）：待确认；电子信箱、电话：待确认。", size=18))

    sect_pr = final_section_xml(columns=2)

    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
        'mc:Ignorable="w14 wp14">'
        '<w:body>'
        + "".join(body)
        + sect_pr
        + "</w:body></w:document>"
    )
    if missing_images:
        image_rels["__missing__"] = ("; ".join(missing_images), "")
    return document, media


def update_relationships(xml_bytes: bytes, image_rels: dict[str, tuple[str, str]]) -> bytes:
    ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    ET.register_namespace("", ns)
    root = ET.fromstring(xml_bytes)
    for rel_id, (target, ext) in image_rels.items():
        if rel_id.startswith("__"):
            continue
        ET.SubElement(
            root,
            f"{{{ns}}}Relationship",
            {
                "Id": rel_id,
                "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
                "Target": f"media/{target}",
            },
        )
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def update_content_types(xml_bytes: bytes) -> bytes:
    ns = "http://schemas.openxmlformats.org/package/2006/content-types"
    ET.register_namespace("", ns)
    root = ET.fromstring(xml_bytes)
    existing = {node.attrib.get("Extension") for node in root.findall(f"{{{ns}}}Default")}
    for ext, ctype in [("jpg", "image/jpeg"), ("jpeg", "image/jpeg"), ("png", "image/png")]:
        if ext not in existing:
            ET.SubElement(root, f"{{{ns}}}Default", {"Extension": ext, "ContentType": ctype})
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def build_docx() -> dict[str, int | str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tex = strip_comments(TEX_PATH.read_text(encoding="utf-8"))
    citation_map, references = extract_bibliography(tex)
    label_map = first_pass_label_map(tex)
    title, abstract, blocks, references = parse_blocks(tex, citation_map, label_map)

    image_rels: dict[str, tuple[str, str]] = {}
    document_xml, media = build_document_xml(title, abstract, blocks, references, image_rels)

    src = template_path()
    if OUTPUT_DOCX.exists():
        OUTPUT_DOCX.unlink()
    with zipfile.ZipFile(src, "r") as zin, zipfile.ZipFile(OUTPUT_DOCX, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = document_xml.encode("utf-8")
            elif item.filename == "word/_rels/document.xml.rels":
                data = update_relationships(data, image_rels)
            elif item.filename == "[Content_Types].xml":
                data = update_content_types(data)
            zout.writestr(item, data)
        for target_name, path in media:
            zout.write(path, f"word/media/{target_name}")

    return {
        "blocks": len(blocks),
        "tables": sum(isinstance(block, TableBlock) for block in blocks),
        "figures": sum(isinstance(block, FigureBlock) for block in blocks),
        "images": len(media),
        "references": len(references),
        "missing_images": image_rels.get("__missing__", ("", ""))[0],
    }


def write_report(stats: dict[str, int | str]) -> None:
    missing_images = str(stats.get("missing_images") or "")
    lines = [
        "# CEA Word Migration Audit",
        "",
        "This report is generated by `tools/build_cea_word_draft.py`. It records the first-pass migration from the current LaTeX manuscript candidate into the local CEA Word template. It does not change experiment values and does not mark the manuscript as formally submitted.",
        "",
        "## Summary",
        "",
        f"- Output docx: `{OUTPUT_DOCX.relative_to(ROOT).as_posix()}`",
        f"- Source LaTeX: `{TEX_PATH.relative_to(ROOT).as_posix()}`",
        f"- Template: `{template_path().relative_to(ROOT).as_posix()}`",
        f"- Parsed content blocks: {stats['blocks']}",
        f"- Migrated tables: {stats['tables']}",
        f"- Migrated figure environments: {stats['figures']}",
        f"- Embedded images: {stats['images']}",
        f"- References: {stats['references']}",
        f"- Missing images: {missing_images if missing_images else 'none'}",
        "- Layout: front matter is generated as a single-column section; the main text section is generated as two columns.",
        "",
        "## Manual Gates Remaining",
        "",
        "- Author names, affiliations, corresponding author, email, phone, postal address, funding, acknowledgements, and declarations still require user/advisor confirmation.",
        "- The generated Word file is a first-pass migration draft. It still needs manual page-by-page visual inspection in Microsoft Word/WPS.",
        "- The journal submission system file type and upload package requirements still need manual browser confirmation.",
        "- Official VisDrone test-dev metrics are still not included unless the official platform returns real values.",
        "",
        "## Content Boundary",
        "",
        "- Experimental metrics are copied from the current LaTeX candidate and existing paper tables; no new results are added.",
        "- English title and abstract are translation drafts derived from the Chinese title and abstract and should be reviewed by the advisor before formal submission.",
        "- The introduction is left unnumbered in the Word draft to match the CEA template note that the preface/introduction section should not be numbered.",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    stats = build_docx()
    write_report(stats)
    print(f"Wrote {OUTPUT_DOCX.relative_to(ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
