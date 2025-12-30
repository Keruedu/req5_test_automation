"""
Configuration for OrangeHRM Automation Testing
Contains all constants and settings
"""

# ============================================
# APPLICATION SETTINGS
# ============================================

BASE_URL = "http://localhost"
ADMIN_USERNAME = "duongjane32"
ADMIN_PASSWORD = "OrangeHRM@111"

# ============================================
# BROWSER SETTINGS
# ============================================

# Supported browsers for cross-browser testing
BROWSERS = ["chrome", "firefox", "edge"]

# Default browser
DEFAULT_BROWSER = "chrome"

# Browser options
HEADLESS_MODE = False
WINDOW_SIZE = (1920, 1080)

# ============================================
# TIMEOUT SETTINGS
# ============================================

IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30

# ============================================
# REPORT SETTINGS
# ============================================

REPORT_DIR = "reports"
SCREENSHOT_DIR = "screenshots"
REPORT_TITLE = "OrangeHRM Automation Test Report"
TESTER_NAME = "Lê Hoàng Việt"
STUDENT_ID = "22120430"

# ============================================
# LOGGING SETTINGS
# ============================================

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
