#!/usr/bin/env python3
"""
Generic CV Generator - Works with different markdown formats and profiles
Supports both the new format and legacy formats
"""
import os
import sys
import asyncio
sys.path.append(os.path.dirname(__file__))

from manual_template_processor import process_template_manually
from resume_processor import ResumeProcessor
from html_pdf_generator import HTMLToPDFGenerator

async def generate_cv_from_markdown(markdown_content: str, output_filename: str = "generated_cv.pdf", user_id: str = "user"):
    """
    Generate CV from any markdown content
    
    Args:
        markdown_content: The resume content in markdown format
        output_filename: Name of the output PDF file
        user_id: User identifier for the PDF generator
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    print(f"🎯 Generating CV from markdown content...")
    print(f"📄 Resume content length: {len(markdown_content)} characters")
    
    # Process resume content
    processor = ResumeProcessor()
    structured_data = processor.process_resume_content(markdown_content, {})
    
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
    
    # Generate PDF using Playwright
    print("\n📄 Generating PDF with Playwright...")
    pdf_generator = HTMLToPDFGenerator()
    
    try:
        pdf_bytes = await pdf_generator.generate_pdf_from_html(html_content, user_id)
        
        if pdf_bytes:
            print(f"✅ PDF generated successfully: {len(pdf_bytes)} bytes")
            
            # Save the PDF
            with open(output_filename, "wb") as f:
                f.write(pdf_bytes)
            print(f"💾 CV PDF saved as: {output_filename}")
            
            # Also save the HTML for inspection
            html_filename = output_filename.replace('.pdf', '.html')
            with open(html_filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"💾 HTML version saved as: {html_filename}")
            
            print(f"\n🎉 Success! Generated CV from markdown")
            print(f"📁 Files created:")
            print(f"   - {output_filename} (PDF)")
            print(f"   - {html_filename} (HTML)")
            
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

async def main():
    """Main function to demonstrate CV generation"""
    
    # Example 1: New format (like the one we just fixed)
    new_format_content = """**John Doe**  
Software Engineer | Python | React | AWS  
San Francisco, CA  
+1 555 123 4567 | john.doe@email.com | [LinkedIn](https://linkedin.com/in/johndoe) | [GitHub](https://github.com/johndoe)  

---  

### Professional Summary  
Experienced software engineer with 5+ years of experience in full-stack development, cloud architecture, and team leadership. Passionate about building scalable applications and mentoring junior developers.

---  

### Key Competencies  

| Technical | Process & Project | Soft & Leadership |
|-----------|------------------|--------------------|
| Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes | Agile development, CI/CD, code review, testing | Team leadership, mentoring, stakeholder communication |

---  

### Professional Experience  

**Senior Software Engineer**  
**Tech Corp** | Jan 2022 – Present  
- Led development of microservices architecture serving 1M+ users
- Mentored 3 junior developers and improved team productivity by 30%
- Implemented CI/CD pipelines reducing deployment time by 50%

**Software Engineer**  
**StartupXYZ** | Jun 2020 – Dec 2021  
- Built full-stack web applications using React and Python
- Collaborated with product team to define technical requirements
- Optimized database queries improving response time by 40%

---  

### Education  

**Bachelor of Computer Science** – University of California | 2016 – 2020  

---  

### Languages  

- English – Native  
- Spanish – Conversational  

---  

### Interests  

Open source contributions, hiking, photography, cooking."""

    # Generate CV with new format
    success = await generate_cv_from_markdown(
        new_format_content, 
        "john_doe_cv.pdf", 
        "john_doe"
    )
    
    if success:
        print("\n🎉 CV generation completed successfully!")
        print("📖 You can now open john_doe_cv.pdf to see the result!")
    else:
        print("\n❌ CV generation failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
