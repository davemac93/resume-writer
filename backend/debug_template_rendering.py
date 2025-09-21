#!/usr/bin/env python3
"""
Debug script to test template rendering with AI-generated markdown
"""
import json
from resume_processor import ResumeProcessor
from template_engine import TemplateEngine

def test_template_rendering():
    print("🔍 Testing template rendering with AI-generated markdown...")
    
    # Sample AI-generated markdown (from the logs)
    markdown_content = """**DAWID MACIEJEWSKI**  
Digitalization Specialist | RPA, Power BI, Python, Automation | Poland
Warsaw, Poland | +48 502 109 666 | dawid.mac@hotmail.com | [LinkedIn](https://www.linkedin.com/in/dawid-maciejewski-32668289/) | [GitHub](https://github.com/davemac93)
---
### Professional Summary
Digitalization and Automation Specialist with a Computer Science background and a proven record of designing and deploying end‑to‑end RPA and analytics solutions. In recent roles, I have automated over 150 manual tasks, reduced invoice backlogs by 60%, and delivered real‑time Power BI dashboards that drove executive decision‑making. I thrive on collaborating with global stakeholders to translate business needs into scalable technology solutions.
---
### Key Competencies
| Technical | Process & Project | Soft & Leadership |
|-----------|------------------|--------------------|
| UiPath, Python, Power BI, Power Automate, VBA, SAP, Ariba, ServiceNow | Process standardization, SOP development, backlog management, system testing, stakeholder collaboration | Cross‑functional collaboration, communication, problem solving, initiative |    
---
### Professional Experience
**Digital Specialist**
**Danfoss, Poland** | *March 2025 – Present*
- Designed and deployed global UiPath bots that automated **150+ manual tasks**, cutting processing time by **40%**.
- Launched a real‑time Power BI dashboard providing executive insights into procurement KPIs, enhancing data visibility across regions.
- Led cross‑regional teams to integrate cutting‑edge automation technologies into daily operations, improving workforce productivity.
**Procurement Specialist**
**Danfoss, Poland** | *April 2024 – March 2025*
- Implemented Python scripts and UiPath bots to reduce invoice processing backlog by **60%**.
- Standardized SOPs adopted by three regional teams, boosting process compliance by **25%**.
- Automated SAP data extraction and PO closure workflows, decreasing manual effort by **35%**.
**Service and Solution Delivery Specialist**
**Philips, Denmark** | *July 2021 – March 2024*
- Piloted ServiceNow automation scripts that trimmed ticket resolution time by **25%**.
- Key contributor to the successful go‑live of the Ariba procurement module in 2023, ensuring a smooth transition for European customers.
---
### Education
**Bachelor's Degree in Computer Science** – University of Łódź | *Sep 2021 – Jun 2024*
---
### Languages
- **English** – Fluent
- **Polish** – Native
- **Danish** – Fluent
---
### Certifications & Training
- **Google Data Analytics Professional Certificate** – Google (2024)
- **Google AI Essentials** – Google (2024)
- **SAP Technology Consultant** – SAP (Currently Enrolled)       
---
### Selected Projects
| Project | Tools | Impact |
|---------|-------|--------|
| **Procurement Analytics Control Tower** | Power BI, SQL, SAP | Centralized procurement view; real‑time monitoring of supplier performance and spending, enabling proactive risk mitigation and cost savings. |
| **PO and FO Automation for SAP System** | Python, SAP | Streamlined PO/FO closure workflow, cutting manual effort by 40% and improving data accuracy across planning processes. |
| **Power Apps Contact Management Tool** | Power Apps, SharePoint, Power Automate | Created a centralized contact repository; improved cross‑regional communication and reduced lookup time by 30%. |
---
### Core Technical Skills
- **Automation & RPA:** UiPath, Power Automate, VBA, Python, JavaScript
- **Analytics & BI:** Power BI, SQL, Power Apps, Excel, Tableau (experts)
---
### Interests
- AI Tools
- Self‑development
- Emerging Technologies
---
### Additional Information
Remote or hybrid work preferences; experienced in global collaboration across Americas, Asia, and Europe.
---"""

    print(f"📄 Markdown content length: {len(markdown_content)} characters")
    
    # Step 1: Process with flexible parser
    print("\n🔧 Step 1: Processing with ResumeProcessor...")
    processor = ResumeProcessor()
    structured_data = processor.process_resume_content(markdown_content, {})
    
    print(f"✅ Processed data keys: {list(structured_data.keys())}")
    print(f"📊 Experience entries: {len(structured_data.get('experience', []))}")
    print(f"🏷️  Tags: {len(structured_data.get('tags', []))}")
    print(f"🎓 Education entries: {len(structured_data.get('education', []))}")
    print(f"📜 Certifications: {len(structured_data.get('certifications', []))}")
    print(f"🚀 Projects: {len(structured_data.get('projects', []))}")
    
    # Print experience details
    print(f"\n📋 Experience details:")
    for i, exp in enumerate(structured_data.get('experience', [])):
        print(f"  {i+1}. Title: {exp.get('title', 'N/A')}")
        print(f"     Company: {exp.get('company', 'N/A')}")
        print(f"     Dates: {exp.get('startDate', 'N/A')} - {exp.get('endDate', 'N/A')}")
        print(f"     Bullets: {len(exp.get('bullets', []))}")
        print()
    
    # Print education details
    print(f"\n🎓 Education details:")
    for i, edu in enumerate(structured_data.get('education', [])):
        print(f"  {i+1}. Degree: {edu.get('degree', 'N/A')}")
        print(f"     Institution: {edu.get('institution', 'N/A')}")
        print(f"     Dates: {edu.get('startDate', 'N/A')} - {edu.get('endDate', 'N/A')}")
        print()
    
    # Print projects details
    print(f"\n🚀 Projects details:")
    for i, proj in enumerate(structured_data.get('projects', [])):
        print(f"  {i+1}. Name: {proj.get('name', 'N/A')}")
        print(f"     Tools: {proj.get('tools', 'N/A')}")
        print(f"     Impact: {proj.get('impact', 'N/A')}")
        print()
    
    # Step 2: Test template rendering
    print("\n🎨 Step 2: Testing template rendering...")
    
    # Read the template
    with open('resume_template.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Render template
    template_engine = TemplateEngine()
    html_content = template_engine.render_template(template_content, structured_data)
    
    print(f"✅ HTML generated: {len(html_content)} characters")
    
    # Check for remaining template syntax
    remaining_syntax = []
    lines = html_content.split('\n')
    for i, line in enumerate(lines):
        if '{{' in line and '}}' in line:
            remaining_syntax.append(f"Line {i+1}: {line.strip()}")
    
    if remaining_syntax:
        print(f"❌ Template syntax still present in {len(remaining_syntax)} lines:")
        for syntax in remaining_syntax[:10]:  # Show first 10
            print(f"  {syntax}")
    else:
        print("✅ Template syntax successfully processed!")
    
    # Save debug files
    with open('debug_structured_data.json', 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
    print("💾 Structured data saved to debug_structured_data.json")
    
    with open('debug_rendered_html.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("💾 Rendered HTML saved to debug_rendered_html.html")

if __name__ == "__main__":
    test_template_rendering()
