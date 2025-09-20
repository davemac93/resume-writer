"""
Simple template engine for rendering HTML templates with data
"""
import re
from typing import Dict, Any, List

class TemplateEngine:
    def __init__(self):
        self.template_cache = {}
    
    def render_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """
        Render template with data using simple template syntax
        
        Args:
            template_content: HTML template content
            data: Data dictionary to render
            
        Returns:
            Rendered HTML content
        """
        rendered = template_content
        
        # Handle simple variable substitution {{variable}}
        for key, value in data.items():
            if isinstance(value, str):
                rendered = rendered.replace(f'{{{{{key}}}}}', value)
            elif isinstance(value, (int, float)):
                rendered = rendered.replace(f'{{{{{key}}}}}', str(value))
            elif value is None:
                rendered = rendered.replace(f'{{{{{key}}}}}', '')
        
        # Handle loops {{#each array}}...{{/each}}
        rendered = self._process_loops(rendered, data)
        
        # Handle conditionals {{#if condition}}...{{/if}}
        rendered = self._process_conditionals(rendered, data)
        
        # Final cleanup - remove any remaining {{this}} or other template syntax
        rendered = self._cleanup_remaining_syntax(rendered, data)
        
        return rendered
    
    def _process_loops(self, content: str, data: Dict[str, Any]) -> str:
        """Process {{#each}} loops in template with support for nested loops"""
        # Process loops iteratively to handle nested loops
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            # Find all {{#each}} blocks
            loop_pattern = r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}'
            matches = re.findall(loop_pattern, content, re.DOTALL)
            
            if not matches:
                break  # No more loops to process
                
            for array_name, loop_content in matches:
                if array_name in data and isinstance(data[array_name], list):
                    array_data = data[array_name]
                    rendered_loops = []
                    
                    for item in array_data:
                        if isinstance(item, dict):
                            # Render the loop content for this item
                            item_content = loop_content
                            
                            # Process simple variable substitution first
                            for key, value in item.items():
                                if isinstance(value, str):
                                    item_content = item_content.replace(f'{{{{{key}}}}}', value)
                                elif isinstance(value, (int, float)):
                                    item_content = item_content.replace(f'{{{{{key}}}}}', str(value))
                                elif value is None:
                                    item_content = item_content.replace(f'{{{{{key}}}}}', '')
                                elif isinstance(value, list):
                                    # Handle list values for {{this}} replacement
                                    if '{{this}}' in item_content:
                                        # Find the specific {{#each}} block for this key
                                        this_pattern = r'\{\{#each\s+' + key + r'\}\}(.*?)\{\{/each\}\}'
                                        this_match = re.search(this_pattern, item_content, re.DOTALL)
                                        if this_match:
                                            this_content = this_match.group(1)
                                            rendered_this = []
                                            for list_item in value:
                                                if isinstance(list_item, str):
                                                    rendered_this.append(this_content.replace('{{this}}', list_item))
                                            # Replace the {{#each key}} block with rendered content
                                            item_content = re.sub(this_pattern, '\n'.join(rendered_this), item_content, flags=re.DOTALL)
                            
                            # Process nested loops after variable substitution
                            item_content = self._process_loops(item_content, item)
                            
                            rendered_loops.append(item_content)
                        elif isinstance(item, str):
                            # Handle simple string items (like tags)
                            item_content = loop_content.replace('{{this}}', item)
                            rendered_loops.append(item_content)
                    
                    # Replace the entire loop block with rendered content
                    full_loop_pattern = f'\\{{{{#each\\s+{array_name}\\}}}}(.*?)\\{{{{/each\\}}}}'
                    replacement = '\n'.join(rendered_loops) if rendered_loops else ''
                    content = re.sub(full_loop_pattern, replacement, content, flags=re.DOTALL)
                else:
                    # Remove the loop block if array doesn't exist or is empty
                    full_loop_pattern = f'\\{{{{#each\\s+{array_name}\\}}}}(.*?)\\{{{{/each\\}}}}'
                    content = re.sub(full_loop_pattern, '', content, flags=re.DOTALL)
            
            iteration += 1
        
        return content
    
    def _process_conditionals(self, content: str, data: Dict[str, Any]) -> str:
        """Process {{#if}} conditionals in template"""
        # Find all {{#if}} blocks
        if_pattern = r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}'
        matches = re.findall(if_pattern, content, re.DOTALL)
        
        for condition_name, if_content in matches:
            if condition_name in data and data[condition_name]:
                # Condition is true, keep the content
                full_if_pattern = f'\\{{{{#if\\s+{condition_name}\\}}}}(.*?)\\{{{{/if\\}}}}'
                content = re.sub(full_if_pattern, if_content, content, flags=re.DOTALL)
            else:
                # Condition is false, remove the content
                full_if_pattern = f'\\{{{{#if\\s+{condition_name}\\}}}}(.*?)\\{{{{/if\\}}}}'
                content = re.sub(full_if_pattern, '', content, flags=re.DOTALL)
        
        return content
    
    def _cleanup_remaining_syntax(self, content: str, data: Dict[str, Any]) -> str:
        """Clean up any remaining template syntax that wasn't processed"""
        # Remove any remaining {{this}} syntax
        content = re.sub(r'\{\{this\}\}', '', content)
        
        # Remove any remaining {{#each}} blocks that weren't processed
        content = re.sub(r'\{\{#each\s+\w+\}\}.*?\{\{/each\}\}', '', content, flags=re.DOTALL)
        
        # Remove any remaining {{#if}} blocks that weren't processed
        content = re.sub(r'\{\{#if\s+\w+\}\}.*?\{\{/if\}\}', '', content, flags=re.DOTALL)
        
        # Remove any remaining {{variable}} syntax
        content = re.sub(r'\{\{[^}]+\}\}', '', content)
        
        return content
    
    def load_template(self, template_path: str) -> str:
        """Load template from file"""
        if template_path in self.template_cache:
            return self.template_cache[template_path]
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            self.template_cache[template_path] = template_content
            return template_content
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {template_path}")
        except Exception as e:
            raise Exception(f"Error loading template: {e}")
    
    def render_template_file(self, template_path: str, data: Dict[str, Any]) -> str:
        """Load and render template from file"""
        template_content = self.load_template(template_path)
        return self.render_template(template_content, data)

# Global template engine instance
template_engine = TemplateEngine()
