"""
Resume data processor for converting AI-generated content to structured data
"""
import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class ResumeProcessor:
    def __init__(self):
        self.template_vars = {}
    
    def process_resume_content(self, resume_content: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process AI-generated resume content and profile data into structured format
        
        Args:
            resume_content: Raw resume content from AI
            profile_data: User profile data from database
            
        Returns:
            Structured data for HTML template
        """
        from datetime import date
        
        # Extract personal information
        personal_info = self._extract_personal_info(resume_content, profile_data)
        
        # Extract professional summary
        summary = self._extract_summary(resume_content)
        
        # Extract work experience
        experience = self._extract_experience(resume_content, profile_data)
        
        # Extract education
        education = self._extract_education(resume_content, profile_data)
        
        # Extract skills as tags
        tags = self._extract_skills_as_tags(resume_content, profile_data)
        
        # Extract projects
        projects = self._extract_projects(resume_content, profile_data)
        
        # Extract certifications
        certifications = self._extract_certifications(resume_content, profile_data)
        
        # Extract achievements
        achievements = self._extract_achievements(resume_content, profile_data)
        
        return {
            'name': personal_info.get('name', ''),
            'title': personal_info.get('title', ''),
            'email': personal_info.get('email', ''),
            'phone': personal_info.get('phone', ''),
            'location': personal_info.get('location', ''),
            'linkedin': personal_info.get('linkedin', ''),
            'github': personal_info.get('github', ''),
            'summary': summary,
            'experience': experience,
            'education': education,
            'tags': tags,
            'projects': projects,
            'certifications': certifications,
            'achievements': achievements,
            'core_skills': self._extract_core_skills(resume_content, profile_data),
            'languages': self._extract_languages(resume_content),
            'interests': self._extract_interests(resume_content),
            'strengths': [],
            'additional': [],
            'fit': [],
            'currentYear': date.today().year
        }
    
    def _extract_personal_info(self, resume_content: str, profile_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract personal information from resume content and profile data"""
        personal = profile_data.get('personal', {})
        
        # Try to extract from resume content first, fallback to profile data
        # Handle markdown headers for name - look for **Name** format
        name = self._extract_field(resume_content, r'\*\*([^*]+)\*\*', personal.get('name', ''))
        if not name:
            # Try markdown header format
            name = self._extract_field(resume_content, r'^#\s*(.+?)$', personal.get('name', ''))
        if not name:
            # Try to extract from the first non-empty line if it's not a header
            lines = [line.strip() for line in resume_content.split('\n') if line.strip()]
            if lines and not lines[0].startswith('#'):
                name = lines[0]
            else:
                name = self._extract_field(resume_content, r'Name:\s*(.+?)(?:\n|$)', personal.get('name', ''))
        
        # For title, extract from the second line (after name)
        title = personal.get('title', '')
        if not title:
            lines = [line.strip() for line in resume_content.split('\n') if line.strip()]
            if len(lines) >= 2:
                second_line = lines[1]
                # Skip if it contains contact info (has @ or linkedin.com or github.com)
                if '@' not in second_line and 'linkedin.com' not in second_line.lower() and 'github.com' not in second_line.lower() and not second_line.startswith('#'):
                    title = second_line
        
        # Extract location from the third line (if it doesn't contain contact info)
        location = ""
        lines = [line.strip() for line in resume_content.split('\n') if line.strip()]
        if len(lines) >= 3:
            third_line = lines[2]
            # If third line doesn't contain contact info, it's likely location
            if '@' not in third_line and '+' not in third_line and 'linkedin.com' not in third_line.lower() and 'github.com' not in third_line.lower():
                location = third_line
        
        # Extract contact info - look for the line with phone/email/LinkedIn/GitHub
        contact_line = ""
        for line in lines:
            if ('@' in line and ('+' in line or 'linkedin.com' in line.lower() or 'github.com' in line.lower())):
                contact_line = line
                break
        
        # Also check for emoji-prefixed contact info
        if not contact_line:
            for line in lines:
                if ('📞' in line or '📧' in line) and ('@' in line or '+' in line):
                    contact_line = line
                    break
        
        # Parse pipe-separated contact info
        email = ""
        phone = ""
        linkedin = ""
        github = ""
        
        if contact_line and '|' in contact_line:
            # Split by pipe and extract each field
            parts = [part.strip() for part in contact_line.split('|')]
            for part in parts:
                # Clean up emoji prefixes
                clean_part = re.sub(r'^[📞📧🔗👨‍💻]\s*', '', part.strip())
                
                if '@' in clean_part:
                    email = clean_part
                elif 'linkedin.com' in clean_part.lower():
                    # Extract URL from markdown link format [LinkedIn](url) or <url>
                    linkedin_match = re.search(r'\[LinkedIn\]\(([^)]+)\)|<([^>]+)>', clean_part)
                    if linkedin_match:
                        linkedin = linkedin_match.group(1) or linkedin_match.group(2)
                    else:
                        linkedin = clean_part
                elif 'github.com' in clean_part.lower():
                    # Extract URL from markdown link format [GitHub](url) or <url>
                    github_match = re.search(r'\[GitHub\]\(([^)]+)\)|<([^>]+)>', clean_part)
                    if github_match:
                        github = github_match.group(1) or github_match.group(2)
                    else:
                        github = clean_part
                elif '+' in clean_part or (any(char.isdigit() for char in clean_part) and 'linkedin.com' not in clean_part.lower() and 'github.com' not in clean_part.lower()):
                    phone = clean_part
                elif not email and not phone and not linkedin and not github:
                    # This might be location
                    location = clean_part
        
        # Also check the fourth line for LinkedIn and GitHub
        if len(lines) >= 4:
            fourth_line = lines[3]
            if 'LinkedIn:' in fourth_line and 'GitHub:' in fourth_line:
                # Extract LinkedIn URL
                linkedin_match = re.search(r'LinkedIn:\s*<([^>]+)>', fourth_line)
                if linkedin_match:
                    linkedin = linkedin_match.group(1)
                
                # Extract GitHub URL
                github_match = re.search(r'GitHub:\s*<([^>]+)>', fourth_line)
                if github_match:
                    github = github_match.group(1)
        
        # Fallback to individual field extraction if pipe format didn't work
        if not email:
            email = self._extract_field(resume_content, r'Email:\s*(.+?)(?:\n|$)', personal.get('email', ''))
        if not phone:
            phone = self._extract_field(resume_content, r'Phone:\s*(.+?)(?:\n|$)', personal.get('phone', ''))
        if not location:
            location = self._extract_field(resume_content, r'Location:\s*(.+?)(?:\n|$)', personal.get('location', ''))
        if not linkedin:
            linkedin = self._extract_field(resume_content, r'LinkedIn:\s*(.+?)(?:\n|$)', personal.get('linkedin', ''))
        if not github:
            github = self._extract_field(resume_content, r'GitHub:\s*(.+?)(?:\n|$)', personal.get('github', ''))
        
        # Clean up LinkedIn and GitHub URLs (remove markdown links)
        if linkedin and '[' in linkedin:
            linkedin_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', linkedin)
            if linkedin_match:
                linkedin = linkedin_match.group(2)  # Extract the URL part
        if github and '[' in github:
            github_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', github)
            if github_match:
                github = github_match.group(2)  # Extract the URL part
        
        # If LinkedIn and GitHub are combined, split them
        if linkedin and 'GitHub:' in linkedin:
            parts = linkedin.split('GitHub:')
            linkedin = parts[0].strip()
            if len(parts) > 1:
                github = parts[1].strip()
        
        return {
            'name': name,
            'title': title,
            'email': email,
            'phone': phone,
            'location': location,
            'linkedin': linkedin,
            'github': github
        }
    
    def _extract_summary(self, resume_content: str) -> str:
        """Extract professional summary from resume content"""
        # Look for summary section with markdown headers
        summary_patterns = [
            r'### PROFESSIONAL SUMMARY[:\s]*(.+?)(?=###|$)',
            r'## PROFESSIONAL SUMMARY[:\s]*(.+?)(?=##|$)',
            r'### SUMMARY[:\s]*(.+?)(?=###|$)',
            r'## SUMMARY[:\s]*(.+?)(?=##|$)',
            r'Professional Summary[:\s]*(.+?)(?=\n\n|\n[A-Z][a-z]+ [A-Z]|$)',
            r'Summary[:\s]*(.+?)(?=\n\n|\n[A-Z][a-z]+ [A-Z]|$)',
            r'Profile[:\s]*(.+?)(?=\n\n|\n[A-Z][a-z]+ [A-Z]|$)',
            r'About[:\s]*(.+?)(?=\n\n|\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                summary = match.group(1).strip()
                # Clean up any remaining markdown formatting
                summary = re.sub(r'\*\*([^*]+)\*\*', r'\1', summary)  # Remove bold
                summary = re.sub(r'\*([^*]+)\*', r'\1', summary)      # Remove italic
                return summary
        
        # If no summary found, return first paragraph
        paragraphs = resume_content.split('\n\n')
        if paragraphs:
            first_para = paragraphs[0].strip()
            # Clean up markdown formatting
            first_para = re.sub(r'^#+\s*', '', first_para)  # Remove headers
            first_para = re.sub(r'\*\*([^*]+)\*\*', r'\1', first_para)  # Remove bold
            first_para = re.sub(r'\*([^*]+)\*', r'\1', first_para)      # Remove italic
            return first_para
        
        return "Professional with extensive experience in the field."
    
    def _extract_experience(self, resume_content: str, profile_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract work experience from resume content and profile data"""
        experience = []
        
        # First try to extract from profile data
        profile_experience = profile_data.get('experience', [])
        if profile_experience:
            for exp in profile_experience:
                # Convert description to bullets if it's a string
                bullets = []
                if isinstance(exp.get('description', ''), str):
                    bullets = [line.strip() for line in exp.get('description', '').split('\n') if line.strip()]
                elif isinstance(exp.get('bullets', []), list):
                    bullets = exp.get('bullets', [])
                
                experience.append({
                    'title': exp.get('title', ''),
                    'company': exp.get('company', ''),
                    'startDate': exp.get('start_date', ''),
                    'endDate': exp.get('end_date', 'Present'),
                    'bullets': bullets,
                    'impact': exp.get('impact', [])
                })
        
        # If no experience in profile, try to extract from resume content
        if not experience:
            experience = self._parse_experience_section(resume_content)
        
        return experience
    
    def _extract_education(self, resume_content: str, profile_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract education from resume content and profile data"""
        education = []
        
        # First try to extract from profile data
        profile_education = profile_data.get('education', [])
        if profile_education:
            for edu in profile_education:
                education.append({
                    'degree': edu.get('degree', ''),
                    'institution': edu.get('institution', ''),
                    'startDate': edu.get('start_date', ''),
                    'endDate': edu.get('end_date', ''),
                    'description': edu.get('description', '')
                })
        
        # If no education in profile, try to extract from resume content
        if not education:
            education = self._parse_education_section(resume_content)
        
        return education
    
    def _extract_skills_as_tags(self, resume_content: str, profile_data: Dict[str, Any]) -> List[str]:
        """Extract skills as a list of tags from resume content and profile data"""
        tags = []
        
        # First try to extract from profile data
        profile_skills = profile_data.get('skills', [])
        if profile_skills:
            for skill in profile_skills:
                # Handle both string and dictionary formats
                if isinstance(skill, dict):
                    skill_name = skill.get('name', '')
                elif isinstance(skill, str):
                    skill_name = skill
                else:
                    continue
                
                if skill_name and skill_name not in tags:
                    tags.append(skill_name)
        
        # If no skills in profile, try to extract from resume content
        if not tags:
            tags = self._parse_skills_as_tags(resume_content)
        
        return tags
    
    def _extract_core_skills(self, resume_content: str, profile_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extract core skills organized by category"""
        core_skills = {}
        
        # Look for core technical skills section
        skills_patterns = [
            r'### CORE TECHNICAL SKILLS[:\s]*(.+?)(?=###|$)',
            r'## CORE TECHNICAL SKILLS[:\s]*(.+?)(?=###|$)',
            r'### CORE COMPETENCIES[:\s]*(.+?)(?=###|$)',
            r'## CORE COMPETENCIES[:\s]*(.+?)(?=###|$)',
            r'### CORE COMPETENCES[:\s]*(.+?)(?=###|$)',
            r'## CORE COMPETENCES[:\s]*(.+?)(?=###|$)',
            r'### KEY COMPETENCIES[:\s]*(.+?)(?=###|$)',
            r'## KEY COMPETENCIES[:\s]*(.+?)(?=###|$)',
            r'CORE TECHNICAL SKILLS[:\s]*(.+?)(?=###|$)',
            r'---\s*\n### CORE TECHNICAL SKILLS[:\s]*(.+?)(?=---|###|$)',
        ]
        
        skills_content = ""
        for pattern in skills_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                skills_content = match.group(1)
                break
        
        if skills_content:
            # Handle bullet point format with categories
            if skills_content.strip().startswith('-'):
                skill_lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
                for line in skill_lines:
                    if line.startswith('-'):
                        # Remove bullet point and clean up
                        skill_line = re.sub(r'^-\s*', '', line)
                        
                        # Extract category and skills
                        if ':' in skill_line:
                            # Format: "**Category:** skill1, skill2, skill3"
                            category_match = re.match(r'\*\*([^*]+?):\*\*\s*(.+)', skill_line)
                            if category_match:
                                category = category_match.group(1).strip()
                                skills_part = category_match.group(2).strip()
                                
                                # Split skills by comma
                                skills = [skill.strip() for skill in re.split(r'[,;]', skills_part) if skill.strip()]
                                core_skills[category] = skills
            
            # Handle markdown table format
            elif '|' in skills_content:
                lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
                
                # Find all tables in the content
                tables = []
                current_table = []
                in_table = False
                
                for line in lines:
                    if '|' in line:
                        if not in_table:
                            in_table = True
                            current_table = []
                        current_table.append(line)
                    elif in_table and line.strip() == '':
                        if current_table:
                            tables.append(current_table)
                            current_table = []
                            in_table = False
                    elif in_table and not line.startswith('|---'):
                        current_table.append(line)
                
                # Add the last table if exists
                if current_table:
                    tables.append(current_table)
                
                # Process each table
                for table in tables:
                    if len(table) < 2:  # Need at least header and one data row
                        continue
                    
                    # Get header row
                    header_line = table[0]
                    categories = [part.strip() for part in header_line.split('|') if part.strip()]
                    
                    # Skip separator row if exists
                    data_start = 1
                    if len(table) > 1 and table[1].startswith('|---'):
                        data_start = 2
                    
                    # Check if this is a skills level table (Skills | Level)
                    if len(categories) == 2 and 'Skills' in categories[0] and 'Level' in categories[1]:
                        # This is a skills level table, skip it for core skills
                        continue
                    
                    # Process data rows
                    for i in range(data_start, len(table)):
                        data_line = table[i]
                        parts = [part.strip() for part in data_line.split('|') if part.strip()]
                        
                        if len(parts) >= len(categories):
                            for j, category in enumerate(categories):
                                if j < len(parts):
                                    skills_text = parts[j]
                                    # Clean up category name
                                    clean_category = re.sub(r'\*\*([^*]+)\*\*', r'\1', category)
                                    
                                    # Skip if this looks like a skills level table
                                    if clean_category in ['Skills', 'Level']:
                                        continue
                                    
                                    # Split by common separators
                                    skills = []
                                    for skill in re.split(r'[,;]', skills_text):
                                        skill = skill.strip()
                                        # Clean up skill name
                                        skill = re.sub(r'\*\*([^*]+)\*\*', r'\1', skill)
                                        if skill and len(skill) > 1 and skill not in ['Skills', 'Level', 'Technical', 'Process', 'Project', 'Tools', 'Platforms']:
                                            skills.append(skill)
                                    
                                    if skills:
                                        core_skills[clean_category] = skills
        
        return core_skills
    
    def _extract_languages(self, resume_content: str) -> List[str]:
        """Extract languages from resume content"""
        languages = []
        
        # Look for languages section
        languages_patterns = [
            r'### LANGUAGES[:\s]*(.+?)(?=###|$)',
            r'## LANGUAGES[:\s]*(.+?)(?=###|$)',
            r'### Languages[:\s]*(.+?)(?=###|$)',
            r'## Languages[:\s]*(.+?)(?=###|$)',
            r'Languages[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        languages_content = ""
        for pattern in languages_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                languages_content = match.group(1)
                break
        
        if languages_content:
            # Split by lines and extract languages
            language_lines = [line.strip() for line in languages_content.split('\n') if line.strip()]
            for line in language_lines:
                if line.startswith('-'):
                    # Remove bullet point
                    language = re.sub(r'^-\s*', '', line).strip()
                    if language and language != '--' and not language.startswith('('):
                        languages.append(language)
                else:
                    # Direct language entry
                    if line and not line.startswith('#') and line != '--' and not line.startswith('('):
                        languages.append(line)
        
        return languages
    
    def _extract_interests(self, resume_content: str) -> List[str]:
        """Extract interests from resume content"""
        interests = []
        
        # Look for interests section
        interests_patterns = [
            r'### INTERESTS[:\s]*(.+?)(?=###|$)',
            r'## INTERESTS[:\s]*(.+?)(?=###|$)',
            r'### Interests[:\s]*(.+?)(?=###|$)',
            r'## Interests[:\s]*(.+?)(?=###|$)',
            r'Interests[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        interests_content = ""
        for pattern in interests_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                interests_content = match.group(1)
                break
        
        if interests_content:
            # Split by lines and extract interests
            interest_lines = [line.strip() for line in interests_content.split('\n') if line.strip()]
            for line in interest_lines:
                if line.startswith('-'):
                    # Remove bullet point
                    interest = re.sub(r'^-\s*', '', line).strip()
                    if interest and interest != '--' and not interest.startswith('(') and not interest.startswith('*'):
                        interests.append(interest)
                else:
                    # Direct interest entry
                    if line and not line.startswith('#') and line != '--' and not line.startswith('(') and not line.startswith('*'):
                        interests.append(line)
        
        return interests
    
    def _extract_skills(self, resume_content: str, profile_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract skills from resume content and profile data"""
        skills = []
        
        # First try to extract from profile data
        profile_skills = profile_data.get('skills', [])
        if profile_skills:
            # Group skills by category
            skill_categories = {}
            for skill in profile_skills:
                # Handle both string and dictionary formats
                if isinstance(skill, dict):
                    category = skill.get('category', 'Technical Skills')
                    skill_name = skill.get('name', '')
                elif isinstance(skill, str):
                    # If skill is a string, treat it as the skill name
                    category = 'Technical Skills'
                    skill_name = skill
                else:
                    # Skip invalid skill formats
                    continue
                
                if category not in skill_categories:
                    skill_categories[category] = []
                skill_categories[category].append(skill_name)
            
            for category, skill_list in skill_categories.items():
                skills.append({
                    'category': category,
                    'skills': ', '.join(skill_list)
                })
        
        # If no skills in profile, try to extract from resume content
        if not skills:
            skills = self._parse_skills_section(resume_content)
        
        return skills
    
    def _extract_projects(self, resume_content: str, profile_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract projects from resume content and profile data"""
        projects = []
        
        # First try to extract from profile data
        profile_projects = profile_data.get('projects', [])
        if profile_projects:
            for project in profile_projects:
                # Handle both string and dictionary formats
                if isinstance(project, dict):
                    projects.append({
                        'name': project.get('name', ''),
                        'description': project.get('description', ''),
                        'date': project.get('date', '')
                    })
                elif isinstance(project, str):
                    # If project is a string, treat it as the project name
                    projects.append({
                        'name': project,
                        'description': '',
                        'date': ''
                    })
                # Skip invalid project formats
        
        # If no projects in profile, try to extract from resume content
        if not projects:
            projects = self._parse_projects_section(resume_content)
        
        return projects
    
    def _extract_certifications(self, resume_content: str, profile_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract certifications from resume content and profile data"""
        certifications = []
        
        # First try to extract from profile data
        profile_certifications = profile_data.get('certifications', [])
        if profile_certifications:
            for cert in profile_certifications:
                # Handle both string and dictionary formats
                if isinstance(cert, dict):
                    certifications.append({
                        'name': cert.get('name', ''),
                        'issuer': cert.get('issuer', ''),
                        'date': cert.get('date', '')
                    })
                elif isinstance(cert, str):
                    # If cert is a string, treat it as the certification name
                    certifications.append({
                        'name': cert,
                        'issuer': '',
                        'date': ''
                    })
                # Skip invalid certification formats
        
        # If no certifications in profile, try to extract from resume content
        if not certifications:
            certifications = self._parse_certifications_section(resume_content)
        
        return certifications
    
    def _extract_achievements(self, resume_content: str, profile_data: Dict[str, Any]) -> List[str]:
        """Extract achievements from resume content and profile data"""
        achievements = []
        
        # First try to extract from profile data
        profile_achievements = profile_data.get('achievements', [])
        if profile_achievements:
            achievements = profile_achievements
        
        # If no achievements in profile, try to extract from resume content
        if not achievements:
            achievements = self._parse_achievements_section(resume_content)
        
        return achievements
    
    def _extract_field(self, content: str, pattern: str, fallback: str = '') -> str:
        """Extract a field using regex pattern with fallback"""
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
        return fallback
    
    def _parse_experience_section(self, content: str) -> List[Dict[str, str]]:
        """Parse experience section from resume content"""
        experience = []
        
        # Look for experience section with markdown headers
        exp_patterns = [
            r'### PROFESSIONAL EXPERIENCE[:\s]*(.+?)(?=###|$)',
            r'## PROFESSIONAL EXPERIENCE[:\s]*(.+?)(?=##|$)',
            r'### EXPERIENCE[:\s]*(.+?)(?=###|$)',
            r'## EXPERIENCE[:\s]*(.+?)(?=##|$)',
            r'PROFESSIONAL EXPERIENCE[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)',
            r'EXPERIENCE[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        exp_content = ""
        for pattern in exp_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                exp_content = match.group(1)
                break
        
        if exp_content:
            # Handle AI-generated format:
            # **Job Title**
            # **Company, Location** | *Start Date – End Date*
            # - Bullet point 1
            # - Bullet point 2
            
            # Split by job entries - look for pattern: **Title** followed by **Company**
            jobs = re.split(r'\n(?=\*\*[^*]+\*\*\n\*\*[^*]+\*\*)', exp_content)
            
            for job in jobs:
                if job.strip():
                    lines = [line.strip() for line in job.strip().split('\n') if line.strip()]
                    
                    if len(lines) >= 2:
                        # First line: **Job Title**
                        title_match = re.search(r'\*\*([^*]+)\*\*', lines[0])
                        title = title_match.group(1) if title_match else lines[0]
                        
                        # Second line: **Company, Location** | *Start Date – End Date*
                        second_line = lines[1]
                        
                        # Extract company and location
                        company_match = re.search(r'\*\*([^*]+)\*\*', second_line)
                        company = company_match.group(1) if company_match else ""
                        
                        # Extract dates - look for pattern: | *Start Date – End Date*
                        date_match = re.search(r'\|\s*\*([^*]+)\*', second_line)
                        dates = date_match.group(1) if date_match else ""
                        
                        # Parse start and end dates
                        start_date = ""
                        end_date = ""
                        if dates:
                            date_parts = re.split(r'\s*[–-]\s*', dates)
                            if len(date_parts) >= 2:
                                start_date = date_parts[0].strip()
                                end_date = date_parts[1].strip()
                        
                        # Extract bullets (lines starting with - or •)
                        bullets = []
                        for line in lines[2:]:
                            if re.match(r'^[-•]\s*', line):
                                bullet = re.sub(r'^[-•]\s*', '', line)
                                # Clean up any remaining markdown formatting
                                bullet = re.sub(r'\*\*([^*]+)\*\*', r'\1', bullet)  # Remove bold
                                bullet = re.sub(r'\*([^*]+)\*', r'\1', bullet)      # Remove italic
                                bullets.append(bullet)
                        
                        experience.append({
                            'title': title,
                            'company': company,
                            'startDate': start_date,
                            'endDate': end_date,
                            'bullets': bullets,
                            'impact': []
                        })
        
        return experience
    
    def _parse_education_section(self, content: str) -> List[Dict[str, str]]:
        """Parse education section from resume content"""
        education = []
        
        # Look for education section
        edu_patterns = [
            r'### EDUCATION[:\s]*(.+?)(?=###|$)',
            r'## EDUCATION[:\s]*(.+?)(?=##|$)',
            r'Education[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        edu_content = ""
        for pattern in edu_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                edu_content = match.group(1)
                break
        
        if edu_content:
            # Handle AI-generated format: **Degree** – Institution | *Start Date – End Date*
            lines = [line.strip() for line in edu_content.split('\n') if line.strip()]
            
            for line in lines:
                if line.strip():
                    # Extract degree from bold format
                    degree_match = re.search(r'\*\*([^*]+)\*\*', line)
                    degree = degree_match.group(1) if degree_match else line
                    
                    # Extract institution from the line
                    institution_match = re.search(r'–\s*([^|]+)', line)
                    institution = institution_match.group(1).strip() if institution_match else ""
                    
                    # Extract dates from italic format
                    date_match = re.search(r'\|\s*\*([^*]+)\*', line)
                    dates = date_match.group(1) if date_match else ""
                    
                    education.append({
                        'name': f"{degree} – {institution}" if institution else degree,
                        'dates': dates,
                        'degree': degree,
                        'institution': institution,
                        'startDate': dates.split('–')[0].strip() if '–' in dates else "",
                        'endDate': dates.split('–')[1].strip() if '–' in dates else ""
                    })
        
        return education
    
    def _parse_skills_section(self, content: str) -> List[Dict[str, str]]:
        """Parse skills section from resume content"""
        skills = []
        
        # Look for skills section
        skills_pattern = r'Skills[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        match = re.search(skills_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            skills_content = match.group(1)
            # Split by lines and group into categories
            skill_lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
            
            if skill_lines:
                skills.append({
                    'category': 'Technical Skills',
                    'skills': ', '.join(skill_lines)
                })
        
        return skills
    
    def _parse_projects_section(self, content: str) -> List[Dict[str, str]]:
        """Parse projects section from resume content"""
        projects = []
        
        # Look for projects section
        projects_patterns = [
            r'### PROJECTS[:\s]*(.+?)(?=###|$)',
            r'## PROJECTS[:\s]*(.+?)(?=##|$)',
            r'### Selected Projects[:\s]*(.+?)(?=###|$)',
            r'## Selected Projects[:\s]*(.+?)(?=##|$)',
            r'### RELEVANT PROJECTS[:\s]*(.+?)(?=###|$)',
            r'## RELEVANT PROJECTS[:\s]*(.+?)(?=##|$)',
            r'Projects[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        projects_content = ""
        for pattern in projects_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                projects_content = match.group(1)
                break
        
        if projects_content:
            # Check if it's a markdown table format
            if '|' in projects_content and '---' in projects_content:
                # Parse markdown table
                lines = [line.strip() for line in projects_content.split('\n') if line.strip()]
                table_lines = []
                for line in lines:
                    if '|' in line and not line.startswith('|---'):
                        table_lines.append(line)
                
                for line in table_lines[1:]:  # Skip header row
                    if '|' in line:
                        parts = [part.strip() for part in line.split('|') if part.strip()]
                        if len(parts) >= 3:
                            projects.append({
                                'name': parts[0],
                                'stack': parts[1],  # Tools
                                'desc': [parts[2]] if parts[2] else []  # Impact as list
                            })
            else:
                # Parse as bullet point format (new website format)
                lines = [line.strip() for line in projects_content.split('\n') if line.strip()]
                
                for line in lines:
                    if line.startswith('- **') and '** –' in line:
                        # Format: - **Project Name** – Description
                        project_match = re.match(r'-\s*\*\*([^*]+)\*\* – (.+)', line)
                        if project_match:
                            project_name = project_match.group(1)
                            description = project_match.group(2)
                            
                            # Try to extract tools from description
                            tools = []
                            if 'Powered by' in description:
                                tools_match = re.search(r'Powered by ([^.]+)', description)
                                if tools_match:
                                    tools = [tool.strip() for tool in tools_match.group(1).split('&')]
                            
                            projects.append({
                                'name': project_name,
                                'stack': ', '.join(tools) if tools else '',
                                'desc': [description]
                            })
                    elif line.startswith('- **'):
                        # Format: - **Project Name** – Description
                        project_match = re.match(r'-\s*\*\*([^*]+)\*\*', line)
                        if project_match:
                            project_name = project_match.group(1)
                            projects.append({
                                'name': project_name,
                                'stack': '',
                                'desc': [line.replace(f'- **{project_name}**', '').strip()]
                            })
        
        return projects
    
    def _parse_certifications_section(self, content: str) -> List[Dict[str, str]]:
        """Parse certifications section from resume content"""
        certifications = []
        
        # Look for certifications section
        cert_patterns = [
            r'### CERTIFICATIONS[:\s]*(.+?)(?=###|$)',
            r'## CERTIFICATIONS[:\s]*(.+?)(?=##|$)',
            r'CERTIFICATIONS[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)',
            r'Certifications[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)',
            r'### CERTIFICATIONS & TRAINING[:\s]*(.+?)(?=###|$)',
            r'## CERTIFICATIONS & TRAINING[:\s]*(.+?)(?=###|$)',
        ]
        
        cert_content = ""
        for pattern in cert_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                cert_content = match.group(1)
                break
        
        if cert_content:
            # Check if it's a table format
            if '|' in cert_content and '---' in cert_content:
                # Parse table format
                lines = [line.strip() for line in cert_content.split('\n') if line.strip()]
                table_lines = []
                for line in lines:
                    if '|' in line and not line.startswith('|---'):
                        table_lines.append(line)
                
                for line in table_lines[1:]:  # Skip header row
                    if '|' in line:
                        parts = [part.strip() for part in line.split('|') if part.strip()]
                        if len(parts) >= 2:
                            # Format: Credential | Provider | Year
                            credential = parts[0]
                            provider = parts[1] if len(parts) > 1 else ''
                            year = parts[2] if len(parts) > 2 else ''
                            
                            # Clean up markdown formatting
                            credential = re.sub(r'\*\*([^*]+)\*\*', r'\1', credential)
                            provider = re.sub(r'\*\*([^*]+)\*\*', r'\1', provider)
                            
                            if credential and credential != 'Credential':
                                cert_text = f"{credential} – {provider}"
                                if year and year != 'Year' and year != '•':
                                    cert_text += f" ({year})"
                                certifications.append(cert_text)
            else:
                # Parse bullet point format
                cert_lines = [line.strip() for line in cert_content.split('\n') if line.strip()]
                
                for cert in cert_lines:
                    if cert.strip() and not cert.startswith('|') and not cert.startswith('---') and not cert.startswith('&'):
                        # Clean up markdown formatting
                        cert_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', cert)  # Remove bold
                        cert_clean = re.sub(r'\*([^*]+)\*', r'\1', cert_clean)  # Remove italic
                        # Remove bullet points
                        cert_clean = re.sub(r'^-\s*', '', cert_clean)
                        if cert_clean.strip():
                            certifications.append(cert_clean)
        
        return certifications
    
    def _parse_achievements_section(self, content: str) -> List[str]:
        """Parse achievements section from resume content"""
        achievements = []
        
        # Look for achievements section
        achievements_pattern = r'Achievements[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        match = re.search(achievements_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            achievements_content = match.group(1)
            # Split by lines
            achievement_lines = [line.strip() for line in achievements_content.split('\n') if line.strip()]
            achievements = achievement_lines
        
        return achievements
    
    def _parse_skills_as_tags(self, content: str) -> List[str]:
        """Parse skills as tags from resume content"""
        tags = []
        
        # Look for skills section with markdown headers
        skills_patterns = [
            r'### CORE TECHNICAL SKILLS[:\s]*(.+?)(?=###|$)',
            r'## CORE TECHNICAL SKILLS[:\s]*(.+?)(?=##|$)',
            r'### CORE COMPETENCIES[:\s]*(.+?)(?=###|$)',
            r'## CORE COMPETENCIES[:\s]*(.+?)(?=##|$)',
            r'### KEY COMPETENCIES[:\s]*(.+?)(?=###|$)',
            r'## KEY COMPETENCIES[:\s]*(.+?)(?=##|$)',
            r'### SKILLS[:\s]*(.+?)(?=###|$)',
            r'## SKILLS[:\s]*(.+?)(?=##|$)',
            r'Skills[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        skills_content = ""
        for pattern in skills_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                skills_content = match.group(1)
                break
        
        if skills_content:
            # Handle bullet point format (like in your resume)
            if skills_content.strip().startswith('-'):
                skill_lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
                for line in skill_lines:
                    if line.startswith('-'):
                        # Remove bullet point and clean up
                        skill_line = re.sub(r'^-\s*\*\*([^*]+)\*\*:\s*', r'\1: ', line)
                        skill_line = re.sub(r'^-\s*', '', skill_line)
                        
                        # Extract skills from the line
                        if ':' in skill_line:
                            # Format: "Category: skill1, skill2, skill3"
                            category, skills_part = skill_line.split(':', 1)
                            skills_in_part = re.split(r'[,;]', skills_part)
                            for skill in skills_in_part:
                                skill = skill.strip()
                                # Clean up markdown formatting
                                skill = re.sub(r'\*\*([^*]+)\*\*', r'\1', skill)  # Remove bold
                                skill = re.sub(r'\*([^*]+)\*', r'\1', skill)      # Remove italic
                                skill = re.sub(r'^\*\*', '', skill)  # Remove leading **
                                skill = re.sub(r'\*\*$', '', skill)  # Remove trailing **
                                if skill and skill not in tags and len(skill) > 1 and skill != '**':
                                    tags.append(skill)
                        else:
                            # Single skill or category
                            skill = skill_line.strip()
                            # Clean up markdown formatting
                            skill = re.sub(r'\*\*([^*]+)\*\*', r'\1', skill)  # Remove bold
                            skill = re.sub(r'\*([^*]+)\*', r'\1', skill)      # Remove italic
                            skill = re.sub(r'^\*\*', '', skill)  # Remove leading **
                            skill = re.sub(r'\*\*$', '', skill)  # Remove trailing **
                            if skill and skill not in tags and len(skill) > 1 and skill != '**':
                                tags.append(skill)
            # Handle markdown table format
            elif '|' in skills_content:
                # Parse markdown table
                lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
                for line in lines:
                    if '|' in line and not line.startswith('|---'):
                        # Split by pipe and extract skills
                        parts = [part.strip() for part in line.split('|') if part.strip()]
                        for part in parts:
                            # Skip table headers
                            if not re.match(r'^[A-Z\s&]+$', part) and part not in ['Category', 'Highlights', 'Technical', 'Process & Project', 'Soft & Leadership']:
                                # Split by common separators
                                skills_in_part = re.split(r'[,;]', part)
                                for skill in skills_in_part:
                                    skill = skill.strip()
                                    if skill and skill not in tags and len(skill) > 1:
                                        tags.append(skill)
            else:
                # Handle regular text format
                skill_lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
                for line in skill_lines:
                    # Split by common separators
                    skills_in_line = re.split(r'[,;|•\-\n]', line)
                    for skill in skills_in_line:
                        skill = skill.strip()
                        if skill and skill not in tags and len(skill) > 1:
                            tags.append(skill)
        
        return tags
