"""
HTML to PDF generator using Playwright for better rendering quality
"""
import asyncio
import os
import tempfile
from typing import Optional
from playwright.async_api import async_playwright
import logging

class HTMLToPDFGenerator:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        
    async def initialize(self):
        """Initialize Playwright browser"""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            # Use Chromium for better PDF rendering
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1200, 'height': 800},
                device_scale_factor=1
            )
            logging.info("Playwright browser initialized")

    async def close(self):
        """Close Playwright browser with proper error handling"""
        try:
            if self.context:
                await asyncio.wait_for(self.context.close(), timeout=5.0)
                self.context = None
        except Exception as e:
            logging.warning(f"Error closing Playwright context: {e}")
        
        try:
            if self.browser:
                await asyncio.wait_for(self.browser.close(), timeout=5.0)
                self.browser = None
        except Exception as e:
            logging.warning(f"Error closing Playwright browser: {e}")
        
        try:
            if self.playwright:
                await asyncio.wait_for(self.playwright.stop(), timeout=5.0)
                self.playwright = None
        except Exception as e:
            logging.warning(f"Error stopping Playwright: {e}")
        
        logging.info("Playwright browser cleanup completed")

    async def generate_pdf_from_html(self, html_content: str, user_id: str, options: Optional[dict] = None) -> bytes:
        """
        Generate PDF from HTML content using Playwright
        
        Args:
            html_content: HTML content to convert
            user_id: User ID for filename
            options: Optional PDF generation options
            
        Returns:
            PDF bytes
        """
        await self.initialize()
        
        # Default PDF options
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
        
        # Merge with custom options
        if options:
            pdf_options.update(options)
        
        try:
            # Create a new page
            page = await self.context.new_page()
            
            # Set content and wait for it to load
            await page.set_content(html_content, wait_until='networkidle')
            
            # Wait a bit for any dynamic content to render
            await page.wait_for_timeout(1000)
            
            # Generate PDF
            pdf_bytes = await page.pdf(**pdf_options)
            
            # Close the page
            await page.close()
            
            logging.info(f"PDF generated successfully for user {user_id}")
            return pdf_bytes
            
        except Exception as e:
            logging.error(f"Error generating PDF with Playwright: {e}")
            raise e

    async def generate_pdf_from_url(self, url: str, user_id: str, options: Optional[dict] = None) -> bytes:
        """
        Generate PDF from URL using Playwright
        
        Args:
            url: URL to convert to PDF
            user_id: User ID for filename
            options: Optional PDF generation options
            
        Returns:
            PDF bytes
        """
        await self.initialize()
        
        # Default PDF options
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
        
        # Merge with custom options
        if options:
            pdf_options.update(options)
        
        try:
            # Create a new page
            page = await self.context.new_page()
            
            # Navigate to URL and wait for it to load
            await page.goto(url, wait_until='networkidle')
            
            # Wait a bit for any dynamic content to render
            await page.wait_for_timeout(2000)
            
            # Generate PDF
            pdf_bytes = await page.pdf(**pdf_options)
            
            # Close the page
            await page.close()
            
            logging.info(f"PDF generated successfully from URL {url} for user {user_id}")
            return pdf_bytes
            
        except Exception as e:
            logging.error(f"Error generating PDF from URL with Playwright: {e}")
            raise e

# Global instance
html_pdf_generator = HTMLToPDFGenerator()

async def cleanup_playwright():
    """Cleanup function to close Playwright browser with timeout"""
    try:
        await asyncio.wait_for(html_pdf_generator.close(), timeout=10.0)
        logging.info("Playwright cleanup completed successfully")
    except asyncio.TimeoutError:
        logging.warning("Playwright cleanup timed out, forcing shutdown")
    except Exception as e:
        logging.error(f"Error during Playwright cleanup: {e}")
