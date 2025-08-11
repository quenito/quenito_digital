"""
🔍 Check Playwright Installation
Verify Playwright and browsers are properly installed
"""

import subprocess
import sys
import os
from pathlib import Path

def check_playwright():
    print("🔍 Playwright Installation Check")
    print("="*50)
    
    # 1. Check if playwright is installed
    print("\n1️⃣ Checking Playwright package...")
    try:
        import playwright
        # Get version from package metadata
        try:
            import pkg_resources
            version = pkg_resources.get_distribution("playwright").version
            print(f"✅ Playwright version: {version}")
        except:
            print("✅ Playwright is installed (version check failed but that's OK)")
    except ImportError:
        print("❌ Playwright not installed!")
        print("   Run: pip install playwright")
        return False
    
    # 2. Check browser installations
    print("\n2️⃣ Checking browser installations...")
    
    # Find browser path
    home = Path.home()
    browser_paths = [
        home / ".cache/ms-playwright",  # Linux
        home / "Library/Caches/ms-playwright",  # macOS
        home / "AppData/Local/ms-playwright",  # Windows
    ]
    
    browser_path = None
    for path in browser_paths:
        if path.exists():
            browser_path = path
            break
    
    if browser_path:
        print(f"📁 Browser directory: {browser_path}")
        
        # Check what's installed
        browsers = ["chromium", "firefox", "webkit"]
        installed = []
        
        for browser in browsers:
            browser_dirs = list(browser_path.glob(f"{browser}*"))
            if browser_dirs:
                installed.append(browser)
                for dir in browser_dirs:
                    size = sum(f.stat().st_size for f in dir.rglob('*') if f.is_file()) / (1024**2)
                    print(f"   ✅ {browser}: {dir.name} ({size:.1f} MB)")
        
        if not installed:
            print("   ❌ No browsers found!")
            return False
            
    else:
        print("❌ Playwright browser directory not found!")
        return False
    
    # 3. Test browser launch
    print("\n3️⃣ Testing browser launch...")
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://example.com")
            title = page.title()
            browser.close()
            
            print(f"✅ Browser test successful! Loaded page: {title}")
            return True
            
    except Exception as e:
        print(f"❌ Browser launch failed: {e}")
        return False

def install_playwright_browsers():
    """Install or reinstall Playwright browsers"""
    print("\n🔧 Installing Playwright browsers...")
    print("This will download ~300MB of browser files\n")
    
    try:
        # Run playwright install
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Browsers installed successfully!")
            print(result.stdout)
            return True
        else:
            print("❌ Installation failed!")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running installation: {e}")
        return False

def main():
    # Check installation
    if check_playwright():
        print("\n✅ Playwright is properly installed and working!")
    else:
        print("\n❌ Playwright installation issues detected")
        
        response = input("\nWould you like to (re)install Playwright browsers? (y/n): ")
        if response.lower() == 'y':
            if install_playwright_browsers():
                print("\n🎉 Installation complete! Try your script again.")
            else:
                print("\n😕 Installation failed. Try manually:")
                print("   playwright install chromium")
                print("   or")
                print("   python -m playwright install chromium")

if __name__ == "__main__":
    main()