# Playwright PDF Generation Setup

This document explains the Playwright-based PDF generation system implemented for better HTML-to-PDF conversion.

## 🎭 Overview

Playwright provides superior PDF rendering compared to ReportLab by:
- **Better HTML/CSS Support**: Full modern web standards support
- **Professional Layouts**: Accurate rendering of complex layouts and styling
- **Font Rendering**: High-quality font rendering and text layout
- **Responsive Design**: Proper handling of responsive layouts
- **Print Optimization**: Built-in print media query support

## 📁 Files Structure

```
backend/
├── html_pdf_generator.py      # Playwright PDF generation class
├── resume_processor.py        # Resume content processing
├── template_engine.py         # HTML template rendering
├── resume_template.html       # Professional resume HTML template
├── install_playwright.py      # Browser installation script
├── test_playwright_pdf.py     # Test script for PDF generation
└── PLAYWRIGHT_SETUP.md        # This documentation
```

## 🚀 Installation

### 1. Install Playwright Package
```bash
pip install playwright==1.40.0
```

### 2. Install Browser
```bash
python -m playwright install chromium
```

### 3. Install System Dependencies (Linux only)
```bash
python -m playwright install-deps
```

## 🔧 Usage

### Basic PDF Generation
```python
from html_pdf_generator import html_pdf_generator

# Initialize Playwright
await html_pdf_generator.initialize()

# Generate PDF from HTML
html_content = "<html>...</html>"
pdf_bytes = await html_pdf_generator.generate_pdf_from_html(html_content, "user_id")

# Cleanup
await html_pdf_generator.close()
```

### Resume Processing
```python
from resume_processor import ResumeProcessor
from template_engine import template_engine

# Process resume content
processor = ResumeProcessor()
structured_data = processor.process_resume_content(resume_content, profile_data)

# Render HTML template
html_content = template_engine.render_template_file("resume_template.html", structured_data)
```

## 🌐 API Endpoints

### New Endpoints Added

1. **`POST /generate-html-pdf/`**
   - Generates PDF using Playwright HTML rendering
   - Returns PDF as streaming response
   - Better quality than ReportLab

2. **`POST /generate-and-store-html-pdf/`**
   - Generates PDF using Playwright
   - Stores PDF in Supabase Storage
   - Updates database with storage URL

### Legacy Endpoints (Still Available)

- `POST /generate-pdf/` - ReportLab-based PDF generation
- `POST /generate-and-store-pdf/` - ReportLab + Storage

## 🎨 Resume Template

The `resume_template.html` provides a professional resume layout with:

- **Modern Design**: Clean, professional styling
- **Responsive Layout**: Adapts to different content lengths
- **Print Optimization**: Optimized for PDF generation
- **Template Variables**: Dynamic content insertion
- **Section Support**: Experience, Education, Skills, Projects, etc.

### Template Variables

```javascript
{
  "name": "John Doe",
  "title": "Software Engineer",
  "email": "john@example.com",
  "phone": "(555) 123-4567",
  "location": "San Francisco, CA",
  "linkedin": "linkedin.com/in/johndoe",
  "summary": "Professional summary...",
  "experience": [
    {
      "title": "Senior Developer",
      "company": "Tech Corp",
      "startDate": "2020",
      "endDate": "2023",
      "description": "Job description..."
    }
  ],
  "education": [...],
  "skills": [...],
  "projects": [...],
  "certifications": [...],
  "achievements": [...]
}
```

## 🧪 Testing

### Run Tests
```bash
python test_playwright_pdf.py
```

### Test Coverage
- ✅ Playwright browser initialization
- ✅ HTML-to-PDF conversion
- ✅ Resume content processing
- ✅ Template rendering
- ✅ PDF file generation

## ⚙️ Configuration

### PDF Options
```python
pdf_options = {
    'format': 'A4',
    'print_background': True,
    'margin': {
        'top': '0.5in',
        'right': '0.5in',
        'bottom': '0.5in',
        'left': '0.5in'
    },
    'prefer_css_page_size': True,
    'display_header_footer': False
}
```

### Browser Options
```python
browser_args = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-accelerated-2d-canvas',
    '--no-first-run',
    '--no-zygote',
    '--disable-gpu'
]
```

## 🔄 Migration from ReportLab

### Frontend Changes
The frontend automatically uses the new Playwright endpoints:
- `generate-pdf/` → `generate-html-pdf/`
- `generate-and-store-pdf/` → `generate-and-store-html-pdf/`

### Backward Compatibility
- Legacy ReportLab endpoints remain available
- Gradual migration possible
- No breaking changes

## 🚨 Troubleshooting

### Common Issues

1. **Browser Not Found**
   ```bash
   python -m playwright install chromium
   ```

2. **Permission Errors (Linux)**
   ```bash
   python -m playwright install-deps
   ```

3. **Memory Issues**
   - Reduce browser args
   - Close browser after each use
   - Use headless mode

4. **Template Not Found**
   - Ensure `resume_template.html` exists
   - Check file permissions
   - Verify template path

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance

### Comparison with ReportLab

| Feature | ReportLab | Playwright |
|---------|-----------|------------|
| HTML Support | Limited | Full |
| CSS Support | Basic | Complete |
| Font Rendering | Good | Excellent |
| Layout Accuracy | Fair | Excellent |
| Performance | Fast | Moderate |
| File Size | Small | Medium |

### Optimization Tips

1. **Reuse Browser Instance**: Initialize once, use multiple times
2. **Close Unused Pages**: Clean up after each PDF generation
3. **Optimize HTML**: Minimize external resources
4. **Use Headless Mode**: Faster rendering
5. **Cache Templates**: Avoid re-parsing templates

## 🔮 Future Enhancements

- [ ] Custom CSS themes
- [ ] Multiple resume templates
- [ ] Batch PDF generation
- [ ] PDF optimization
- [ ] Watermark support
- [ ] Digital signature integration

## 📝 Notes

- Playwright requires more system resources than ReportLab
- Better suited for production environments
- Excellent for complex layouts and modern web standards
- Consider caching for high-volume usage
