#!/usr/bin/env python3
"""
Flexible Resume Processor that handles optional sections
"""
import re
from typing import Dict, List, Any, Optional

class FlexibleResumeProcessor:
    """Process resume content with flexible section handling"""
    
    def __init__(self):
        self.required_sections = [
            'name', 'title', 'email', 'phone', 'location', 
            'summary', 'experience', 'education', 'languages'
        ]
        self.optional_sections = [
            'linkedin', 'github', 'certifications', 'projects', 
            'core_skills', 'interests', 'achievements', 'additional'
        ]
    
    def process_resume_content(self, resume_content: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process resume content and return structured data"""
        
        # Extract personal information
        personal_info = self._extract_personal_info(resume_content)
        
        # Extract required sections
        summary = self._extract_summary(resume_content)
        experience = self._parse_experience_section(resume_content)
        education = self._parse_education_section(resume_content)
        languages = self._extract_languages(resume_content)
        
        # Extract optional sections
        linkedin = personal_info.get('linkedin', '')
        github = personal_info.get('github', '')
        certifications = self._parse_certifications_section(resume_content)
        projects = self._parse_projects_section(resume_content)
        core_skills = self._extract_core_skills(resume_content, {})
        interests = self._extract_interests(resume_content)
        
        # Extract skills as tags (for backward compatibility)
        tags = self._extract_skills_as_tags(resume_content)
        
        # Build structured data
        structured_data = {
            'name': personal_info.get('name', ''),
            'title': personal_info.get('title', ''),
            'email': personal_info.get('email', ''),
            'phone': personal_info.get('phone', ''),
            'location': personal_info.get('location', ''),
            'linkedin': linkedin,
            'github': github,
            'summary': summary,
            'experience': experience,
            'education': education,
            'languages': languages,
            'tags': tags,
            'core_skills': core_skills,
            'interests': interests,
            'certifications': certifications,
            'projects': projects,
            'achievements': [],
            'strengths': [],
            'additional': '',
            'fit': '',
            'currentYear': '2025'
        }
        
        return structured_data
    
    def _extract_personal_info(self, resume_content: str) -> Dict[str, str]:
        """Extract personal information from resume content"""
        lines = [line.strip() for line in resume_content.split('\n') if line.strip()]
        
        if not lines:
            return {}
        
        # First line is name
        name = lines[0].replace('**', '').strip()
        
        # Second line is title and skills
        title_line = lines[1] if len(lines) > 1 else ''
        title = title_line.split('|')[0].strip() if '|' in title_line else title_line
        
        # Third line is location
        location = lines[2] if len(lines) > 2 else ''
        
        # Fourth line is contact info
        contact_line = lines[3] if len(lines) > 3 else ''
        
        # Extract contact details
        email = ""
        phone = ""
        linkedin = ""
        github = ""
        
        if contact_line:
            # Clean up emoji prefixes
            clean_line = re.sub(r'^[📞📧🔗👨‍💻]\s*', '', contact_line)
            
            # Split by pipe or other separators
            parts = re.split(r'[|•]', clean_line)
            
            for part in parts:
                part = part.strip()
                if '@' in part:
                    email = part
                elif 'linkedin.com' in part.lower():
                    # Extract URL from markdown link format
                    linkedin_match = re.search(r'\[LinkedIn\]\(([^)]+)\)|<([^>]+)>', part)
                    if linkedin_match:
                        linkedin = linkedin_match.group(1) or linkedin_match.group(2)
                    else:
                        linkedin = part
                elif 'github.com' in part.lower():
                    # Extract URL from markdown link format
                    github_match = re.search(r'\[GitHub\]\(([^)]+)\)|<([^>]+)>', part)
                    if github_match:
                        github = github_match.group(1) or github_match.group(2)
                    else:
                        github = part
                elif '+' in part or (any(char.isdigit() for char in part) and 'linkedin.com' not in part.lower() and 'github.com' not in part.lower()):
                    phone = part
        
        return {
            'name': name,
            'title': title,
            'location': location,
            'email': email,
            'phone': phone,
            'linkedin': linkedin,
            'github': github
        }
    
    def _extract_summary(self, resume_content: str) -> str:
        """Extract professional summary"""
        summary_patterns = [
            r'### Professional Summary[:\s]*(.+?)(?=###|$)',
            r'## Professional Summary[:\s]*(.+?)(?=###|$)',
            r'Professional Summary[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                summary = match.group(1).strip()
                # Clean up markdown formatting
                summary = re.sub(r'\*\*([^*]+)\*\*', r'\1', summary)
                summary = re.sub(r'\*([^*]+)\*', r'\1', summary)
                return summary
        
        return ""
    
    def _parse_experience_section(self, resume_content: str) -> List[Dict[str, str]]:
        """Parse experience section"""
        experience = []
        
        # Look for experience section
        exp_patterns = [
            r'### Professional Experience[:\s]*(.+?)(?=###|$)',
            r'## Professional Experience[:\s]*(.+?)(?=###|$)',
            r'### Experience[:\s]*(.+?)(?=###|$)',
            r'## Experience[:\s]*(.+?)(?=###|$)',
            r'Professional Experience[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        exp_content = ""
        for pattern in exp_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                exp_content = match.group(1)
                break
        
        if exp_content:
            # Split by job entries - look for job titles that don't contain company info
            jobs = re.split(r'\n(?=\*\*[^*]+(?!.*(?:Global|Poland|Denmark|Mar|Apr|Jul|Present|2025|2024|2021))\*\*)', exp_content)
            
            for job in jobs:
                if job.strip():
                    lines = [line.strip() for line in job.strip().split('\n') if line.strip()]
                    
                    if lines:
                        # First line is job title
                        title = lines[0].replace('**', '').strip()
                        
                        # Second line is company and dates
                        company = ""
                        start_date = ""
                        end_date = ""
                        bullet_start_index = 1
                        
                        if len(lines) > 1:
                            second_line = lines[1]
                            
                            # Extract company from bold text
                            company_match = re.search(r'\*\*([^*]+)\*\*', second_line)
                            if company_match:
                                company = company_match.group(1)
                            
                            # Extract dates
                            date_match = re.search(r'(\w+\s+\d{4})\s*[–-]\s*(\w+\s+\d{4}|Present)', second_line)
                            if date_match:
                                start_date = date_match.group(1)
                                end_date = date_match.group(2)
                                bullet_start_index = 2
                        
                        # If no dates found in second line, look in the next few lines
                        if not start_date:
                            for i, line in enumerate(lines[2:5], 2):  # Check next 3 lines
                                date_match = re.search(r'(\w+\s+\d{4})\s*[–-]\s*(\w+\s+\d{4}|Present)', line)
                                if date_match:
                                    start_date = date_match.group(1)
                                    end_date = date_match.group(2)
                                    bullet_start_index = i + 1
                                    break
                        
                        # Extract bullets
                        bullets = []
                        for line in lines[bullet_start_index:]:
                            if line.startswith('-'):
                                bullet = re.sub(r'^-\s*', '', line)
                                # Clean up markdown formatting
                                bullet = re.sub(r'\*\*([^*]+)\*\*', r'\1', bullet)
                                bullet = re.sub(r'\*([^*]+)\*', r'\1', bullet)
                                bullets.append(bullet)
                        
                        experience.append({
                            'title': title,
                            'company': company,
                            'startDate': start_date,
                            'endDate': end_date,
                            'bullets': bullets,
                            'impact': bullets  # For backward compatibility
                        })
        
        return experience
    
    def _parse_education_section(self, resume_content: str) -> List[Dict[str, str]]:
        """Parse education section"""
        education = []
        
        # Look for education section
        edu_patterns = [
            r'### Education[:\s]*(.+?)(?=###|$)',
            r'## Education[:\s]*(.+?)(?=###|$)',
            r'Education[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        edu_content = ""
        for pattern in edu_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                edu_content = match.group(1)
                break
        
        if edu_content:
            lines = [line.strip() for line in edu_content.split('\n') if line.strip()]
            
            for line in lines:
                if line.startswith('**') and '–' in line:
                    # Extract degree and institution
                    degree_match = re.search(r'\*\*([^*]+)\*\* – ([^*]+)', line)
                    if degree_match:
                        degree = degree_match.group(1)
                        institution = degree_match.group(2)
                        
                        # Extract dates if present
                        date_match = re.search(r'(\w+\s+\d{4})\s*[–-]\s*(\w+\s+\d{4})', line)
                        start_date = ""
                        end_date = ""
                        if date_match:
                            start_date = date_match.group(1)
                            end_date = date_match.group(2)
                        
                        education.append({
                            'degree': degree,
                            'institution': institution,
                            'startDate': start_date,
                            'endDate': end_date
                        })
        
        return education
    
    def _extract_languages(self, resume_content: str) -> List[str]:
        """Extract languages"""
        languages = []
        
        # Look for languages section
        lang_patterns = [
            r'### Languages[:\s]*(.+?)(?=###|$)',
            r'## Languages[:\s]*(.+?)(?=###|$)',
            r'Languages[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        lang_content = ""
        for pattern in lang_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                lang_content = match.group(1)
                break
        
        if lang_content:
            lines = [line.strip() for line in lang_content.split('\n') if line.strip()]
            for line in lines:
                if line.startswith('-'):
                    lang = re.sub(r'^-\s*', '', line)
                    # Clean up markdown formatting
                    lang = re.sub(r'\*\*([^*]+)\*\*', r'\1', lang)
                    lang = re.sub(r'\*([^*]+)\*', r'\1', lang)
                    if lang and lang != '--':
                        languages.append(lang)
        
        return languages
    
    def _parse_certifications_section(self, resume_content: str) -> List[str]:
        """Parse certifications section"""
        certifications = []
        
        # Look for certifications section
        cert_patterns = [
            r'### Certifications[:\s]*(.+?)(?=###|$)',
            r'## Certifications[:\s]*(.+?)(?=###|$)',
            r'### Certifications & Training[:\s]*(.+?)(?=###|$)',
            r'## Certifications & Training[:\s]*(.+?)(?=###|$)',
            r'Certifications[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        cert_content = ""
        for pattern in cert_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
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
                lines = [line.strip() for line in cert_content.split('\n') if line.strip()]
                for line in lines:
                    if line.startswith('-') and not line.startswith('|---'):
                        cert = re.sub(r'^-\s*', '', line)
                        # Clean up markdown formatting
                        cert = re.sub(r'\*\*([^*]+)\*\*', r'\1', cert)
                        cert = re.sub(r'\*([^*]+)\*', r'\1', cert)
                        if cert and cert != '& TRAINING':
                            certifications.append(cert)
        
        return certifications
    
    def _parse_projects_section(self, resume_content: str) -> List[Dict[str, str]]:
        """Parse projects section"""
        projects = []
        
        # Look for projects section
        proj_patterns = [
            r'### Selected Projects[:\s]*(.+?)(?=###|$)',
            r'## Selected Projects[:\s]*(.+?)(?=###|$)',
            r'### Projects[:\s]*(.+?)(?=###|$)',
            r'## Projects[:\s]*(.+?)(?=###|$)',
            r'Projects[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        proj_content = ""
        for pattern in proj_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                proj_content = match.group(1)
                break
        
        if proj_content:
            # Check if it's a table format
            if '|' in proj_content and '---' in proj_content:
                # Parse table format
                lines = [line.strip() for line in proj_content.split('\n') if line.strip()]
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
                                'stack': parts[1],
                                'desc': [parts[2]] if parts[2] else []
                            })
            else:
                # Parse bullet point format
                lines = [line.strip() for line in proj_content.split('\n') if line.strip()]
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
        
        return projects
    
    def _extract_core_skills(self, resume_content: str, profile_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extract core skills organized by category"""
        core_skills = {}
        
        # Look for core skills section
        skills_patterns = [
            r'### Core Technical Skills[:\s]*(.+?)(?=###|$)',
            r'## Core Technical Skills[:\s]*(.+?)(?=###|$)',
            r'### Key Competencies[:\s]*(.+?)(?=###|$)',
            r'## Key Competencies[:\s]*(.+?)(?=###|$)',
            r'Core Technical Skills[:\s]*(.+?)(?=###|$)'
        ]
        
        skills_content = ""
        for pattern in skills_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                skills_content = match.group(1)
                break
        
        if skills_content:
            # Handle table format
            if '|' in skills_content and '---' in skills_content:
                lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
                table_lines = []
                for line in lines:
                    if '|' in line and not line.startswith('|---'):
                        table_lines.append(line)
                
                if table_lines:
                    # Get header row
                    header_line = table_lines[0]
                    categories = [part.strip() for part in header_line.split('|') if part.strip()]
                    
                    # Process data rows
                    for i in range(1, len(table_lines)):
                        data_line = table_lines[i]
                        parts = [part.strip() for part in data_line.split('|') if part.strip()]
                        
                        if len(parts) >= len(categories):
                            for j, category in enumerate(categories):
                                if j < len(parts):
                                    skills_text = parts[j]
                                    clean_category = re.sub(r'\*\*([^*]+)\*\*', r'\1', category)
                                    
                                    # Split by common separators
                                    skills = []
                                    for skill in re.split(r'[,;]', skills_text):
                                        skill = skill.strip()
                                        skill = re.sub(r'\*\*([^*]+)\*\*', r'\1', skill)
                                        if skill and len(skill) > 1:
                                            skills.append(skill)
                                    
                                    if skills:
                                        core_skills[clean_category] = skills
            
            # Handle bullet point format
            elif skills_content.strip().startswith('-'):
                lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
                for line in lines:
                    if line.startswith('-'):
                        skill_line = re.sub(r'^-\s*', '', line)
                        if ':' in skill_line:
                            category_match = re.match(r'\*\*([^*]+?):\*\*\s*(.+)', skill_line)
                            if category_match:
                                category = category_match.group(1).strip()
                                skills_part = category_match.group(2).strip()
                                skills = [skill.strip() for skill in re.split(r'[,;]', skills_part) if skill.strip()]
                                core_skills[category] = skills
        
        return core_skills
    
    def _extract_skills_as_tags(self, resume_content: str) -> List[str]:
        """Extract skills as tags for backward compatibility"""
        tags = []
        
        # Look for skills section
        skills_patterns = [
            r'### Key Competencies[:\s]*(.+?)(?=###|$)',
            r'## Key Competencies[:\s]*(.+?)(?=###|$)',
            r'### Core Technical Skills[:\s]*(.+?)(?=###|$)',
            r'## Core Technical Skills[:\s]*(.+?)(?=###|$)',
            r'Skills[:\s]*(.+?)(?=\n\n[A-Z][a-z]+ [A-Z]|$)'
        ]
        
        skills_content = ""
        for pattern in skills_patterns:
            match = re.search(pattern, resume_content, re.DOTALL | re.IGNORECASE)
            if match:
                skills_content = match.group(1)
                break
        
        if skills_content:
            # Handle table format
            if '|' in skills_content and '---' in skills_content:
                lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
                for line in lines:
                    if '|' in line and not line.startswith('|---'):
                        parts = [part.strip() for part in line.split('|') if part.strip()]
                        for part in parts:
                            # Split by common separators
                            for skill in re.split(r'[,;]', part):
                                skill = skill.strip()
                                skill = re.sub(r'\*\*([^*]+)\*\*', r'\1', skill)
                                if skill and len(skill) > 1 and skill not in ['Technical', 'Process', 'Project', 'Soft', 'Leadership']:
                                    tags.append(skill)
            
            # Handle bullet point format
            elif skills_content.strip().startswith('-'):
                lines = [line.strip() for line in skills_content.split('\n') if line.strip()]
                for line in lines:
                    if line.startswith('-'):
                        skill = re.sub(r'^-\s*', '', line)
                        skill = re.sub(r'\*\*([^*]+)\*\*', r'\1', skill)
                        if skill and skill != '--':
                            tags.append(skill)
        
        return tags
    
    def _extract_interests(self, resume_content: str) -> List[str]:
        """Extract interests"""
        interests = []
        
        # Look for interests section
        interests_patterns = [
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
            lines = [line.strip() for line in interests_content.split('\n') if line.strip()]
            for line in lines:
                if line.startswith('-'):
                    interest = re.sub(r'^-\s*', '', line)
                    # Clean up markdown formatting
                    interest = re.sub(r'\*\*([^*]+)\*\*', r'\1', interest)
                    interest = re.sub(r'\*([^*]+)\*', r'\1', interest)
                    if interest and interest != '--':
                        interests.append(interest)
                else:
                    # Handle comma-separated interests
                    if ',' in line:
                        for interest in line.split(','):
                            interest = interest.strip()
                            if interest:
                                interests.append(interest)
        
        return interests
