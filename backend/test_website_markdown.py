#!/usr/bin/env python3
"""
Test CV generation with website-generated markdown content
"""
import os
import sys
import asyncio
sys.path.append(os.path.dirname(__file__))

from manual_template_processor import process_template_manually
from resume_processor import ResumeProcessor
from html_pdf_generator import HTMLToPDFGenerator

async def test_website_markdown_cv():
    """Test CV generation with website-generated markdown content"""
    
    # Website-generated markdown content
    markdown_content = """**DAWID MACIEJEWSKI**  
Digitalization & Automation Specialist  
Poland • Remote / Hybrid  
📞 +48 502 109 666 | 📧 dawid.mac@hotmail.com  
🔗 LinkedIn: https://www.linkedin.com/in/dawid-maciejewski-32668289/ | 👨‍💻 GitHub: https://github.com/davemac93  

---

### PROFESSIONAL SUMMARY  
Strategic and hands‑on Digitalization & Automation Specialist with 5 + years of experience driving process transformation in global procurement, ERP, and service‑delivery environments. Proven track record in RPA (UiPath), data‑driven analytics (Power BI), and Python automation that reduce manual effort by up to 60 % and accelerate decision‑making. Adept at collaborating with cross‑functional teams across the Americas, Asia, and Europe, and eager to contribute to PwC's consulting portfolio through technology‑enabled business solutions.

---

### CORE COMPETENCES  

| **Technical** | **Process / Project** | **Tools & Platforms** |
|---------------|-----------------------|-----------------------|
| RPA (UiPath, Power Automate) | Process standardization & optimization | Power BI, Power Apps, SQL |
| Python, VBA, JavaScript | SOP development & backlog reduction | SAP, Ariba, ServiceNow |
| Excel, VBA | Stakeholder management & testing | Node.js, HTML/CSS |
| Data analysis | Change management | SharePoint, ClickView, Microsoft Teams |

| **Skills** | **Level** |
|------------|-----------|
| Robotic Process Automation (RPA) | Advanced |
| Business Process Improvement | Advanced |
| Data Analysis | Advanced |
| SAP | Advanced |
| Power BI | Advanced |
| Python | Advanced |

---

### PROFESSIONAL EXPERIENCE  

**Danfoss** – *Digital Specialist*  
*Mar 2025 – Present*  
- Lead end‑to‑end digital transformation for the Indirect Procurement organization across 5 continents.  
- Designed and deployed a global UiPath bot suite that automated 150+ repetitive tasks, reducing process time by **40 %**.  
- Launched a real‑time Power BI dashboard that drives executive insights into procurement KPIs and identifies cost‑saving opportunities.  

**Danfoss** – *Procurement Specialist*  
*Apr 2024 – Mar 2025*  
- Streamlined procurement workflows for the newly established DPS department in Poland, cutting invoice backlog by **60 %** through integrated Python scripting and UiPath automation.  
- Developed Power BI dashboards visualizing blocked invoice statistics, enabling proactive resolution of bottlenecks.  
- Authored SOPs adopted by three regional teams, improving compliance and process clarity.  

**Philips** – *Service and Solution Delivery Specialist*  
*Jul 2021 – Mar 2024*  
- Managed service delivery for Danish clients, coordinating quotes, parts, and investigative ticketing in ServiceNow.  
- Piloted automation scripts that reduced ticket resolution time by **25 %**, improving customer satisfaction.  
- Contributed to the successful Ariba module go‑live in 2023, participating in end‑to‑end testing and knowledge transfer.  

---

### EDUCATION  

**University of Łódź** – *Bachelor's Degree, Computer Science*  
*Sep 2021 – Jun 2024*  

---

### CERTIFICATIONS & TRAINING  

| Credential | Provider | Year |
|------------|----------|------|
| SAP Technology Consultant (In‑progress) | SAP | • |
| Google Data Analytics Professional Certificate | Google | 2024 |
| Google AI Essentials | Google | 2024 |

---

### RELEVANT PROJECTS  

- **Procurement Analytics Control Tower** – Powered by Power BI & SAP, delivering a single source of truth for procurement metrics, real‑time alerts, and predictive insights.  
- **PO & FO Automation for SAP** – Automated PO and forecast order processing in SAP, reducing manual effort and enhancing data accuracy.  
- **Power Apps Contact Management Tool** – Centralized contact repository for procurement specialists across regions, improving collaboration and data integrity.  
- **Procurement Process Documentation & Standardization** – Created a SharePoint‑based documentation hub that clarified workflows and reduced backlog for a multi‑country transition.  

---

### LANGUAGES  

- **English** – Fluent  
- **Polish** – Native  
- **Danish** – Fluent  

---

### INTERESTS  

AI‑Powered solutions, emerging technologies, continuous self‑development, cultural exploration, travel, and family time.  

--- 

**Note:** All dates are in the format *MMM YYYY – MMM YYYY* or *MMM YYYY – Present*. All company names are bolded and positions italicized per professional standards. The resume is tailored for a Digitalization/Automation Specialist role at PwC, emphasizing automation, data analytics, procurement expertise, and cross‑functional collaboration."""

    print("🎯 Testing CV generation with website-generated markdown content...")
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
        output_pdf = "DAWID_WEBSITE_CV.pdf"
        output_html = "DAWID_WEBSITE_CV.html"
        
        with open(output_pdf, 'wb') as f:
            f.write(pdf_bytes)
        
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 CV PDF saved as: {output_pdf}")
        print(f"💾 HTML version saved as: {output_html}")
        
        print(f"\n🎉 Success! Generated CV from website markdown")
        print(f"📁 Files created:")
        print(f"   - {output_pdf} (PDF)")
        print(f"   - {output_html} (HTML)")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_website_markdown_cv())
