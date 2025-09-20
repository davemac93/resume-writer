#!/usr/bin/env python3
"""
Script to install Playwright browsers
"""
import subprocess
import sys
import os

def install_playwright_browsers():
    """Install Playwright browsers"""
    print("🎭 Installing Playwright browsers...")
    
    try:
        # Install Playwright browsers
        result = subprocess.run([
            sys.executable, "-m", "playwright", "install", "chromium"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Playwright Chromium browser installed successfully")
        print(result.stdout)
        
        # Also install system dependencies if on Linux
        if os.name == 'posix' and sys.platform != 'darwin':
            print("🔧 Installing system dependencies...")
            subprocess.run([
                sys.executable, "-m", "playwright", "install-deps"
            ], check=True)
            print("✅ System dependencies installed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Playwright browsers: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = install_playwright_browsers()
    if success:
        print("\n🎉 Playwright setup completed successfully!")
        print("You can now use HTML-to-PDF generation with Playwright.")
    else:
        print("\n❌ Playwright setup failed. Please check the error messages above.")
        sys.exit(1)
