"""
Manual template processor that handles the specific patterns we need
"""
import re
from typing import Dict, Any, List

def process_template_manually(template_content: str, data: Dict[str, Any]) -> str:
    """Manually process template with specific patterns"""
    content = template_content
    
    # Handle simple variable substitution
    for key, value in data.items():
        if isinstance(value, str):
            content = content.replace(f'{{{{{key}}}}}', value)
        elif isinstance(value, (int, float)):
            content = content.replace(f'{{{{{key}}}}}', str(value))
        elif value is None:
            content = content.replace(f'{{{{{key}}}}}', '')
    
    # Handle experience section
    if 'experience' in data and isinstance(data['experience'], list):
        experience_html = ""
        for exp in data['experience']:
            bullets_html = ""
            if 'bullets' in exp and isinstance(exp['bullets'], list):
                for bullet in exp['bullets']:
                    # Skip empty bullets or dashes
                    if bullet.strip() and bullet.strip() != '--':
                        bullets_html += f"<li>{bullet}</li>\n"
            
            # Add impact section if there are impact items
            impact_html = ""
            if 'impact' in exp and isinstance(exp['impact'], list) and exp['impact']:
                impact_items = ""
                for impact in exp['impact']:
                    if impact.strip():
                        impact_items += f"<li>{impact}</li>\n"
                if impact_items:
                    impact_html = f"""
                    <div class="subhead">Key impact</div>
                    <ul class="bullets">
                        {impact_items}
                    </ul>
                    """
            
            experience_html += f"""
                <section class="entry">
                    <div class="entry-head">
                        <div class="entry-title">{exp.get('title', '')} <span class="at">·</span> <span class="company">{exp.get('company', '')}</span></div>
                        <div class="dates">{exp.get('startDate', '')} – {exp.get('endDate', '')}</div>
                    </div>
                    <ul class="bullets">
                        {bullets_html}
                    </ul>
                    {impact_html}
                </section>
            """
        
        # Replace the experience section
        exp_pattern = r'<div class="section-title">Experience</div>\s*{{#each experience}}.*?{{/each}}\s*</section>'
        content = re.sub(exp_pattern, f'<div class="section-title">Experience</div>\n{experience_html}\n            </section>', content, flags=re.DOTALL)
    
    # Handle projects section
    if 'projects' in data and isinstance(data['projects'], list):
        projects_html = ""
        for project in data['projects']:
            desc_html = ""
            if 'desc' in project and isinstance(project['desc'], list):
                for desc in project['desc']:
                    desc_html += f"<li>{desc}</li>\n"
            
            # Clean up project name (remove markdown formatting)
            project_name = project.get('name', '')
            project_name = re.sub(r'\*\*([^*]+)\*\*', r'\1', project_name)  # Remove bold
            project_name = re.sub(r'\*([^*]+)\*', r'\1', project_name)      # Remove italic
            
            projects_html += f"""
                <section class="entry">
                    <div class="entry-head">
                        <div class="entry-title">{project_name} <span class="stack">— {project.get('stack', '')}</span></div>
                    </div>
                    <ul class="bullets">
                        {desc_html}
                    </ul>
                </section>
            """
        
        # Replace the projects section
        proj_pattern = r'<div class="section-title">Projects</div>\s*{{#each projects}}.*?{{/each}}'
        content = re.sub(proj_pattern, f'<div class="section-title">Projects</div>\n{projects_html}', content, flags=re.DOTALL)
    
    # Handle education section
    if 'education' in data and isinstance(data['education'], list):
        education_html = ""
        for edu in data['education']:
            # Clean up education name (remove markdown formatting)
            edu_name = edu.get('name', '')
            edu_name = re.sub(r'\*\*([^*]+)\*\*', r'\1', edu_name)  # Remove bold
            edu_name = re.sub(r'\*([^*]+)\*', r'\1', edu_name)      # Remove italic
            
            education_html += f"""
                <div class='edu-item'>
                    <div class="edu-line">{edu_name}</div>
                    <div class='edu-dates'>{edu.get('dates', '')}</div>
                </div>
            """
        
        # Replace the education section
        edu_pattern = r'<div class="section-title">Education</div>\s*{{#each education}}.*?{{/each}}'
        content = re.sub(edu_pattern, f'<div class="section-title">Education</div>\n{education_html}', content, flags=re.DOTALL)
    
    # Handle certifications section
    if 'certifications' in data and isinstance(data['certifications'], list):
        cert_html = ""
        for cert in data['certifications']:
            cert_html += f"<li>{cert}</li>\n"
        
        # Replace the certifications section
        cert_pattern = r'<div class="section-title">Certifications[^<]*</div>\s*<ul class="bullets">\s*{{#each certifications}}.*?{{/each}}\s*</ul>'
        content = re.sub(cert_pattern, f'<div class="section-title">Certifications</div>\n<ul class="bullets">\n{cert_html}</ul>', content, flags=re.DOTALL)
    
    # Handle tags section
    if 'tags' in data and isinstance(data['tags'], list):
        tags_html = ""
        for tag in data['tags']:
            # Clean up any remaining markdown formatting
            clean_tag = re.sub(r'\*\*([^*]+)\*\*', r'\1', tag)  # Remove bold
            clean_tag = re.sub(r'\*([^*]+)\*', r'\1', clean_tag)  # Remove italic
            clean_tag = clean_tag.strip()
            if clean_tag and clean_tag != '--' and len(clean_tag) > 1:
                tags_html += f'<span class="chip">{clean_tag}</span>\n'
        
        # Replace the tags section
        tags_pattern = r'<div class="tags">\s*{{#each tags}}.*?{{/each}}\s*</div>'
        content = re.sub(tags_pattern, f'<div class="tags">\n{tags_html}</div>', content, flags=re.DOTALL)
    
    # Handle core skills section
    if 'core_skills' in data and isinstance(data['core_skills'], dict) and data['core_skills']:
        core_skills_html = ""
        for category, skills in data['core_skills'].items():
            skills_list = ', '.join(skills)
            core_skills_html += f'<div class="skill-category"><strong>{category}:</strong> {skills_list}</div>\n'
        
        # Replace the existing core skills section
        core_skills_section = f'''
            <section class="section">
                <div class="section-title">Core Skills</div>
                <div class="core-skills">
                    {core_skills_html}
                </div>
            </section>
        '''
        
        # Replace the existing core skills section
        core_skills_pattern = r'<section class="section">\s*<div class="section-title">Core Skills</div>.*?</section>'
        content = re.sub(core_skills_pattern, core_skills_section, content, flags=re.DOTALL)
    
    # Handle languages section
    if 'languages' in data and isinstance(data['languages'], list) and data['languages']:
        languages_html = ""
        for language in data['languages']:
            languages_html += f"<li>{language}</li>\n"
        
        languages_section = f'''
            <section class="section">
                <div class="section-title">Languages</div>
                <ul class="bullets">
                    {languages_html}
                </ul>
            </section>
        '''
        
        # Add languages section after certifications
        content = content.replace('</main>', f'{languages_section}\n        </main>')
    
    # Handle interests section
    if 'interests' in data and isinstance(data['interests'], list) and data['interests']:
        interests_html = ""
        for interest in data['interests']:
            interests_html += f"<li>{interest}</li>\n"
        
        interests_section = f'''
            <section class="section">
                <div class="section-title">Interests</div>
                <ul class="bullets">
                    {interests_html}
                </ul>
            </section>
        '''
        
        # Add interests section after languages
        content = content.replace('</main>', f'{interests_section}\n        </main>')
    
    # Remove empty sections that are not populated
    empty_sections = [
        r'<section class="section">\s*<div class="section-title">Selected Technical Strengths</div>.*?</section>',
        r'<section class="section">\s*<div class="section-title">Additional</div>.*?</section>',
        r'<section class="section">\s*<div class="section-title">How this matches the role</div>.*?</section>',
    ]
    
    for pattern in empty_sections:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Remove any remaining template syntax
    content = re.sub(r'\{\{[^}]+\}\}', '', content)
    
    return content
