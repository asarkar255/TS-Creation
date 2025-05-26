from docx import Document

def create_docx(ts_text: str, buffer):
    doc = Document()
    doc.add_heading('Technical Specification', level=1)
    for line in ts_text.splitlines():
        doc.add_paragraph(line)
    doc.save(buffer)

