# Flexible CV Generation System

## Overview

This system provides a complete solution for generating professional CVs from markdown content. It's designed to be flexible and work with different markdown formats while maintaining consistent, high-quality output.

## Key Features

✅ **Flexible Parser** - Handles various markdown formats
✅ **Optional Sections** - Only includes sections that have content
✅ **Professional Design** - Uses the proven design from `generate_dawid_cv.py`
✅ **AI Agent Ready** - Includes prompt template for consistent markdown generation
✅ **PDF Generation** - High-quality PDF output using Playwright

## System Components

### 1. AI Agent Prompt Template (`ai_agent_prompt_template.md`)
- **Purpose**: Ensures consistent markdown format from AI agents
- **Features**: 
  - Required sections (name, contact, summary, experience, education, languages)
  - Optional sections (certifications, projects, skills, interests)
  - Clear formatting guidelines
  - Example output

### 2. Flexible Resume Processor (`flexible_resume_processor.py`)
- **Purpose**: Parses markdown content into structured data
- **Features**:
  - Handles multiple markdown formats
  - Extracts personal information, experience, education, etc.
  - Processes optional sections only if they have content
  - Cleans up markdown formatting

### 3. Manual Template Processor (`manual_template_processor.py`)
- **Purpose**: Renders HTML templates with structured data
- **Features**:
  - Handles complex nested loops
  - Processes conditional sections
  - Cleans up template syntax

### 4. HTML to PDF Generator (`html_pdf_generator.py`)
- **Purpose**: Converts HTML to PDF using Playwright
- **Features**:
  - High-quality PDF output
  - Professional formatting
  - Consistent styling

## Usage

### Basic Usage

```python
from generate_cv_flexible import generate_cv_from_markdown
import asyncio

async def main():
    markdown_content = """**John Doe**
Software Engineer | Python | React | AWS
San Francisco, CA
+1 555 123 4567 | john.doe@email.com | [LinkedIn](https://linkedin.com/in/johndoe) | [GitHub](https://github.com/johndoe)

---

### Professional Summary
Experienced Software Engineer with 5+ years developing scalable web applications...

---

### Professional Experience
**Senior Software Engineer**
**Tech Corp, San Francisco, CA** | Jan 2022 – Present
- Led development of microservices architecture...
- Implemented CI/CD pipelines...

---

### Education
**Bachelor of Science in Computer Science** – University of California, Berkeley | Sep 2016 – May 2020

---

### Languages
- **English** – Native
- **Spanish** – Conversational"""

    success = await generate_cv_from_markdown(markdown_content, "john_doe_cv.pdf")
    if success:
        print("CV generated successfully!")

asyncio.run(main())
```

### Command Line Usage

```bash
# Test the flexible system
python generate_cv_flexible.py

# Test with specific markdown
python test_flexible_cv.py
```

## Required Sections

These sections are **always included** in the generated CV:

1. **Name** - Full name
2. **Contact Details** - Email, phone, location, LinkedIn, GitHub
3. **Professional Summary** - 2-3 sentences describing experience and value
4. **Professional Experience** - Job history with achievements
5. **Education** - Degree and institution
6. **Languages** - Language proficiency

## Optional Sections

These sections are **only included if they have content**:

1. **Certifications & Training** - Professional certifications
2. **Selected Projects** - Key projects with tools and impact
3. **Core Technical Skills** - Skills organized by category
4. **Interests** - Personal interests and hobbies
5. **Additional Information** - Any other relevant information

## Markdown Format Requirements

### Personal Information
```markdown
**FULL NAME**
Job Title | Key Skills (3-4 skills) | Location
City, Country | Phone | Email | [LinkedIn](URL) | [GitHub](URL)
```

### Experience
```markdown
**Job Title**
**Company Name, Location** | Start Date – End Date
- Achievement 1 with quantified results
- Achievement 2 with quantified results
- Achievement 3 with quantified results
```

### Skills (Table Format)
```markdown
| Technical | Process & Project | Soft & Leadership |
|-----------|------------------|--------------------|
| skill1, skill2, skill3 | skill1, skill2, skill3 | skill1, skill2, skill3 |
```

### Projects (Table Format)
```markdown
| Project | Tools | Impact |
|---------|-------|--------|
| **Project Name** | Tools used | Brief impact description |
```

## AI Agent Integration

To use with an AI agent, provide the prompt template from `ai_agent_prompt_template.md`:

1. **Copy the prompt template**
2. **Customize for your specific needs**
3. **Send to AI agent with candidate information**
4. **Use generated markdown with this system**

## File Structure

```
backend/
├── ai_agent_prompt_template.md      # AI agent prompt template
├── flexible_resume_processor.py     # Flexible markdown parser
├── manual_template_processor.py     # HTML template renderer
├── html_pdf_generator.py           # PDF generator
├── resume_template.html            # HTML template
├── generate_cv_flexible.py         # Main CV generator
├── test_flexible_cv.py            # Test script
└── FLEXIBLE_CV_SYSTEM_README.md   # This file
```

## Testing

### Test the System
```bash
python generate_cv_flexible.py
```

### Test with Different Formats
```bash
python test_flexible_cv.py
```

## Output Files

For each CV generation, the system creates:

1. **`filename.pdf`** - The generated CV in PDF format
2. **`filename.html`** - HTML version for inspection

## Error Handling

The system includes comprehensive error handling:

- **Template syntax validation** - Ensures all placeholders are processed
- **Section validation** - Checks for required sections
- **PDF generation validation** - Verifies successful PDF creation
- **Debug output** - Shows extracted data for troubleshooting

## Customization

### Adding New Sections

1. **Update `flexible_resume_processor.py`** - Add parsing logic
2. **Update `manual_template_processor.py`** - Add rendering logic
3. **Update `resume_template.html`** - Add HTML structure
4. **Update `ai_agent_prompt_template.md`** - Add to prompt template

### Modifying Design

1. **Edit `resume_template.html`** - Change HTML structure and CSS
2. **Update `manual_template_processor.py`** - Modify rendering logic
3. **Test with `generate_cv_flexible.py`** - Verify changes

## Best Practices

1. **Use the AI agent prompt template** for consistent markdown generation
2. **Test with different markdown formats** to ensure flexibility
3. **Validate output** by checking both PDF and HTML files
4. **Keep sections optional** - only include if they have meaningful content
5. **Use quantified achievements** in experience descriptions
6. **Maintain consistent formatting** across all sections

## Troubleshooting

### Common Issues

1. **Template syntax not processed** - Check `manual_template_processor.py`
2. **Missing sections** - Verify markdown format matches expected structure
3. **PDF generation fails** - Check Playwright installation and browser setup
4. **Poor formatting** - Review HTML template and CSS styles

### Debug Mode

Enable debug output by setting environment variable:
```bash
export DEBUG_CV_GENERATION=1
python generate_cv_flexible.py
```

## Performance

- **Processing time**: ~2-3 seconds per CV
- **PDF size**: Typically 100-150KB
- **Memory usage**: ~50MB during generation
- **Concurrent generation**: Supports multiple simultaneous generations

## License

This system is part of the CV Builder project and follows the same licensing terms.

## Support

For issues or questions:
1. Check the debug output
2. Review the generated HTML file
3. Verify markdown format matches the template
4. Check the troubleshooting section above
