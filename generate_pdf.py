
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf():
    doc = SimpleDocTemplate("PROJECT_DOCUMENTATION.pdf", pagesize=A4, margin=(20, 20, 20, 20))
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleCustom',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=1, # Center
        spaceAfter=20,
        textColor=colors.darkblue
    )
    
    h1_style = ParagraphStyle(
        'Header1Custom',
        parent=styles['Heading1'],
        fontSize=18,
        spaceBefore=15,
        spaceAfter=10,
        textColor=colors.darkblue,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Header2Custom',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=10,
        spaceAfter=5,
        textColor=colors.black,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeCustom',
        parent=styles['Code'],
        fontSize=9,
        leading=11,
        fontName='Courier',
        backColor=colors.lightgrey,
        borderPadding=5
    )

    story = []
    
    # Add Title Page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("KONKAN GUIDE", title_style))
    story.append(Paragraph("PROJECT DOCUMENTATION", title_style))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("A Beginner's Guide to the Codebase", styles['Heading3']))
    story.append(PageBreak())

    with open("PROJECT_DOCUMENTATION.txt", "r") as f:
        lines = f.readlines()

    buffer_text = []
    
    def flush_buffer():
        if buffer_text:
            text = " ".join(buffer_text).strip()
            if text:
                story.append(Paragraph(text, body_style))
            buffer_text.clear()

    current_section = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip separator lines
        if line.startswith("===") or line.startswith("---"):
            i += 1
            continue
            
        # Check for Sections (SECTION X: ...)
        if line.startswith("SECTION "):
            flush_buffer()
            # If previous line was separator, this is definitely a header
            story.append(PageBreak())
            story.append(Paragraph(line, h1_style))
            i += 1
            continue
            
        # Check for Subheadings (ALL CAPS, usually short)
        # We need to be careful not to trigger on short sentences.
        # Heuristic: line is all upper, length > 3, not starting with - or *
        is_subheading = (line.isupper() and len(line) > 3 and not line.startswith("-") 
                         and " " in line and len(line.split()) < 10)
        
        # Or checking if next line is "---" or "===" in original text?
        # My txt file puts "---" UNDER subheadings usually? No, I put it under Section headers.
        # But I used "WHAT THIS PROJECT DOES" followed by "----------------------"
        if i + 1 < len(lines) and lines[i+1].strip().startswith("---"):
             flush_buffer()
             story.append(Paragraph(line, h2_style))
             i += 2 # Skip current line and dashed line
             continue

        if not line:
            flush_buffer()
            # Double newline might mean spacer
            # story.append(Spacer(1, 5)) 
            i += 1
            continue
            
        # Code lists or bullet points
        if line.startswith("- ") or line.startswith("* ") or line.startswith("1. "):
             flush_buffer()
             # Render list item
             story.append(Paragraph(line, body_style))
             i += 1
             continue
             
        # Normal text
        buffer_text.append(line)
        i += 1
        
    flush_buffer()
    
    doc.build(story)
    print("PDF Generated Successfully")

if __name__ == "__main__":
    generate_pdf()
