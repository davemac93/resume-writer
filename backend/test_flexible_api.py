#!/usr/bin/env python3
"""
Test the flexible CV API endpoint
"""
import requests
import json

def test_flexible_cv_api():
    """Test the flexible CV API endpoint"""
    
    # Test markdown content
    markdown_content = """**John Doe**
Software Engineer | Python | React | AWS
San Francisco, CA
+1 555 123 4567 | john.doe@email.com | [LinkedIn](https://linkedin.com/in/johndoe) | [GitHub](https://github.com/johndoe)

---

### Professional Summary
Experienced Software Engineer with 5+ years developing scalable web applications and cloud solutions. Expert in Python, React, and AWS with proven track record of delivering high-impact projects.

---

### Key Competencies

| Technical | Process & Project | Soft & Leadership |
|-----------|------------------|--------------------|
| Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes | Agile development, CI/CD, code review, testing | Team leadership, mentoring, stakeholder communication |

---

### Professional Experience

**Senior Software Engineer**
**Tech Corp, San Francisco, CA** | Jan 2022 – Present
- Led development of microservices architecture using Python and AWS Lambda, improving system scalability by 40%
- Implemented CI/CD pipelines with Jenkins and Docker, reducing deployment time by 50%
- Mentored 3 junior engineers, improving team productivity by 25%

**Software Engineer**
**StartupXYZ, San Francisco, CA** | Jun 2020 – Dec 2021
- Developed RESTful APIs using Node.js and Express, handling over 10,000 requests per minute
- Collaborated with product designers to implement new features in React, resulting in 20% increase in user engagement
- Optimized database queries in PostgreSQL, reducing response times by 30%

---

### Education

**Bachelor of Science in Computer Science** – University of California, Berkeley | Sep 2016 – May 2020

---

### Languages

- **English** – Native
- **Spanish** – Conversational"""

    # Test the health endpoint first
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

    # Test the flexible CV endpoint (without authentication for now)
    print("\n🎯 Testing flexible CV endpoint...")
    try:
        # Note: This will fail without authentication, but we can test the endpoint structure
        response = requests.post(
            "http://localhost:8000/generate-flexible-cv/",
            data={"markdown_content": markdown_content},
            timeout=30
        )
        print(f"📊 Response status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Endpoint exists (authentication required as expected)")
        else:
            print(f"📄 Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Flexible CV endpoint test failed: {e}")
        return False

    print("\n🎉 API endpoint tests completed!")
    return True

if __name__ == "__main__":
    test_flexible_cv_api()
