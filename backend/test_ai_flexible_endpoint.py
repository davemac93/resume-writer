#!/usr/bin/env python3
"""
Test the AI flexible CV endpoint with proper FormData
"""
import requests
import json
import os

def test_ai_flexible_endpoint():
    """Test the AI flexible CV endpoint with proper FormData"""
    
    # Create a sample JSON profile file
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
        "summary": "Experienced Software Engineer with 5+ years developing scalable web applications.",
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "start_date": "Jan 2022",
                "end_date": "Present",
                "achievements": [
                    "Led development of microservices architecture using Python and AWS Lambda, improving system scalability by 40%",
                    "Implemented CI/CD pipelines with Jenkins and Docker, reducing deployment time by 50%"
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
            "technical": ["Python", "JavaScript", "React", "Node.js", "AWS"],
            "process": ["Agile development", "CI/CD", "code review"],
            "soft": ["Team leadership", "mentoring", "communication"]
        },
        "languages": [
            {"name": "English", "level": "Native"},
            {"name": "Spanish", "level": "Conversational"}
        ]
    }
    
    # Save profile to temporary file
    with open("test_profile.json", "w") as f:
        json.dump(profile_data, f, indent=2)
    
    print("🔍 Testing AI flexible CV endpoint...")
    
    # Test without authentication first to see the exact error
    try:
        with open("test_profile.json", "rb") as f:
            files = {"profile_json": ("test_profile.json", f, "application/json")}
            data = {"job_offer_url": "https://example.com/job"}
            
            response = requests.post(
                "http://localhost:8000/generate-ai-flexible-cv/",
                files=files,
                data=data,
                timeout=30
            )
            
        print(f"📊 Response status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 422:
            print("❌ 422 Unprocessable Entity - likely authentication required")
        elif response.status_code == 401:
            print("✅ 401 Unauthorized - authentication required as expected")
        else:
            print(f"✅ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Clean up
    if os.path.exists("test_profile.json"):
        os.remove("test_profile.json")

if __name__ == "__main__":
    test_ai_flexible_endpoint()
