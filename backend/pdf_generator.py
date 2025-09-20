from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io
import logging

class ResumePDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.darkblue,
            borderPadding=5
        ))
        
        # Contact info style
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=20
        ))

    def generate_pdf(self, resume_content: str, user_id: str) -> bytes:
        """Generate PDF from resume content"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        # Parse resume content and create story
        story = []
        
        # Split content into sections
        sections = self._parse_resume_content(resume_content)
        
        # Add title
        if 'name' in sections:
            story.append(Paragraph(sections['name'], self.styles['CustomTitle']))
        
        # Add contact info
        if 'contact' in sections:
            story.append(Paragraph(sections['contact'], self.styles['ContactInfo']))
        
        # Add other sections
        for section_name, content in sections.items():
            if section_name not in ['name', 'contact'] and content.strip():
                story.append(Paragraph(section_name.replace('_', ' ').title(), self.styles['SectionHeader']))
                story.append(Paragraph(content, self.styles['Normal']))
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def _parse_resume_content(self, content: str) -> dict:
        """Parse resume content into sections"""
        sections = {}
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header (all caps, or followed by colons)
            if line.isupper() and len(line) > 3 and len(line) < 50:
                # Save previous section
                if current_section and current_content:
                    sections[current_section.lower()] = '<br/>'.join(current_content)
                
                # Start new section
                current_section = line
                current_content = []
            elif line.endswith(':') and len(line) < 50:
                # Save previous section
                if current_section and current_content:
                    sections[current_section.lower()] = '<br/>'.join(current_content)
                
                # Start new section
                current_section = line[:-1]  # Remove colon
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
                else:
                    # This might be the name or contact info
                    if not sections.get('name'):
                        sections['name'] = line
                    elif not sections.get('contact'):
                        sections['contact'] = line
        
        # Save last section
        if current_section and current_content:
            sections[current_section.lower()] = '<br/>'.join(current_content)
        
        return sections
