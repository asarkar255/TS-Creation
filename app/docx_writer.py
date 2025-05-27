from docx import Document
from docx.shared import Pt, RGBColor
import re

def add_heading(doc, text):
    paragraph = doc.add_paragraph()
    run = paragraph.add_run(text)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 0, 255)  # Blue
    run.underline = True
    run.font.size = Pt(14)
    paragraph.style = 'Normal'

def add_content(doc, text):
    doc.add_paragraph(text)

def extract_flowchart_text(ts_text: str) -> str:
    flowchart_section = re.search(r"12\. Flowchart\s*(.*?)\n(?=\d{1,2}\.|\Z)", ts_text, re.DOTALL)
    if flowchart_section:
        return flowchart_section.group(1).strip()
    return ""

def create_docx(ts_text: str, buffer):

    # section_header_pattern = re.compile(r"^\s*\d{1,2}\.\s*.+")
    doc = Document()
    doc.add_heading('Technical Specification', level=1)

    current_section = ""
    current_content = []

    lines = ts_text.splitlines()
    for line in lines:
        # if section_header_pattern.match(line):
            if current_section and current_content:
                add_heading(doc, current_section)
                add_content(doc, '\n'.join(current_content))
            current_section = line.strip()
            current_content = []
        # else:
            current_content.append(line)

    # Add last section
    if current_section and current_content:
        add_heading(doc, current_section)
        add_content(doc, '\n'.join(current_content))

    # Append Flowchart as raw text
    flowchart_text = extract_flowchart_text(ts_text)
    if flowchart_text:
        doc.add_page_break()
        add_heading(doc, "Flowchart (Visual)")
        add_content(doc, flowchart_text)

    doc.save(buffer)
