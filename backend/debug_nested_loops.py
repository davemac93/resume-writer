#!/usr/bin/env python3
"""
Debug nested loops in template engine
"""
from template_engine import TemplateEngine

def test_nested_loops():
    print("🔍 Testing nested loops...")
    
    # Test data with nested lists
    test_data = {
        "projects": [
            {
                "name": "Project 1",
                "desc": ["Description 1", "Description 2"]
            }
        ]
    }
    
    # Simple template with nested loop
    template = """
    {{#each projects}}
    <div>
        <h3>{{name}}</h3>
        <ul>
            {{#each desc}}
            <li>{{this}}</li>
            {{/each}}
        </ul>
    </div>
    {{/each}}
    """
    
    print("📄 Template:")
    print(template)
    print("\n📊 Data:")
    print(test_data)
    
    # Render template
    engine = TemplateEngine()
    result = engine.render_template(template, test_data)
    
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
    test_nested_loops()
