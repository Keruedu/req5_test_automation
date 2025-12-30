"""
Selenium Automation Tests for OrangeHRM
Requirement 5: Automation Testing

47 Test Cases based on Test_Design_Report.md Section 6.3
Using Black-Box Testing Techniques:
- Domain Testing: 18 cases
- Decision Table: 7 cases
- Use Case Testing: 4 cases
- State Transition: 8 cases
- All-Pair Testing: 6 cases
- Other: 4 cases
"""

import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    ElementClickInterceptedException
)

# Try to import webdriver_manager, fallback to manual driver
try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

# ============================================
# CONFIGURATION
# ============================================

BASE_URL = "http://localhost"
ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "admin123"
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================
# TEST CASE DEFINITIONS (47 Test Cases)
# ============================================

class TestStatus(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


@dataclass
class TestResult:
    test_id: str
    test_name: str
    status: TestStatus
    expected: str
    actual: str
    duration: float
    error_message: Optional[str] = None
    screenshot: Optional[str] = None


# All 47 Test Cases from Test_Design_Report.md Section 6.3
TEST_CASES = [
    # === LOCATIONS - Domain Testing (8 cases) ===
    {"id": "TC_LOC_D01", "module": "Locations", "technique": "Domain", 
     "name": "Add location - valid data", 
     "expected": "Success: Location 'HCM Office' created with all fields"},
    {"id": "TC_LOC_D02", "module": "Locations", "technique": "Domain",
     "name": "Add location - min name (1 char)",
     "expected": "Success: Location with name 'A' created"},
    {"id": "TC_LOC_D03", "module": "Locations", "technique": "Domain",
     "name": "Add location - max name (100 chars)",
     "expected": "Success: Location with 100-char name created"},
    {"id": "TC_LOC_D04", "module": "Locations", "technique": "Domain",
     "name": "Add location - empty name",
     "expected": "Error: 'Required' validation message displayed"},
    {"id": "TC_LOC_D05", "module": "Locations", "technique": "Domain",
     "name": "Add location - name > 100 chars",
     "expected": "Error: Input truncated or 'Maximum 100 characters' shown"},
    {"id": "TC_LOC_D06", "module": "Locations", "technique": "Domain",
     "name": "Add location - no country",
     "expected": "Error: 'Required' validation for Country field"},
    {"id": "TC_LOC_D07", "module": "Locations", "technique": "Domain",
     "name": "Add location - duplicate name",
     "expected": "Error: 'Already exists' message displayed"},
    {"id": "TC_LOC_D08", "module": "Locations", "technique": "Domain",
     "name": "Add location - invalid phone format",
     "expected": "Error: 'Invalid phone format' or accepted with warning"},
    
    # === JOB TITLES - Domain Testing (4 cases) ===
    {"id": "TC_JOB_D01", "module": "Job Titles", "technique": "Domain",
     "name": "Add job title - valid",
     "expected": "Success: 'Senior Developer' job title created"},
    {"id": "TC_JOB_D02", "module": "Job Titles", "technique": "Domain",
     "name": "Add job title - empty",
     "expected": "Error: 'Required' validation message"},
    {"id": "TC_JOB_D03", "module": "Job Titles", "technique": "Domain",
     "name": "Add job title - duplicate",
     "expected": "Error: 'Already exists' for existing 'Staff' title"},
    {"id": "TC_JOB_D04", "module": "Job Titles", "technique": "Domain",
     "name": "Add job title - description > 400 chars",
     "expected": "Error: 'Maximum 400 characters' message"},
    
    # === JOB TITLES - Use Case (1 case) ===
    {"id": "TC_JOB_UC01", "module": "Job Titles", "technique": "Use Case",
     "name": "Delete job title assigned to employee",
     "expected": "Error: 'Cannot delete - in use by employees'"},
    
    # === SKILLS - Domain Testing (2 cases) ===
    {"id": "TC_SKL_D01", "module": "Skills", "technique": "Domain",
     "name": "Add skill - valid",
     "expected": "Success: 'Python' skill created"},
    {"id": "TC_SKL_D02", "module": "Skills", "technique": "Domain",
     "name": "Add skill - duplicate",
     "expected": "Error: 'Already exists' message"},
    
    # === EDUCATION - Domain Testing (1 case) ===
    {"id": "TC_EDU_D01", "module": "Education", "technique": "Domain",
     "name": "Add education - valid",
     "expected": "Success: 'Bachelor Degree' added"},
    
    # === LANGUAGES - Domain Testing (1 case) ===
    {"id": "TC_LNG_D01", "module": "Languages", "technique": "Domain",
     "name": "Add language - special characters",
     "expected": "Success/Error: Handle 'Việt Nam' characters"},
    
    # === LICENSES - Domain Testing (1 case) ===
    {"id": "TC_LIC_D01", "module": "Licenses", "technique": "Domain",
     "name": "Add license - valid with expiry",
     "expected": "Success: License with date fields"},
    
    # === KPIs - Domain Testing (4 cases) ===
    {"id": "TC_KPI_D01", "module": "KPIs", "technique": "Domain",
     "name": "Add KPI - valid (min=0, max=100)",
     "expected": "Success: KPI 'Sales Target' created"},
    {"id": "TC_KPI_D02", "module": "KPIs", "technique": "Domain",
     "name": "Add KPI - min > max (invalid range)",
     "expected": "Error: 'Min rating cannot exceed Max rating'"},
    {"id": "TC_KPI_D03", "module": "KPIs", "technique": "Domain",
     "name": "Add KPI - min = max = 50 (boundary)",
     "expected": "Success: KPI with single-value range"},
    {"id": "TC_KPI_D04", "module": "KPIs", "technique": "Domain",
     "name": "Add KPI - negative min value",
     "expected": "Error: 'Must be positive number' or 'Invalid'"},
    
    # === KPIs - Decision Table (3 cases) ===
    {"id": "TC_KPI_DT01", "module": "KPIs", "technique": "Decision Table",
     "name": "KPI: Indicator + Job + ValidRange → OK",
     "expected": "Success: All conditions met"},
    {"id": "TC_KPI_DT02", "module": "KPIs", "technique": "Decision Table",
     "name": "KPI: NoIndicator → Error",
     "expected": "Error: 'Key Performance Indicator Required'"},
    {"id": "TC_KPI_DT03", "module": "KPIs", "technique": "Decision Table",
     "name": "KPI: NoJobTitle → Error",
     "expected": "Error: 'Job Title Required'"},
    
    # === REVIEWS - Decision Table (4 cases) ===
    {"id": "TC_REV_DT01", "module": "Reviews", "technique": "Decision Table",
     "name": "Review: Emp + Sup + ValidDates → OK",
     "expected": "Success: Review for 'John' created"},
    {"id": "TC_REV_DT02", "module": "Reviews", "technique": "Decision Table",
     "name": "Review: NoEmployee → Error",
     "expected": "Error: 'Employee Name Required'"},
    {"id": "TC_REV_DT03", "module": "Reviews", "technique": "Decision Table",
     "name": "Review: StartDate > EndDate → Error",
     "expected": "Error: 'To date should be after From date'"},
    {"id": "TC_REV_DT04", "module": "Reviews", "technique": "Decision Table",
     "name": "Review: Supervisor = Employee → Error",
     "expected": "Error: 'Supervisor cannot be same as Employee'"},
    
    # === TRACKERS - Use Case (2 cases) ===
    {"id": "TC_TRK_UC01", "module": "Trackers", "technique": "Use Case",
     "name": "View My Trackers - no trackers",
     "expected": "Display: 'No Records Found' message"},
    {"id": "TC_TRK_UC02", "module": "Trackers", "technique": "Use Case",
     "name": "Search Employee Trackers by name",
     "expected": "Display: Matching tracker records"},
    
    # === REVIEWS - State Transition (8 cases) ===
    {"id": "TC_ST_01", "module": "Reviews", "technique": "State Transition",
     "name": "Create Review → Inactive state",
     "expected": "Status changes to 'Inactive', not visible to employee"},
    {"id": "TC_ST_02", "module": "Reviews", "technique": "State Transition",
     "name": "Activate Review → Activated state",
     "expected": "Status 'Activated', employee receives notification"},
    {"id": "TC_ST_03", "module": "Reviews", "technique": "State Transition",
     "name": "Employee Self-Evaluation → In Progress",
     "expected": "Status 'In Progress', progress bar updated"},
    {"id": "TC_ST_04", "module": "Reviews", "technique": "State Transition",
     "name": "Complete All Evaluations → Completed",
     "expected": "Status 'Completed', final rating calculated"},
    {"id": "TC_ST_05", "module": "Reviews", "technique": "State Transition",
     "name": "Delete Draft Review → Deleted",
     "expected": "Review removed from list, confirmation shown"},
    {"id": "TC_ST_06", "module": "Reviews", "technique": "State Transition",
     "name": "Try update Completed review → Error",
     "expected": "Error: 'Cannot modify completed review'"},
    {"id": "TC_ST_07", "module": "Reviews", "technique": "State Transition",
     "name": "Try complete without evaluation → Error",
     "expected": "Error: 'Self evaluation not submitted'"},
    {"id": "TC_ST_08", "module": "Reviews", "technique": "State Transition",
     "name": "Try delete In Progress review → Error",
     "expected": "Error: 'Cannot delete - review in progress'"},
    
    # === SEARCH - All-Pair Testing (6 cases) ===
    {"id": "TC_AP_01", "module": "Search", "technique": "All-Pair",
     "name": "Locations + Valid + All + Asc",
     "expected": "Results sorted A-Z, all statuses shown"},
    {"id": "TC_AP_02", "module": "Search", "technique": "All-Pair",
     "name": "Job Titles + Empty + Active + Desc",
     "expected": "All active titles, sorted Z-A"},
    {"id": "TC_AP_03", "module": "Search", "technique": "All-Pair",
     "name": "Skills + Special Chars (@#$) + All",
     "expected": "'No Records Found' or escaped display"},
    {"id": "TC_AP_04", "module": "Search", "technique": "All-Pair",
     "name": "KPIs + No Match (XYZ) + Active",
     "expected": "'No Records Found' message"},
    {"id": "TC_AP_05", "module": "Search", "technique": "All-Pair",
     "name": "Locations + Apostrophe (Test's)",
     "expected": "Handles SQL injection-like input safely"},
    {"id": "TC_AP_06", "module": "Search", "technique": "All-Pair",
     "name": "Job Titles + Valid (Dev) + All + Asc",
     "expected": "'Developer', 'DevOps' etc. displayed"},
    
    # === LOCATIONS - Use Case (2 cases) ===
    {"id": "TC_LOC_UC01", "module": "Locations", "technique": "Use Case",
     "name": "Delete location in use by employee",
     "expected": "Error: 'Location assigned to 5 employees'"},
    {"id": "TC_LOC_UC02", "module": "Locations", "technique": "Use Case",
     "name": "Search location - partial match",
     "expected": "'HCM' returns 'HCM Office', 'HCM Branch'"},
]


# ============================================
# SELENIUM TEST AUTOMATION CLASS
# ============================================

class OrangeHRMAutomation:
    """Selenium automation for OrangeHRM testing"""
    
    def __init__(self, base_url: str = BASE_URL, headless: bool = False):
        self.base_url = base_url
        self.headless = headless
        self.driver = None
        self.results: List[TestResult] = []
        self.start_time = None
        
    def setup(self) -> bool:
        """Initialize WebDriver"""
        try:
            options = Options()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            
            if USE_WEBDRIVER_MANAGER:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                self.driver = webdriver.Chrome(options=options)
            
            self.driver.implicitly_wait(IMPLICIT_WAIT)
            logger.info("✓ WebDriver initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to initialize WebDriver: {e}")
            return False
    
    def teardown(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("✓ WebDriver closed")
    
    def login(self, username: str = ADMIN_USERNAME, password: str = ADMIN_PASSWORD) -> bool:
        """Login to OrangeHRM"""
        try:
            self.driver.get(self.base_url)
            time.sleep(2)
            
            # Wait for login form
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            # Fill credentials
            self.driver.find_element(By.NAME, "username").send_keys(username)
            self.driver.find_element(By.NAME, "password").send_keys(password)
            
            # Click login button
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            
            # Wait for dashboard
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-sidepanel"))
            )
            
            logger.info("✓ Logged in successfully")
            return True
            
        except Exception as e:
            logger.error(f"✗ Login failed: {e}")
            return False
    
    # ============================================
    # NAVIGATION HELPERS
    # ============================================
    
    def navigate_to_menu(self, menu_name: str) -> bool:
        """Click on left sidebar menu"""
        try:
            menu_items = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-main-menu-item")
            for item in menu_items:
                if menu_name.lower() in item.text.lower():
                    item.click()
                    time.sleep(1)
                    return True
            return False
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return False
    
    def navigate_to_topbar(self, menu_text: str) -> bool:
        """Click on topbar menu item"""
        try:
            topbar_items = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-topbar-body-nav-tab")
            for item in topbar_items:
                if menu_text.lower() in item.text.lower():
                    item.click()
                    time.sleep(1)
                    return True
            return False
        except Exception as e:
            logger.error(f"Topbar navigation error: {e}")
            return False
    
    def navigate_to_submenu(self, submenu_text: str) -> bool:
        """Click on submenu item from dropdown"""
        try:
            time.sleep(0.5)
            submenu_items = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-dropdown-menu a")
            for item in submenu_items:
                if submenu_text.lower() in item.text.lower():
                    item.click()
                    time.sleep(1)
                    return True
            return False
        except Exception as e:
            logger.error(f"Submenu navigation error: {e}")
            return False
    
    def navigate_to(self, main_menu: str, topbar_menu: str = None, submenu: str = None) -> bool:
        """Full navigation path"""
        try:
            self.navigate_to_menu(main_menu)
            time.sleep(1)
            
            if topbar_menu:
                self.navigate_to_topbar(topbar_menu)
                time.sleep(0.5)
                
                if submenu:
                    self.navigate_to_submenu(submenu)
            
            time.sleep(1)
            return True
        except Exception as e:
            logger.error(f"Full navigation error: {e}")
            return False
    
    # ============================================
    # ACTION HELPERS
    # ============================================
    
    def click_add_button(self) -> bool:
        """Click Add button"""
        try:
            add_btn = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.oxd-button--secondary"))
            )
            add_btn.click()
            time.sleep(1)
            return True
        except Exception as e:
            logger.error(f"Add button error: {e}")
            return False
    
    def click_save_button(self) -> bool:
        """Click Save button"""
        try:
            save_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            save_btn.click()
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Save button error: {e}")
            return False
    
    def fill_input(self, label_text: str, value: str, clear: bool = True) -> bool:
        """Fill input field by label"""
        try:
            # Find all form groups
            form_groups = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-input-group")
            for group in form_groups:
                if label_text.lower() in group.text.lower():
                    input_field = group.find_element(By.CSS_SELECTOR, "input.oxd-input")
                    if clear:
                        input_field.clear()
                    input_field.send_keys(value)
                    return True
            return False
        except Exception as e:
            logger.error(f"Fill input error: {e}")
            return False
    
    def select_dropdown(self, label_text: str, option_text: str) -> bool:
        """Select dropdown option"""
        try:
            form_groups = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-input-group")
            for group in form_groups:
                if label_text.lower() in group.text.lower():
                    dropdown = group.find_element(By.CSS_SELECTOR, ".oxd-select-text")
                    dropdown.click()
                    time.sleep(0.5)
                    
                    options = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-select-option")
                    for option in options:
                        if option_text.lower() in option.text.lower():
                            option.click()
                            return True
            return False
        except Exception as e:
            logger.error(f"Dropdown error: {e}")
            return False
    
    def check_success_toast(self) -> bool:
        """Check if success toast appears"""
        try:
            toast = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-toast--success"))
            )
            return True
        except:
            return False
    
    def check_error_message(self) -> Tuple[bool, str]:
        """Check if error message appears"""
        try:
            # Check for inline validation errors
            errors = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-input-field-error-message")
            if errors:
                return True, errors[0].text
            
            # Check for toast error
            toast = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-toast--error")
            if toast:
                return True, toast[0].text
            
            return False, ""
        except:
            return False, ""
    
    def take_screenshot(self, name: str) -> str:
        """Take screenshot and save"""
        try:
            filename = f"screenshots/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(filename)
            return filename
        except:
            return ""
    
    # ============================================
    # TEST IMPLEMENTATIONS
    # ============================================
    
    def run_test(self, test_case: dict) -> TestResult:
        """Run a single test case"""
        test_id = test_case["id"]
        start = time.time()
        
        logger.info(f"Running {test_id}: {test_case['name']}")
        
        try:
            # Get the test function
            test_func = getattr(self, f"test_{test_id.lower()}", None)
            
            if test_func:
                actual_result, passed = test_func()
            else:
                # If no specific implementation, mark as skipped
                actual_result = "No implementation"
                passed = None  # Skipped
            
            duration = time.time() - start
            
            if passed is None:
                status = TestStatus.SKIPPED
            elif passed:
                status = TestStatus.PASSED
            else:
                status = TestStatus.FAILED
            
            return TestResult(
                test_id=test_id,
                test_name=test_case["name"],
                status=status,
                expected=test_case["expected"],
                actual=actual_result,
                duration=duration
            )
            
        except Exception as e:
            duration = time.time() - start
            return TestResult(
                test_id=test_id,
                test_name=test_case["name"],
                status=TestStatus.ERROR,
                expected=test_case["expected"],
                actual=str(e),
                duration=duration,
                error_message=str(e)
            )
    
    # === LOCATION TEST IMPLEMENTATIONS ===
    
    def test_tc_loc_d01(self) -> Tuple[str, bool]:
        """Add location - valid data"""
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add_button()
        
        self.fill_input("Name", "HCM Office Test")
        self.select_dropdown("Country", "Viet Nam")
        self.fill_input("City", "Ho Chi Minh")
        self.fill_input("Phone", "+84-28-1234567")
        
        self.click_save_button()
        
        if self.check_success_toast():
            return "Success: Location created", True
        else:
            has_error, msg = self.check_error_message()
            return f"Failed: {msg}", False
    
    def test_tc_loc_d02(self) -> Tuple[str, bool]:
        """Add location - min name (1 char)"""
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add_button()
        
        self.fill_input("Name", "A")
        self.select_dropdown("Country", "Viet Nam")
        
        self.click_save_button()
        
        if self.check_success_toast():
            return "Success: Location 'A' created", True
        else:
            has_error, msg = self.check_error_message()
            return f"Failed: {msg}", False
    
    def test_tc_loc_d03(self) -> Tuple[str, bool]:
        """Add location - max name (100 chars)"""
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add_button()
        
        long_name = "A" * 100
        self.fill_input("Name", long_name)
        self.select_dropdown("Country", "Viet Nam")
        
        self.click_save_button()
        
        if self.check_success_toast():
            return "Success: Location with 100-char name created", True
        else:
            has_error, msg = self.check_error_message()
            return f"Failed: {msg}", False
    
    def test_tc_loc_d04(self) -> Tuple[str, bool]:
        """Add location - empty name"""
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add_button()
        
        self.fill_input("Name", "")
        self.select_dropdown("Country", "Viet Nam")
        
        self.click_save_button()
        
        has_error, msg = self.check_error_message()
        if has_error and "required" in msg.lower():
            return f"Error: {msg}", True
        else:
            return "No validation error shown", False
    
    def test_tc_loc_d05(self) -> Tuple[str, bool]:
        """Add location - name > 100 chars"""
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add_button()
        
        long_name = "A" * 101
        self.fill_input("Name", long_name)
        self.select_dropdown("Country", "Viet Nam")
        
        self.click_save_button()
        
        has_error, msg = self.check_error_message()
        if has_error:
            return f"Error: {msg}", True
        elif self.check_success_toast():
            return "Input was truncated and accepted", True
        else:
            return "Unexpected behavior", False
    
    def test_tc_loc_d06(self) -> Tuple[str, bool]:
        """Add location - no country"""
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add_button()
        
        self.fill_input("Name", "Test Office")
        # Don't select country
        
        self.click_save_button()
        
        has_error, msg = self.check_error_message()
        if has_error and "required" in msg.lower():
            return f"Error: {msg}", True
        else:
            return "No validation error shown", False
    
    def test_tc_loc_d07(self) -> Tuple[str, bool]:
        """Add location - duplicate name"""
        # First, create a location
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add_button()
        
        self.fill_input("Name", "Duplicate Test Office")
        self.select_dropdown("Country", "Viet Nam")
        self.click_save_button()
        time.sleep(2)
        
        # Now try to create same name
        self.click_add_button()
        self.fill_input("Name", "Duplicate Test Office")
        self.select_dropdown("Country", "Viet Nam")
        self.click_save_button()
        
        has_error, msg = self.check_error_message()
        if has_error and "exists" in msg.lower():
            return f"Error: {msg}", True
        elif self.check_success_toast():
            return "Duplicate allowed (unexpected)", False
        else:
            return f"Result: {msg}", False
    
    def test_tc_loc_d08(self) -> Tuple[str, bool]:
        """Add location - invalid phone format"""
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add_button()
        
        self.fill_input("Name", "Phone Test Office")
        self.select_dropdown("Country", "Viet Nam")
        self.fill_input("Phone", "abc@#$invalid")
        
        self.click_save_button()
        
        has_error, msg = self.check_error_message()
        if has_error:
            return f"Error: {msg}", True
        elif self.check_success_toast():
            return "Invalid phone accepted (may need review)", True
        else:
            return "Unexpected behavior", False
    
    # === JOB TITLES TEST IMPLEMENTATIONS ===
    
    def test_tc_job_d01(self) -> Tuple[str, bool]:
        """Add job title - valid"""
        self.navigate_to("Admin", "Job", "Job Titles")
        self.click_add_button()
        
        self.fill_input("Title", f"Senior Developer {datetime.now().strftime('%H%M%S')}")
        
        self.click_save_button()
        
        if self.check_success_toast():
            return "Success: Job title created", True
        else:
            has_error, msg = self.check_error_message()
            return f"Failed: {msg}", False
    
    def test_tc_job_d02(self) -> Tuple[str, bool]:
        """Add job title - empty"""
        self.navigate_to("Admin", "Job", "Job Titles")
        self.click_add_button()
        
        self.fill_input("Title", "")
        
        self.click_save_button()
        
        has_error, msg = self.check_error_message()
        if has_error and "required" in msg.lower():
            return f"Error: {msg}", True
        else:
            return "No validation error shown", False
    
    # === KPI TEST IMPLEMENTATIONS ===
    
    def test_tc_kpi_d01(self) -> Tuple[str, bool]:
        """Add KPI - valid (min=0, max=100)"""
        self.navigate_to("Performance", "Configure", "KPIs")
        self.click_add_button()
        
        self.fill_input("Key Performance Indicator", "Sales Target Test")
        self.select_dropdown("Job Title", "")  # Select first available
        self.fill_input("Minimum Rating", "0")
        self.fill_input("Maximum Rating", "100")
        
        self.click_save_button()
        
        if self.check_success_toast():
            return "Success: KPI created", True
        else:
            has_error, msg = self.check_error_message()
            return f"Failed: {msg}", False
    
    def test_tc_kpi_d02(self) -> Tuple[str, bool]:
        """Add KPI - min > max (invalid range)"""
        self.navigate_to("Performance", "Configure", "KPIs")
        self.click_add_button()
        
        self.fill_input("Key Performance Indicator", "Invalid Range KPI")
        self.select_dropdown("Job Title", "")
        self.fill_input("Minimum Rating", "80")
        self.fill_input("Maximum Rating", "50")
        
        self.click_save_button()
        
        has_error, msg = self.check_error_message()
        if has_error:
            return f"Error: {msg}", True
        else:
            return "No validation for invalid range", False
    
    def test_tc_kpi_d03(self) -> Tuple[str, bool]:
        """Add KPI - min = max = 50 (boundary)"""
        self.navigate_to("Performance", "Configure", "KPIs")
        self.click_add_button()
        
        self.fill_input("Key Performance Indicator", "Equal Range KPI")
        self.select_dropdown("Job Title", "")
        self.fill_input("Minimum Rating", "50")
        self.fill_input("Maximum Rating", "50")
        
        self.click_save_button()
        
        if self.check_success_toast():
            return "Success: KPI with equal min/max created", True
        else:
            has_error, msg = self.check_error_message()
            return f"Failed: {msg}", False
    
    def test_tc_kpi_d04(self) -> Tuple[str, bool]:
        """Add KPI - negative min value"""
        self.navigate_to("Performance", "Configure", "KPIs")
        self.click_add_button()
        
        self.fill_input("Key Performance Indicator", "Negative KPI")
        self.select_dropdown("Job Title", "")
        self.fill_input("Minimum Rating", "-10")
        self.fill_input("Maximum Rating", "100")
        
        self.click_save_button()
        
        has_error, msg = self.check_error_message()
        if has_error:
            return f"Error: {msg}", True
        else:
            return "Negative value accepted (may need review)", False
    
    # === SKILLS TEST IMPLEMENTATIONS ===
    
    def test_tc_skl_d01(self) -> Tuple[str, bool]:
        """Add skill - valid"""
        self.navigate_to("Admin", "Qualifications", "Skills")
        self.click_add_button()
        
        self.fill_input("Name", f"Python {datetime.now().strftime('%H%M%S')}")
        
        self.click_save_button()
        
        if self.check_success_toast():
            return "Success: Skill created", True
        else:
            has_error, msg = self.check_error_message()
            return f"Failed: {msg}", False
    
    def test_tc_skl_d02(self) -> Tuple[str, bool]:
        """Add skill - duplicate"""
        self.navigate_to("Admin", "Qualifications", "Skills")
        
        # First create
        self.click_add_button()
        skill_name = f"DuplicateSkill{datetime.now().strftime('%H%M%S')}"
        self.fill_input("Name", skill_name)
        self.click_save_button()
        time.sleep(2)
        
        # Try duplicate
        self.click_add_button()
        self.fill_input("Name", skill_name)
        self.click_save_button()
        
        has_error, msg = self.check_error_message()
        if has_error and "exists" in msg.lower():
            return f"Error: {msg}", True
        else:
            return "Duplicate allowed", False
    
    # ============================================
    # TEST RUNNER
    # ============================================
    
    def run_all_tests(self) -> List[TestResult]:
        """Run all 47 test cases"""
        self.start_time = datetime.now()
        self.results = []
        
        logger.info("=" * 60)
        logger.info("STARTING AUTOMATION TESTS - 47 Test Cases")
        logger.info("=" * 60)
        
        if not self.setup():
            logger.error("Failed to setup WebDriver")
            return []
        
        if not self.login():
            logger.error("Failed to login")
            self.teardown()
            return []
        
        for test_case in TEST_CASES:
            result = self.run_test(test_case)
            self.results.append(result)
            
            status_icon = "✓" if result.status == TestStatus.PASSED else "✗" if result.status == TestStatus.FAILED else "⊘"
            logger.info(f"  {status_icon} {result.test_id}: {result.status.value} ({result.duration:.2f}s)")
        
        self.teardown()
        
        # Summary
        passed = sum(1 for r in self.results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in self.results if r.status == TestStatus.SKIPPED)
        errors = sum(1 for r in self.results if r.status == TestStatus.ERROR)
        
        logger.info("=" * 60)
        logger.info("TEST RESULTS SUMMARY")
        logger.info(f"  Total: {len(self.results)}")
        logger.info(f"  Passed: {passed}")
        logger.info(f"  Failed: {failed}")
        logger.info(f"  Skipped: {skipped}")
        logger.info(f"  Errors: {errors}")
        logger.info(f"  Pass Rate: {(passed/len(self.results))*100:.1f}%")
        logger.info("=" * 60)
        
        return self.results
    
    def get_results_summary(self) -> dict:
        """Get summary of test results"""
        passed = sum(1 for r in self.results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in self.results if r.status == TestStatus.SKIPPED)
        errors = sum(1 for r in self.results if r.status == TestStatus.ERROR)
        
        return {
            "total": len(self.results),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "errors": errors,
            "pass_rate": (passed / len(self.results) * 100) if self.results else 0,
            "start_time": self.start_time,
            "results": self.results
        }


# ============================================
# MAIN ENTRY POINT
# ============================================

def main():
    """Main function to run tests"""
    print("=" * 60)
    print("OrangeHRM Automation Testing")
    print("47 Test Cases - Based on Test_Design_Report.md")
    print("=" * 60)
    
    # Create tester instance
    tester = OrangeHRMAutomation(base_url=BASE_URL, headless=False)
    
    # Run all tests
    results = tester.run_all_tests()
    
    # Get summary
    summary = tester.get_results_summary()
    
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {summary['total']}")
    print(f"Passed: {summary['passed']} ({summary['pass_rate']:.1f}%)")
    print(f"Failed: {summary['failed']}")
    print(f"Skipped: {summary['skipped']}")
    print(f"Errors: {summary['errors']}")
    print("=" * 60)
    
    return summary


if __name__ == "__main__":
    main()
