# CV Generator System

A comprehensive system for generating professional CVs from markdown content using Python, Playwright, and FastAPI.

## Features

✅ **Flexible Markdown Support** - Works with different markdown formats  
✅ **Professional PDF Generation** - High-quality PDFs using Playwright  
✅ **Complete Section Support** - All CV sections including optional ones  
✅ **RESTful API** - Easy integration with web applications  
✅ **Template Engine** - Customizable HTML templates  
✅ **Data Extraction** - Intelligent parsing of markdown content  

## Supported Sections

### Required Sections (Always Present)
- **Name & Contact Details** - Name, title, email, phone, location, LinkedIn, GitHub
- **Professional Summary** - Career overview and key achievements
- **Professional Experience** - Work history with detailed descriptions
- **Education** - Academic qualifications and degrees
- **Languages** - Language proficiency levels

### Optional Sections (Included When Present)
- **Core Skills** - Technical and soft skills organized by category
- **Projects** - Portfolio projects with tools and impact
- **Certifications** - Professional certifications and training
- **Interests** - Personal interests and hobbies
- **Achievements** - Awards and recognitions
- **Additional Skills** - Other relevant skills

## Markdown Format

The system supports a flexible markdown format. Here's the recommended structure:

```markdown
**Your Name**  
Your Title | Key Skills | Technologies  
Location / Remote  
+1 234 567 8900 | your.email@example.com | [LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)  

---  

### Professional Summary  
Your professional summary here...

---  

### Key Competencies  

| Technical | Process & Project | Soft & Leadership |
|-----------|------------------|--------------------|
| Skill1, Skill2, Skill3 | Process1, Process2 | Leadership1, Leadership2 |

---  

### Professional Experience  

**Job Title**  
**Company Name** | Start Date – End Date  
- Achievement 1 with metrics
- Achievement 2 with impact
- Achievement 3 with results

---  

### Selected Projects  

| Project | Tools | Impact |
|---------|-------|--------|
| Project Name | Tool1, Tool2 | Impact description |

---  

### Education  

**Degree Name** – University Name | Start Date – End Date  

---  

### Certifications & Training  

- Certification 1 – Issuer (Year)
- Certification 2 – Issuer (Year)

---  

### Languages  

- Language 1 – Proficiency Level
- Language 2 – Proficiency Level

---  

### Interests (optional)  

Your interests and hobbies here...
```

## Usage

### 1. Command Line Usage

#### Generate CV from specific markdown:
```bash
python generate_dawid_cv.py
```

#### Generate CV from any markdown:
```bash
python generate_cv_generic.py
```

#### Test with new markdown format:
```bash
python test_new_markdown_cv.py
```

### 2. API Usage

#### Start the API server:
```bash
python cv_api.py
```

#### Generate CV via API:
```bash
curl -X POST "http://localhost:8000/generate-cv" \
  -H "Content-Type: application/json" \
  -d '{
    "markdown_content": "**Your Name**\nYour Title...",
    "filename": "my_cv.pdf"
  }'
```

### 3. Python Integration

```python
import asyncio
from generate_cv_generic import generate_cv_from_markdown

async def create_cv():
    markdown_content = """
    **John Doe**  
    Software Engineer | Python | React  
    San Francisco, CA  
    +1 555 123 4567 | john@email.com  
    
    ### Professional Summary  
    Experienced software engineer...
    """
    
    success = await generate_cv_from_markdown(
        markdown_content, 
        "john_cv.pdf", 
        "john_doe"
    )
    
    if success:
        print("CV generated successfully!")

asyncio.run(create_cv())
```

## File Structure

```
backend/
├── cv_api.py                    # FastAPI REST API
├── generate_cv_generic.py       # Generic CV generator
├── generate_dawid_cv.py         # Specific CV generator
├── test_new_markdown_cv.py      # Test script
├── manual_template_processor.py # Template processing engine
├── resume_processor.py          # Markdown parsing engine
├── html_pdf_generator.py        # PDF generation with Playwright
├── resume_template.html         # HTML template
└── requirements.txt             # Dependencies
```

## Dependencies

- **FastAPI** - Web framework for API
- **Playwright** - PDF generation
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Template Customization

Edit `resume_template.html` to customize the CV appearance:
- CSS styles for colors, fonts, layout
- HTML structure for sections
- Responsive design elements

### Data Extraction

Modify `resume_processor.py` to:
- Add new section parsers
- Customize extraction patterns
- Handle different markdown formats

### PDF Generation

Adjust `html_pdf_generator.py` for:
- Page size and margins
- Print quality settings
- Browser options

## API Endpoints

### POST /generate-cv
Generate a CV from markdown content.

**Request Body:**
```json
{
  "markdown_content": "**Name**\nTitle...",
  "user_id": "optional_user_id",
  "filename": "optional_filename.pdf"
}
```

**Response:**
```json
{
  "success": true,
  "message": "CV generated successfully",
  "pdf_filename": "cv_12345.pdf",
  "html_filename": "cv_12345.html",
  "file_size": 112712
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "CV Generator API is running"
}
```

## Error Handling

The system includes comprehensive error handling:
- **Template Processing Errors** - Invalid template syntax
- **PDF Generation Errors** - Playwright or browser issues
- **Data Extraction Errors** - Malformed markdown content
- **File System Errors** - Permission or disk space issues

## Performance

- **PDF Generation**: ~2-3 seconds per CV
- **Memory Usage**: ~50-100MB per generation
- **Concurrent Requests**: Supports multiple simultaneous generations
- **File Size**: Typical CVs are 80-120KB

## Troubleshooting

### Common Issues

1. **Template syntax errors**
   - Check for unclosed `{{}}` blocks
   - Verify template file exists

2. **PDF generation fails**
   - Ensure Playwright is installed: `playwright install`
   - Check browser dependencies

3. **Data extraction issues**
   - Verify markdown format matches expected patterns
   - Check for special characters in content

4. **File permission errors**
   - Ensure write permissions in output directory
   - Check disk space availability

### Debug Mode

Enable debug output by setting environment variable:
```bash
export DEBUG=1
python generate_cv_generic.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Create an issue in the repository
4. Contact the development team

---

**Note**: This system is designed to be flexible and work with different markdown formats. The parser automatically detects and handles various section formats, making it suitable for different CV styles and requirements.
