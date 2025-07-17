"""
Survey Automation Core Modules
Enhanced with stealth browser capabilities and brain intelligence.
"""

from .backup.stealth_browser_manager_backup import StealthBrowserManager

# Import existing browser manager for compatibility
try:
    from .browser_manager import BrowserManager
except ImportError:
    BrowserManager = None

__all__ = [
    'StealthBrowserManager'
]

if BrowserManager:
    __all__.append('BrowserManager')
