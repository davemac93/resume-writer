"""
Simple template engine that handles nested loops correctly
"""
import re
from typing import Dict, Any, List

class SimpleTemplateEngine:
    def __init__(self):
        pass
    
    def render_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """Render template with data using simple template syntax"""
        rendered = template_content
        
        # Process loops first (including nested loops)
        rendered = self._process_loops(rendered, data)
        
        # Process conditionals
        rendered = self._process_conditionals(rendered, data)
        
        # Process simple variable substitution last
        rendered = self._process_variables(rendered, data)
        
        return rendered
    
    def _process_loops(self, content: str, data: Dict[str, Any]) -> str:
        """Process {{#each}} loops recursively"""
        # Find all {{#each}} blocks
        loop_pattern = r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}'
        matches = re.findall(loop_pattern, content, re.DOTALL)
        
        if not matches:
            return content
        
        for array_name, loop_content in matches:
            if array_name in data and isinstance(data[array_name], list):
                array_data = data[array_name]
                rendered_loops = []
                
                for item in array_data:
                    if isinstance(item, dict):
                        # Create a new data context for this item
                        item_data = {**data, **item}
                        # Recursively process the loop content
                        item_rendered = self._process_loops(loop_content, item_data)
                        rendered_loops.append(item_rendered)
                    elif isinstance(item, str):
                        # Handle simple string items
                        item_rendered = loop_content.replace('{{this}}', item)
                        rendered_loops.append(item_rendered)
                
                # Replace the loop block with rendered content
                full_loop_pattern = f'\\{{{{#each\\s+{array_name}\\}}}}(.*?)\\{{{{/each\\}}}}'
                replacement = '\n'.join(rendered_loops) if rendered_loops else ''
                content = re.sub(full_loop_pattern, replacement, content, flags=re.DOTALL)
            else:
                # Remove the loop block if array doesn't exist or is empty
                full_loop_pattern = f'\\{{{{#each\\s+{array_name}\\}}}}(.*?)\\{{{{/each\\}}}}'
                content = re.sub(full_loop_pattern, '', content, flags=re.DOTALL)
        
        return content
    
    def _process_conditionals(self, content: str, data: Dict[str, Any]) -> str:
        """Process {{#if}} conditionals"""
        if_pattern = r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}'
        matches = re.findall(if_pattern, content, re.DOTALL)
        
        for condition_name, if_content in matches:
            if condition_name in data and data[condition_name]:
                # Keep the content
                content = re.sub(f'\\{{{{#if\\s+{condition_name}\\}}}}(.*?)\\{{{{/if\\}}}}', r'\\1', content, flags=re.DOTALL)
            else:
                # Remove the content
                content = re.sub(f'\\{{{{#if\\s+{condition_name}\\}}}}(.*?)\\{{{{/if\\}}}}', '', content, flags=re.DOTALL)
        
        return content
    
    def _process_variables(self, content: str, data: Dict[str, Any]) -> str:
        """Process simple variable substitution {{variable}}"""
        for key, value in data.items():
            if isinstance(value, str):
                content = content.replace(f'{{{{{key}}}}}', value)
            elif isinstance(value, (int, float)):
                content = content.replace(f'{{{{{key}}}}}', str(value))
            elif value is None:
                content = content.replace(f'{{{{{key}}}}}', '')
        
        return content