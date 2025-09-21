#!/usr/bin/env python3
"""
Test the complete AI flexible CV workflow: JSON profile → AI agent → markdown → flexible parser → PDF
"""
import asyncio
import json
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from lib.agent import run_agent
from flexible_resume_processor import FlexibleResumeProcessor
from manual_template_processor import process_template_manually
from html_pdf_generator import HTMLToPDFGenerator

async def test_ai_flexible_workflow():
    """Test the complete AI flexible CV workflow"""
    
    print("🎯 Testing complete AI flexible CV workflow...")
    
    # Sample JSON profile
    profile_data = {
        "personal_info": {
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1 555 123 4567",
            "location": "San Francisco, CA",
            "linkedin": "https://linkedin.com/in/johndoe",
            "github": "https://github.com/johndoe"
        },
        "title": "Senior Software Engineer",
        "summary": "Experienced Software Engineer with 5+ years developing scalable web applications and cloud solutions. Expert in Python, React, and AWS with proven track record of delivering high-impact projects.",
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "start_date": "Jan 2022",
                "end_date": "Present",
                "achievements": [
                    "Led development of microservices architecture using Python and AWS Lambda, improving system scalability by 40%",
                    "Implemented CI/CD pipelines with Jenkins and Docker, reducing deployment time by 50%",
                    "Mentored 3 junior engineers, improving team productivity by 25%"
                ]
            },
            {
                "title": "Software Engineer",
                "company": "StartupXYZ",
                "location": "San Francisco, CA",
                "start_date": "Jun 2020",
                "end_date": "Dec 2021",
                "achievements": [
                    "Developed RESTful APIs using Node.js and Express, handling over 10,000 requests per minute",
                    "Collaborated with product designers to implement new features in React, resulting in 20% increase in user engagement",
                    "Optimized database queries in PostgreSQL, reducing response times by 30%"
                ]
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "institution": "University of California, Berkeley",
                "start_date": "Sep 2016",
                "end_date": "May 2020"
            }
        ],
        "skills": {
            "technical": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes"],
            "process": ["Agile development", "CI/CD", "code review", "testing"],
            "soft": ["Team leadership", "mentoring", "stakeholder communication"]
        },
        "languages": [
            {"name": "English", "level": "Native"},
            {"name": "Spanish", "level": "Conversational"}
        ],
        "certifications": [
            {"name": "AWS Certified Solutions Architect", "provider": "Amazon", "year": "2023"},
            {"name": "Google Data Analytics Professional Certificate", "provider": "Google", "year": "2022"}
        ],
        "projects": [
            {
                "name": "E-commerce Platform",
                "tools": "React, Node.js, MongoDB",
                "impact": "Increased sales by 35% through improved user experience"
            },
            {
                "name": "Data Analytics Dashboard",
                "tools": "Python, Power BI, SQL",
                "impact": "Enabled data-driven decisions, saving $500K annually"
            }
        ],
        "interests": ["Open source contributions", "Machine learning", "Photography", "Hiking"]
    }
    
    job_offer_url = "https://example.com/senior-software-engineer-job"
    
    print(f"📄 Profile data keys: {list(profile_data.keys())}")
    
    # Step 1: AI Agent generates markdown from JSON profile
    print("\n🤖 Step 1: AI Agent generating markdown from JSON profile...")
    try:
        markdown_content = await run_agent(profile_data, job_offer_url)
        
        if not markdown_content:
            print("❌ AI agent failed to generate markdown")
            return False
        
        print(f"✅ AI agent generated markdown: {len(markdown_content)} characters")
        print(f"📝 Markdown preview:\n{markdown_content[:500]}...")
        
        # Save markdown for inspection
        with open("ai_generated_markdown.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print("💾 Markdown saved to ai_generated_markdown.md")
        
    except Exception as e:
        print(f"❌ AI agent error: {e}")
        return False
    
    # Step 2: Flexible parser processes markdown
    print("\n🔧 Step 2: Flexible parser processing markdown...")
    try:
        processor = FlexibleResumeProcessor()
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
        
    except Exception as e:
        print(f"❌ Flexible parser error: {e}")
        return False
    
    # Step 3: Generate PDF using template
    print("\n🎨 Step 3: Rendering template...")
    try:
        template_path = "resume_template.html"
        if not os.path.exists(template_path):
            print(f"❌ Template file not found: {template_path}")
            return False
        
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
        
        # Save HTML for inspection
        with open("ai_flexible_cv.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("💾 HTML saved to ai_flexible_cv.html")
        
    except Exception as e:
        print(f"❌ Template rendering error: {e}")
        return False
    
    # Step 4: Generate PDF using Playwright
    print("\n📄 Step 4: Generating PDF with Playwright...")
    try:
        pdf_generator = HTMLToPDFGenerator()
        await pdf_generator.initialize()
        
        pdf_bytes = await pdf_generator.generate_pdf_from_html(html_content, "test_user")
        
        if not pdf_bytes:
            print("❌ PDF generation failed")
            return False
        
        print(f"✅ PDF generated successfully: {len(pdf_bytes)} bytes")
        
        # Save PDF
        with open("AI_FLEXIBLE_CV_TEST.pdf", "wb") as f:
            f.write(pdf_bytes)
        print("💾 PDF saved to AI_FLEXIBLE_CV_TEST.pdf")
        
        await pdf_generator.close()
        
    except Exception as e:
        print(f"❌ PDF generation error: {e}")
        return False
    
    print("\n🎉 Complete AI flexible CV workflow test successful!")
    print("📁 Files created:")
    print("   - ai_generated_markdown.md (AI agent output)")
    print("   - ai_flexible_cv.html (rendered HTML)")
    print("   - AI_FLEXIBLE_CV_TEST.pdf (final PDF)")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_ai_flexible_workflow())
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
