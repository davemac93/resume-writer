#!/usr/bin/env python3
"""
Simple test for template rendering with projects
"""
from template_engine import TemplateEngine

def test_simple_template():
    print("🔍 Testing simple template rendering...")
    
    # Simple test data
    test_data = {
        "name": "Test User",
        "projects": [
            {
                "name": "Project 1",
                "stack": "Python, React",
                "desc": ["Description 1", "Description 2"]
            },
            {
                "name": "Project 2", 
                "stack": "Node.js, MongoDB",
                "desc": ["Description 3"]
            }
        ]
    }
    
    # Simple template
    template = """
    <div>
        <h1>{{name}}</h1>
        <h2>Projects</h2>
        {{#each projects}}
        <div>
            <h3>{{name}} - {{stack}}</h3>
            <ul>
                {{#each desc}}
                <li>{{this}}</li>
                {{/each}}
            </ul>
        </div>
        {{/each}}
    </div>
    """
    
    # Render template
    engine = TemplateEngine()
    result = engine.render_template(template, test_data)
    
    print("📄 Template:")
    print(template)
    print("\n📊 Data:")
    print(test_data)
    print("\n🎨 Rendered:")
    print(result)
    
    # Check for remaining template syntax
    remaining = []
    lines = result.split('\n')
    for i, line in enumerate(lines):
        if '{{' in line and '}}' in line:
            remaining.append(f"Line {i+1}: {line.strip()}")
    
    if remaining:
        print(f"\n❌ Remaining template syntax: {remaining}")
    else:
        print("\n✅ Template syntax processed successfully!")

if __name__ == "__main__":
    test_simple_template()
