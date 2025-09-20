#!/usr/bin/env python3
"""
Generate CV from Dawid's exact markdown content
"""
import os
import sys
import asyncio
sys.path.append(os.path.dirname(__file__))

from manual_template_processor import process_template_manually
from resume_processor import ResumeProcessor
from html_pdf_generator import HTMLToPDFGenerator

async def generate_dawid_cv():
    """Generate CV from Dawid's exact markdown content"""
    
    # Dawid's exact resume content
    resume_content = """**DAWID MACIEJEWSKI**  
Digitalization & Automation Specialist  
Poland | Remote | +48 502 109 666 | dawid.mac@hotmail.com  
LinkedIn: <https://www.linkedin.com/in/dawid-maciejewski-32668289/> • GitHub: <https://github.com/davemac93>  

---

### PROFESSIONAL SUMMARY  
Digitalization leader with 3 + years of end‑to‑end experience in automating complex procurement and service‑delivery processes. Expert in UiPath, Power BI, Python, SAP/Ariba, and Power Apps, delivering measurable efficiency gains (40 % time‑reduction, 60 % backlog cut). Adept at cross‑regional stakeholder collaboration across North America, Asia, and EMEA, and a strong advocate for data‑driven decision‑making. Seeking a Digitalization/Automation role at PwC where I can leverage my consulting‑style mindset and technology expertise to scale global implementation projects.

---

### CORE TECHNICAL SKILLS  
- **Automation & RPA:** UiPath, Power Automate, ServiceNow, VBA, Python scripting  
- **Analytics & BI:** Power BI, SQL, Python (pandas, matplotlib)  
- **ERP & Procurement:** SAP, Ariba, SAP S/4HANA, SAP data extraction  
- **App Development:** Power Apps, SharePoint integration, Power Automate flows  
- **Miscellaneous:** Excel (advanced), ClickView, JavaScript, HTML/CSS, Node.js, C++  

**Process & Project Expertise** – process standardisation, SOP development, backlog management, cross‑functional collaboration, stakeholder communication.  

**Languages** – English (Fluent), Polish (Native), Danish (Fluent).  

---

### PROFESSIONAL EXPERIENCE  

**Digital Specialist – Indirect Procurement**  
*Danfoss, Poland* Mar 2025 – Present  
- Spearhead global digital‑transformation roadmap for the Indirect Procurement organisation, aligning strategy with tactical execution across 11 countries.  
- Lead the design & rollout of 150+ UiPath bots; automated routine cycles, reducing processing time by **40 %** and freeing 120 + person‑hours per month.  
- Build real‑time Power BI dashboards that provide executive‑level visibility into procurement KPIs; dashboards drive quarterly strategic reviews and cost‑saving discussions.  
- Champion continuous improvement, coaching teams on zero‑defect SOPs and change‑management practices.  

**Procurement Specialist – DPS (Direct Procurement Services)**  
*Danfoss, Poland* Apr 2024 – Mar 2025  
- Streamlined Poland DPS workflows, introducing Python‑based automation for email filtering, invoice parsing, and SAP PO closure—cutting invoice backlog by **60 %**.  
- Developed Power BI "Blocked‑Invoice" dashboards; enabled proactive risk mitigation for 3 regional teams.  
- Authored SOPs and workflow mappings adopted company‑wide to standardise SOP compliance.  
- Configured UiPath flows for material creation that reduced manual entry errors by 90 %.  

**Service & Solution Delivery Specialist**  
*Philips, Poland* Jul 2021 – Mar 2024  
- Delivered end‑to‑end service packages for Danish clients, managing quotes, parts, and post‑sales support.  
- Integrated Ariba procurement module; led testing and post‑go‑live support that ensured 100 % user adoption.  
- Piloted ServiceNow automation scripts that shortened ticket resolution time by **25 %**.  
- Produced ClickView & Excel dashboards for service statistics, informing capacity planning.  

---

### PROJECTS  

| Project | Tools | Impact |
|---------|-------|--------|
| **Procurement Analytics Control Tower** | Power BI, SQL, SAP | Unified real‑time analytics across all categories; supported supplier scorecard and cost‑saving analysis. |
| **PO & FO Automation (SAP)** | Python, SAP | Reduced PO/FO closure cycle by 70 %, eliminating manual errors. |
| **Power Apps Contact Management** | Power Apps, SharePoint, Power Automate | Centralised contact repository, cutting lookup times by 80 %. |
| **Procurement Process Standardisation** | SharePoint | Completed SOP library, decreasing onboarding time by 50 %. |
| **Real‑Estate Project Management Suite** | Power Apps, Power BI, Azure | Consolidated project data, improved variance tracking accuracy by 30 %. |

---

### EDUCATION  

**Bachelor of Computer Science** – *University of Łódź*  
Sep 2021 – Jun 2024  

---

### CERTIFICATIONS & TRAINING  

- **SAP Technology Consultant** – SAP (Enrolled)  
- **Google Data Analytics Professional Certificate** – Google (2024)  
- **Google AI Essentials** – Google (2024)  

---

### INTERESTS & ADDITIONAL SKILLS  

- AI tools & emerging technologies  
- Continuous self‑development & coaching  
- Multicultural teamwork & travel  
- Open‑source contributions & community mentoring  

---  

**Prepared for: PwC Global Implementation Projects – Digitalisation & Automation Specialist**  
*References available upon request.*"""

    print("🎯 Generating CV from Dawid's exact markdown content...")
    print(f"📄 Resume content length: {len(resume_content)} characters")
    
    # Process resume content
    processor = ResumeProcessor()
    structured_data = processor.process_resume_content(resume_content, {})
    
    print(f"✅ Processed data keys: {list(structured_data.keys())}")
    print(f"📊 Experience entries: {len(structured_data.get('experience', []))}")
    print(f"🏷️  Tags: {len(structured_data.get('tags', []))}")
    print(f"🎓 Education entries: {len(structured_data.get('education', []))}")
    print(f"📜 Certifications: {len(structured_data.get('certifications', []))}")
    print(f"🚀 Projects: {len(structured_data.get('projects', []))}")
    
    # Show extracted data
    print(f"\n👤 Name: {structured_data.get('name', 'N/A')}")
    print(f"💼 Title: {structured_data.get('title', 'N/A')}")
    print(f"📧 Email: {structured_data.get('email', 'N/A')}")
    print(f"📱 Phone: {structured_data.get('phone', 'N/A')}")
    print(f"🌍 Location: {structured_data.get('location', 'N/A')}")
    print(f"🔗 LinkedIn: {structured_data.get('linkedin', 'N/A')}")
    print(f"💻 GitHub: {structured_data.get('github', 'N/A')}")
    
    # Show experience details
    print(f"\n📋 Experience Details:")
    for i, exp in enumerate(structured_data.get('experience', [])[:3]):
        print(f"  {i+1}. {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}")
        print(f"     Dates: {exp.get('startDate', 'N/A')} – {exp.get('endDate', 'N/A')}")
        print(f"     Bullets: {len(exp.get('bullets', []))}")
    
    # Show projects details
    print(f"\n🚀 Projects Details:")
    for i, project in enumerate(structured_data.get('projects', [])[:3]):
        print(f"  {i+1}. {project.get('name', 'N/A')}")
        print(f"     Tools: {project.get('stack', 'N/A')}")
        print(f"     Description: {len(project.get('desc', []))} items")
    
    # Show skills
    print(f"\n🏷️  Skills (first 10):")
    for i, skill in enumerate(structured_data.get('tags', [])[:10]):
        print(f"  {i+1}. {skill}")
    
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
    
    # Generate PDF using Playwright
    print("\n📄 Generating PDF with Playwright...")
    pdf_generator = HTMLToPDFGenerator()
    
    try:
        pdf_bytes = await pdf_generator.generate_pdf_from_html(html_content, "dawid_maciejewski")
        
        if pdf_bytes:
            print(f"✅ PDF generated successfully: {len(pdf_bytes)} bytes")
            
            # Save the PDF
            output_path = "DAWID_MACIEJEWSKI_CV.pdf"
            with open(output_path, "wb") as f:
                f.write(pdf_bytes)
            print(f"💾 CV PDF saved as: {output_path}")
            
            # Also save the HTML for inspection
            html_path = "DAWID_MACIEJEWSKI_CV.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"💾 HTML version saved as: {html_path}")
            
            print(f"\n🎉 Success! Generated CV from Dawid's markdown")
            print(f"📁 Files created:")
            print(f"   - {output_path} (PDF)")
            print(f"   - {html_path} (HTML)")
            
            return True
        else:
            print("❌ PDF generation failed - no bytes returned")
            return False
            
    except Exception as e:
        print(f"❌ PDF generation error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await pdf_generator.close()

if __name__ == "__main__":
    success = asyncio.run(generate_dawid_cv())
    if success:
        print("\n🎉 CV generation completed successfully!")
        print("📖 You can now open DAWID_MACIEJEWSKI_CV.pdf to see the result!")
    else:
        print("\n❌ CV generation failed!")
        sys.exit(1)
