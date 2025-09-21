#!/usr/bin/env python3
"""
Test CV generation with the new markdown content
"""
import os
import sys
import asyncio
sys.path.append(os.path.dirname(__file__))

from manual_template_processor import process_template_manually
from resume_processor import ResumeProcessor
from html_pdf_generator import HTMLToPDFGenerator

async def test_new_markdown_cv():
    """Test CV generation with the new markdown content"""
    
    # New markdown content
    markdown_content = """**Dawid Maciejewski**  
Digitalization & Automation Specialist | RPA | Power BI | Python  
Poland / Denmark / Remote  
+48 502 109 666 | dawid.mac@hotmail.com | [LinkedIn](https://www.linkedin.com/in/dawid-maciejewski-32668289/) | [GitHub](https://github.com/davemac93)  

---  

### Professional Summary  
Dynamic digital‑transformation leader with 3+ years of end‑to‑end experience in procurement, SaaS, and engineering sectors. Proven record of designing and deploying enterprise‑scale RPA, analytics, and process‑automation solutions that cut manual effort by up to 60 % and accelerate key KPIs. Adept at translating business requirements into data‑driven technology roadmaps, collaborating with stakeholders across Americas, Asia, and Europe, and delivering measurable impact for global firms such as Danfoss and Philips.

---  

### Key Competencies  

| Technical | Process & Project | Soft & Leadership |
|-----------|------------------|--------------------|
| UiPath, Power Automate, Power Apps, Power BI, Python, VBA, SQL, SAP, Ariba, ServiceNow, Excel, SharePoint | Process standardization, SOP development, backlog management, testing & implementation | Cross‑functional stakeholder management, change‑management, project leadership, agile facilitation |

---  

### Professional Experience  

**Digital Specialist – Digitalization & Automation**  
**Danfoss, Global** | Mar 2025 – Present  
- Spearheaded global RPA program, delivering 150 + bots that reduced manual tasks by **40 %** and cut processing time for procurement workflows.  
- Designed and launched a real‑time Power BI dashboard that feeds executive stakeholders with live KPIs, improving decision speed by **25 %**.  
- Partnered with SAP/Ariba teams to integrate data pipelines, ensuring accurate, real‑time reporting across 12 regions.  

**Procurement Specialist – Digital Procurement**  
**Danfoss, Poland** | Apr 2024 – Mar 2025  
- Automated vendor‑onboarding and invoice reconciliation using Python scripts, shrinking backlog by **60 %** and increasing compliance across 3 regional teams.  
- Developed SOPs and facilitated workshops that unified processes, boosting adoption rate to > 90 % among cross‑regional stakeholders.  
- Implemented UiPath automation for material creation, cutting cycle time from 3 days to 4 hours.  

**Service & Solution Delivery Specialist**  
**Philips, Denmark** | Jul 2021 – Mar 2024  
- Delivered global procurement services, managing quotes and parts for over 2000 customer requests per quarter.  
- Automated ticket‑resolution workflow in ServiceNow, reducing average resolution time by **25 %**; led go‑live of Ariba procurement module in 2023.  
- Created data‑driven insights in ClickView and Excel, enabling proactive quality monitoring.  

---  

### Selected Projects  

| Project | Tools | Impact |
|---------|-------|--------|
| **Procurement Analytics Control Tower** | Power BI, SQL, SAP | Centralized real‑time dashboard for supplier performance; enabled predictive insights that saved > €300k annually. |
| **PO & FO Automation for SAP** | Python, SAP | Automated PO/FO closure, cutting closure cycle from 5 days to 30 minutes; improved data accuracy by 98 %. |
| **Power Apps Contact Management Tool** | Power Apps, SharePoint, Power Automate | Unified cross‑regional contact database; reduced lookup time by 70 %. |
| **Process Documentation & Standardization** | SharePoint | Created a single source of truth for procurement processes, slashing documentation time by 80 %. |
| **Power Apps & Power BI Real Estate PM** | Power Apps, Power BI, Azure | Integrated data collection & approval workflows; improved project visibility and budget adherence by 15 %. |

---  

### Education  

**Bachelor's Degree in Computer Science** – University of Lodz | 2021 Sep – 2024 Jun  

---  

### Certifications & Training  

- **Google Data Analytics Professional Certificate** – 2024  
- **Google AI Essentials** – 2024  
- **SAP Technology Consultant** – *Enrolled*  

---  

### Languages  

- English – Fluent  
- Polish – Native  
- Danish – Fluent  

---  

### Interests (optional)  

AI tools, emerging technologies, global travel, continuous learning, family & friends.  

---  

*Prepared for PwC Digitalisation Specialist – Automation & Analytics role.*"""

    print("🎯 Testing CV generation with new markdown content...")
    print(f"📄 Resume content length: {len(markdown_content)} characters")
    
    # Process the resume
    processor = ResumeProcessor()
    structured_data = processor.process_resume_content(markdown_content, {})
    
    print(f"✅ Processed data keys: {list(structured_data.keys())}")
    print(f"📊 Experience entries: {len(structured_data.get('experience', []))}")
    print(f"🏷️  Tags: {len(structured_data.get('tags', []))}")
    print(f"🎓 Education entries: {len(structured_data.get('education', []))}")
    print(f"📜 Certifications: {len(structured_data.get('certifications', []))}")
    print(f"🚀 Projects: {len(structured_data.get('projects', []))}")
    
    # Show personal info
    print(f"\n👤 Name: {structured_data.get('name', 'N/A')}")
    print(f"💼 Title: {structured_data.get('title', 'N/A')}")
    print(f"📧 Email: {structured_data.get('email', 'N/A')}")
    print(f"📱 Phone: {structured_data.get('phone', 'N/A')}")
    print(f"🌍 Location: {structured_data.get('location', 'N/A')}")
    print(f"🔗 LinkedIn: {structured_data.get('linkedin', 'N/A')}")
    print(f"💻 GitHub: {structured_data.get('github', 'N/A')}")
    
    # Show experience details
    print(f"\n📋 Experience Details:")
    for i, exp in enumerate(structured_data.get('experience', [])):
        print(f"  {i+1}. {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
        print(f"     Dates: {exp.get('startDate', 'N/A')} – {exp.get('endDate', 'N/A')}")
        print(f"     Bullets: {len(exp.get('bullets', []))}")
    
    # Show projects details
    print(f"\n🚀 Projects Details:")
    for i, project in enumerate(structured_data.get('projects', [])):
        print(f"  {i+1}. {project.get('name', 'N/A')}")
        print(f"     Tools: {project.get('stack', 'N/A')}")
        print(f"     Description: {len(project.get('desc', []))} items")
    
    # Show skills
    print(f"\n🏷️  Skills (first 10):")
    for i, skill in enumerate(structured_data.get('tags', [])[:10]):
        print(f"  {i+1}. {skill}")
    
    print(f"\n🎯 Core Skills:")
    core_skills = structured_data.get('core_skills', {})
    for category, skills in core_skills.items():
        print(f"  {category}: {skills}")
    
    print(f"\n🌍 Languages:")
    for i, lang in enumerate(structured_data.get('languages', [])):
        print(f"  {i+1}. {lang}")
    
    print(f"\n🎨 Interests:")
    for i, interest in enumerate(structured_data.get('interests', [])):
        print(f"  {i+1}. {interest}")
    
    # Test template rendering
    template_path = os.path.join(os.path.dirname(__file__), "resume_template.html")
    
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return False
    
    print("\n🎨 Rendering template...")
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    html_content = process_template_manually(template_content, structured_data)
    
    # Check if template syntax is still present
    if "{{" in html_content and "}}" in html_content:
        print("❌ Template syntax still present in rendered HTML!")
        lines = html_content.split('\n')
        for i, line in enumerate(lines):
            if "{{" in line and "}}" in line:
                print(f"  Line {i+1}: {line.strip()}")
        return False
    else:
        print("✅ Template syntax successfully processed!")
    
    # Generate PDF
    print("\n📄 Generating PDF with Playwright...")
    pdf_generator = HTMLToPDFGenerator()
    
    try:
        pdf_bytes = await pdf_generator.generate_pdf_from_html(html_content, "test_user")
        print(f"✅ PDF generated successfully: {len(pdf_bytes)} bytes")
        
        # Save files
        output_pdf = "DAWID_NEW_MARKDOWN_CV.pdf"
        output_html = "DAWID_NEW_MARKDOWN_CV.html"
        
        with open(output_pdf, 'wb') as f:
            f.write(pdf_bytes)
        
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 CV PDF saved as: {output_pdf}")
        print(f"💾 HTML version saved as: {output_html}")
        
        print(f"\n🎉 Success! Generated CV from new markdown")
        print(f"📁 Files created:")
        print(f"   - {output_pdf} (PDF)")
        print(f"   - {output_html} (HTML)")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_new_markdown_cv())
