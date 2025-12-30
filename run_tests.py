"""
Main Test Runner for OrangeHRM Automation Testing
Requirement 5: Automation Testing

Features:
- Multi-browser support (Chrome, Firefox, Edge)
- Data-driven testing from JSON
- HTML report generation
- Screenshot capture on failure
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import (
    BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD,
    BROWSERS, EXPLICIT_WAIT, SCREENSHOT_DIR
)
from browser_factory import BrowserFactory
from report_generator import ReportGenerator, TestResult, TestStatus

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================
# TEST CASE DEFINITIONS (47 Test Cases)
# ============================================

TEST_CASES = [
    # === LOCATIONS - Domain Testing (8 cases) ===
    {"id": "TC_LOC_D01", "module": "Locations", "technique": "Domain", 
     "name": "Add location - valid data", 
     "expected": "Success: Location created"},
    {"id": "TC_LOC_D02", "module": "Locations", "technique": "Domain",
     "name": "Add location - min name (1 char)",
     "expected": "Success: Location with name 'A' created"},
    {"id": "TC_LOC_D03", "module": "Locations", "technique": "Domain",
     "name": "Add location - max name (100 chars)",
     "expected": "Success: Location with 100-char name created"},
    {"id": "TC_LOC_D04", "module": "Locations", "technique": "Domain",
     "name": "Add location - empty name",
     "expected": "Error: 'Required' validation message"},
    {"id": "TC_LOC_D05", "module": "Locations", "technique": "Domain",
     "name": "Add location - name > 100 chars",
     "expected": "Error: Input truncated or 'Maximum 100 characters'"},
    {"id": "TC_LOC_D06", "module": "Locations", "technique": "Domain",
     "name": "Add location - no country",
     "expected": "Error: 'Required' validation for Country"},
    {"id": "TC_LOC_D07", "module": "Locations", "technique": "Domain",
     "name": "Add location - duplicate name",
     "expected": "Error: 'Already exists' message"},
    {"id": "TC_LOC_D08", "module": "Locations", "technique": "Domain",
     "name": "Add location - invalid phone",
     "expected": "Error: 'Invalid phone format'"},
    
    # === JOB TITLES (5 cases) ===
    {"id": "TC_JOB_D01", "module": "Job Titles", "technique": "Domain",
     "name": "Add job title - valid", "expected": "Success: Job title created"},
    {"id": "TC_JOB_D02", "module": "Job Titles", "technique": "Domain",
     "name": "Add job title - empty", "expected": "Error: 'Required' message"},
    {"id": "TC_JOB_D03", "module": "Job Titles", "technique": "Domain",
     "name": "Add job title - duplicate", "expected": "Error: 'Already exists'"},
    {"id": "TC_JOB_D04", "module": "Job Titles", "technique": "Domain",
     "name": "Add job title - description > 400", "expected": "Error: 'Maximum 400 characters'"},
    {"id": "TC_JOB_UC01", "module": "Job Titles", "technique": "Use Case",
     "name": "Delete job title in use", "expected": "Error: 'Cannot delete'"},
    
    # === SKILLS (2 cases) ===
    {"id": "TC_SKL_D01", "module": "Skills", "technique": "Domain",
     "name": "Add skill - valid", "expected": "Success: Skill created"},
    {"id": "TC_SKL_D02", "module": "Skills", "technique": "Domain",
     "name": "Add skill - duplicate", "expected": "Error: 'Already exists'"},
    
    # === EDUCATION, LANGUAGES, LICENSES (3 cases) ===
    {"id": "TC_EDU_D01", "module": "Education", "technique": "Domain",
     "name": "Add education - valid", "expected": "Success: Education added"},
    {"id": "TC_LNG_D01", "module": "Languages", "technique": "Domain",
     "name": "Add language - special chars", "expected": "Success/Error: Handle special chars"},
    {"id": "TC_LIC_D01", "module": "Licenses", "technique": "Domain",
     "name": "Add license - valid", "expected": "Success: License created"},
    
    # === KPIs - Domain & Decision Table (7 cases) ===
    {"id": "TC_KPI_D01", "module": "KPIs", "technique": "Domain",
     "name": "Add KPI - valid (min=0, max=100)", "expected": "Success: KPI created"},
    {"id": "TC_KPI_D02", "module": "KPIs", "technique": "Domain",
     "name": "Add KPI - min > max", "expected": "Error: 'Min cannot exceed Max'"},
    {"id": "TC_KPI_D03", "module": "KPIs", "technique": "Domain",
     "name": "Add KPI - min = max = 50", "expected": "Success: KPI with equal range"},
    {"id": "TC_KPI_D04", "module": "KPIs", "technique": "Domain",
     "name": "Add KPI - negative min", "expected": "Error: 'Must be positive'"},
    {"id": "TC_KPI_DT01", "module": "KPIs", "technique": "Decision Table",
     "name": "KPI: All valid → OK", "expected": "Success: KPI created"},
    {"id": "TC_KPI_DT02", "module": "KPIs", "technique": "Decision Table",
     "name": "KPI: NoIndicator → Error", "expected": "Error: 'Indicator Required'"},
    {"id": "TC_KPI_DT03", "module": "KPIs", "technique": "Decision Table",
     "name": "KPI: NoJobTitle → Error", "expected": "Error: 'Job Title Required'"},
    
    # === REVIEWS - Decision Table (4 cases) ===
    {"id": "TC_REV_DT01", "module": "Reviews", "technique": "Decision Table",
     "name": "Review: All valid → OK", "expected": "Success: Review created"},
    {"id": "TC_REV_DT02", "module": "Reviews", "technique": "Decision Table",
     "name": "Review: NoEmployee → Error", "expected": "Error: 'Employee Required'"},
    {"id": "TC_REV_DT03", "module": "Reviews", "technique": "Decision Table",
     "name": "Review: StartDate > EndDate", "expected": "Error: 'Invalid dates'"},
    {"id": "TC_REV_DT04", "module": "Reviews", "technique": "Decision Table",
     "name": "Review: Supervisor = Employee", "expected": "Error: 'Cannot be same'"},
    
    # === TRACKERS - Use Case (2 cases) ===
    {"id": "TC_TRK_UC01", "module": "Trackers", "technique": "Use Case",
     "name": "View My Trackers - empty", "expected": "Display: 'No Records Found'"},
    {"id": "TC_TRK_UC02", "module": "Trackers", "technique": "Use Case",
     "name": "Search Trackers by name", "expected": "Display: Matching records"},
    
    # === REVIEWS - State Transition (8 cases) ===
    {"id": "TC_ST_01", "module": "Reviews", "technique": "State Transition",
     "name": "Create Review → Inactive", "expected": "Status: 'Inactive'"},
    {"id": "TC_ST_02", "module": "Reviews", "technique": "State Transition",
     "name": "Activate Review", "expected": "Status: 'Activated'"},
    {"id": "TC_ST_03", "module": "Reviews", "technique": "State Transition",
     "name": "Self-Evaluation → In Progress", "expected": "Status: 'In Progress'"},
    {"id": "TC_ST_04", "module": "Reviews", "technique": "State Transition",
     "name": "Complete All → Completed", "expected": "Status: 'Completed'"},
    {"id": "TC_ST_05", "module": "Reviews", "technique": "State Transition",
     "name": "Delete Draft Review", "expected": "Review removed"},
    {"id": "TC_ST_06", "module": "Reviews", "technique": "State Transition",
     "name": "Update Completed → Error", "expected": "Error: 'Cannot modify'"},
    {"id": "TC_ST_07", "module": "Reviews", "technique": "State Transition",
     "name": "Complete without eval → Error", "expected": "Error: 'Not submitted'"},
    {"id": "TC_ST_08", "module": "Reviews", "technique": "State Transition",
     "name": "Delete In Progress → Error", "expected": "Error: 'Cannot delete'"},
    
    # === SEARCH - All-Pair (6 cases) ===
    {"id": "TC_AP_01", "module": "Search", "technique": "All-Pair",
     "name": "Locations + Valid + Asc", "expected": "Results sorted A-Z"},
    {"id": "TC_AP_02", "module": "Search", "technique": "All-Pair",
     "name": "Job Titles + Empty + Desc", "expected": "All titles, sorted Z-A"},
    {"id": "TC_AP_03", "module": "Search", "technique": "All-Pair",
     "name": "Skills + Special Chars", "expected": "'No Records Found'"},
    {"id": "TC_AP_04", "module": "Search", "technique": "All-Pair",
     "name": "KPIs + No Match", "expected": "'No Records Found'"},
    {"id": "TC_AP_05", "module": "Search", "technique": "All-Pair",
     "name": "Locations + SQL Injection", "expected": "Handles safely"},
    {"id": "TC_AP_06", "module": "Search", "technique": "All-Pair",
     "name": "Job Titles + Valid + Asc", "expected": "Matching results"},
    
    # === LOCATIONS - Use Case (2 cases) ===
    {"id": "TC_LOC_UC01", "module": "Locations", "technique": "Use Case",
     "name": "Delete location in use", "expected": "Error: 'Location assigned'"},
    {"id": "TC_LOC_UC02", "module": "Locations", "technique": "Use Case",
     "name": "Search location - partial", "expected": "Matching results"},
]


class OrangeHRMTester:
    """Main test automation class with multi-browser and data-driven support"""
    
    def __init__(self, browser: str = "chrome"):
        self.browser_name = browser
        self.driver = None
        self.test_data = self._load_test_data()
        
    def _load_test_data(self) -> dict:
        """Load test data from JSON file (Data-Driven)"""
        try:
            data_file = os.path.join(os.path.dirname(__file__), "test_data.json")
            with open(data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load test data: {e}")
            return {}
    
    def setup(self) -> bool:
        """Initialize WebDriver"""
        try:
            self.driver = BrowserFactory.get_driver(self.browser_name)
            logger.info(f"✓ Using {self.browser_name.upper()} browser")
            return True
        except Exception as e:
            logger.error(f"✗ Setup failed: {e}")
            return False
    
    def teardown(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def login(self) -> bool:
        """Login to OrangeHRM"""
        try:
            self.driver.get(BASE_URL)
            time.sleep(2)
            
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            self.driver.find_element(By.NAME, "username").send_keys(ADMIN_USERNAME)
            self.driver.find_element(By.NAME, "password").send_keys(ADMIN_PASSWORD)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            
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
    
    def navigate_to_menu(self, menu: str) -> bool:
        """Navigate to sidebar menu"""
        try:
            time.sleep(1)
            # Wait for sidebar to be present
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-main-menu"))
            )
            items = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-main-menu-item")
            for item in items:
                if menu.lower() in item.text.lower():
                    # Scroll into view and click
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", item)
                    time.sleep(0.3)
                    item.click()
                    time.sleep(2)
                    return True
            logger.warning(f"Menu '{menu}' not found")
            return False
        except Exception as e:
            logger.error(f"Navigate to menu error: {e}")
            return False
    
    def navigate_to_topbar(self, menu: str) -> bool:
        """Navigate to topbar menu (dropdown parent)"""
        try:
            time.sleep(1)
            # Wait for topbar
            WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-topbar-body-nav"))
            )
            # Find tabs with dropdown (--parent class)
            items = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-topbar-body-nav-tab")
            for item in items:
                if menu.lower() in item.text.lower():
                    item.click()
                    time.sleep(1)
                    return True
            logger.warning(f"Topbar menu '{menu}' not found")
            return False
        except Exception as e:
            logger.error(f"Navigate to topbar error: {e}")
            return False
    
    def navigate_to_submenu(self, submenu: str) -> bool:
        """Navigate to dropdown submenu"""
        try:
            # Wait for dropdown menu to appear
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-dropdown-menu"))
            )
            time.sleep(0.5)
            items = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-dropdown-menu a")
            for item in items:
                if submenu.lower() in item.text.lower():
                    item.click()
                    time.sleep(2)
                    return True
            logger.warning(f"Submenu '{submenu}' not found")
            return False
        except Exception as e:
            logger.error(f"Navigate to submenu error: {e}")
            return False
    
    def navigate_to(self, main: str, topbar: str = None, sub: str = None) -> bool:
        """Full navigation path"""
        self.navigate_to_menu(main)
        time.sleep(1)
        if topbar:
            self.navigate_to_topbar(topbar)
            if sub:
                self.navigate_to_submenu(sub)
        return True
    
    # ============================================
    # ACTION HELPERS
    # ============================================
    
    def click_add(self) -> bool:
        """Click Add button (in header container with plus icon)"""
        try:
            time.sleep(1)
            
            # Scroll to top first to avoid header overlap
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            
            # The Add button is in orangehrm-header-container and has bi-plus icon
            selectors = [
                ".orangehrm-header-container button.oxd-button--secondary",
                "button.oxd-button--secondary i.bi-plus",
            ]
            
            for selector in selectors:
                try:
                    if "i.bi-plus" in selector:
                        # Find button containing the plus icon
                        icons = self.driver.find_elements(By.CSS_SELECTOR, "i.bi-plus")
                        for icon in icons:
                            btn = icon.find_element(By.XPATH, "./..")
                            if btn.tag_name == "button":
                                # Use JavaScript click to avoid intercept
                                self.driver.execute_script("arguments[0].click();", btn)
                                time.sleep(2)
                                logger.info("✓ Clicked Add button via icon")
                                return True
                    else:
                        btn = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        # Use JavaScript click to avoid intercept
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(2)
                        logger.info("✓ Clicked Add button via selector")
                        return True
                except:
                    continue
            
            # Fallback: find any button with "Add" text and use JS click
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.oxd-button--secondary")
            for btn in buttons:
                if "add" in btn.text.lower():
                    self.driver.execute_script("arguments[0].click();", btn)
                    time.sleep(2)
                    logger.info("✓ Clicked Add button via text match")
                    return True
            
            logger.error("Add button not found")
            return False
        except Exception as e:
            logger.error(f"Click Add button error: {e}")
            return False
    
    def click_save(self) -> bool:
        """Click Save button"""
        try:
            time.sleep(0.5)
            # Find submit button
            btn = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
            )
            # Use JavaScript click to avoid intercept
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(3)
            logger.info("✓ Clicked Save button")
            return True
        except Exception as e:
            logger.error(f"Click Save button error: {e}")
            return False
    
    def fill_input(self, label: str, value: str) -> bool:
        """Fill input field by label"""
        try:
            groups = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-input-group")
            for g in groups:
                try:
                    label_elem = g.find_element(By.CSS_SELECTOR, ".oxd-label")
                    if label.lower() in label_elem.text.lower():
                        inp = g.find_element(By.CSS_SELECTOR, "input.oxd-input")
                        inp.clear()
                        time.sleep(0.2)
                        inp.send_keys(value)
                        return True
                except:
                    continue
            # Fallback: try by placeholder
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input.oxd-input")
            for inp in inputs:
                placeholder = inp.get_attribute("placeholder") or ""
                if label.lower() in placeholder.lower():
                    inp.clear()
                    inp.send_keys(value)
                    return True
            logger.warning(f"Input field '{label}' not found")
            return False
        except Exception as e:
            logger.error(f"Fill input error: {e}")
            return False
    
    def select_dropdown(self, label: str, option: str) -> bool:
        """Select dropdown option"""
        try:
            groups = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-input-group")
            for g in groups:
                try:
                    label_elem = g.find_element(By.CSS_SELECTOR, ".oxd-label")
                    if label.lower() in label_elem.text.lower():
                        dd = g.find_element(By.CSS_SELECTOR, ".oxd-select-text")
                        dd.click()
                        time.sleep(1)
                        
                        # Wait for dropdown options
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-select-dropdown"))
                        )
                        
                        opts = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-select-option")
                        for o in opts:
                            # If option is empty, select first non-empty option
                            if option == "" or option.lower() in o.text.lower():
                                o.click()
                                time.sleep(0.5)
                                return True
                except:
                    continue
            logger.warning(f"Dropdown '{label}' not found")
            return False
        except Exception as e:
            logger.error(f"Select dropdown error: {e}")
            return False
    
    def check_success(self) -> bool:
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-toast--success"))
            )
            return True
        except:
            return False
    
    def check_error(self) -> Tuple[bool, str]:
        try:
            errors = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-input-field-error-message")
            if errors:
                return True, errors[0].text
            toast = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-toast--error")
            if toast:
                return True, toast[0].text
            return False, ""
        except:
            return False, ""
    
    def take_screenshot(self, name: str) -> str:
        try:
            if not os.path.exists(SCREENSHOT_DIR):
                os.makedirs(SCREENSHOT_DIR)
            filename = os.path.join(SCREENSHOT_DIR, f"{name}_{datetime.now().strftime('%H%M%S')}.png")
            self.driver.save_screenshot(filename)
            return filename
        except:
            return ""
    
    # ============================================
    # DATA-DRIVEN TEST EXECUTION
    # ============================================
    
    def get_test_data(self, module: str, scenario: str) -> list:
        """Get test data for data-driven testing"""
        try:
            return self.test_data.get(module.lower(), {}).get(scenario, [])
        except:
            return []
    
    def run_test(self, test_case: dict) -> TestResult:
        """Execute a single test case"""
        test_id = test_case["id"]
        start = time.time()
        
        logger.info(f"  Running {test_id}: {test_case['name']}")
        
        try:
            # Get test function or use generic
            func = getattr(self, f"test_{test_id.lower()}", None)
            
            if func:
                actual, passed = func()
            else:
                # Generic test - mark as skipped
                actual = "No specific implementation"
                passed = None
            
            duration = time.time() - start
            
            if passed is None:
                status = TestStatus.SKIPPED
            elif passed:
                status = TestStatus.PASSED
            else:
                status = TestStatus.FAILED
                self.take_screenshot(test_id)
            
            return TestResult(
                test_id=test_id,
                test_name=test_case["name"],
                module=test_case["module"],
                technique=test_case["technique"],
                browser=self.browser_name,
                status=status,
                expected=test_case["expected"],
                actual=actual,
                duration=duration
            )
            
        except Exception as e:
            return TestResult(
                test_id=test_id,
                test_name=test_case["name"],
                module=test_case["module"],
                technique=test_case["technique"],
                browser=self.browser_name,
                status=TestStatus.ERROR,
                expected=test_case["expected"],
                actual=str(e),
                duration=time.time() - start,
                error_message=str(e)
            )
    
    # ============================================
    # TEST IMPLEMENTATIONS (Data-Driven)
    # ============================================
    
    def test_tc_loc_d01(self) -> Tuple[str, bool]:
        """Add location - valid data (Data-Driven)"""
        # Get test data
        data_list = self.get_test_data("locations", "valid")
        if not data_list:
            data_list = [{"name": "Test Office", "country": "Viet Nam", "city": "HCM", "phone": ""}]
        
        data = data_list[0]
        
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add()
        
        self.fill_input("Name", f"{data['name']} {datetime.now().strftime('%H%M%S')}")
        self.select_dropdown("Country", data["country"])
        if data.get("city"):
            self.fill_input("City", data["city"])
        if data.get("phone"):
            self.fill_input("Phone", data["phone"])
        
        self.click_save()
        
        if self.check_success():
            return "Success: Location created", True
        else:
            has_err, msg = self.check_error()
            return f"Failed: {msg}", False
    
    def test_tc_loc_d02(self) -> Tuple[str, bool]:
        """Add location - min name (Data-Driven)"""
        data_list = self.get_test_data("locations", "boundary_min_name")
        data = data_list[0] if data_list else {"name": "A", "country": "Viet Nam"}
        
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add()
        
        self.fill_input("Name", data["name"])
        self.select_dropdown("Country", data["country"])
        self.click_save()
        
        if self.check_success():
            return "Success: Min name location created", True
        else:
            has_err, msg = self.check_error()
            return f"Failed: {msg}", False
    
    def test_tc_loc_d04(self) -> Tuple[str, bool]:
        """Add location - empty name"""
        self.navigate_to("Admin", "Organization", "Locations")
        self.click_add()
        
        self.fill_input("Name", "")
        self.select_dropdown("Country", "Viet Nam")
        self.click_save()
        
        has_err, msg = self.check_error()
        if has_err and "required" in msg.lower():
            return f"Error: {msg}", True
        return "No validation error", False
    
    def test_tc_kpi_d01(self) -> Tuple[str, bool]:
        """Add KPI - valid (Data-Driven)"""
        data_list = self.get_test_data("kpis", "valid")
        data = data_list[0] if data_list else {"indicator": "Test KPI", "min": 0, "max": 100}
        
        self.navigate_to("Performance", "Configure", "KPIs")
        self.click_add()
        
        self.fill_input("Key Performance Indicator", f"{data['indicator']} {datetime.now().strftime('%H%M%S')}")
        self.select_dropdown("Job Title", "")  # First available
        self.fill_input("Minimum Rating", str(data["min"]))
        self.fill_input("Maximum Rating", str(data["max"]))
        
        self.click_save()
        
        if self.check_success():
            return "Success: KPI created", True
        else:
            has_err, msg = self.check_error()
            return f"Failed: {msg}", False
    
    def test_tc_kpi_d02(self) -> Tuple[str, bool]:
        """Add KPI - min > max (Data-Driven)"""
        data_list = self.get_test_data("kpis", "invalid_min_greater_max")
        data = data_list[0] if data_list else {"indicator": "Invalid", "min": 80, "max": 50}
        
        self.navigate_to("Performance", "Configure", "KPIs")
        self.click_add()
        
        self.fill_input("Key Performance Indicator", data["indicator"])
        self.select_dropdown("Job Title", "")
        self.fill_input("Minimum Rating", str(data["min"]))
        self.fill_input("Maximum Rating", str(data["max"]))
        
        self.click_save()
        
        has_err, msg = self.check_error()
        if has_err:
            return f"Error: {msg}", True
        return "No validation for invalid range", False
    
    def test_tc_skl_d01(self) -> Tuple[str, bool]:
        """Add skill - valid (Data-Driven)"""
        data_list = self.get_test_data("skills", "valid")
        data = data_list[0] if data_list else {"name": "Python"}
        
        self.navigate_to("Admin", "Qualifications", "Skills")
        self.click_add()
        
        self.fill_input("Name", f"{data['name']} {datetime.now().strftime('%H%M%S')}")
        self.click_save()
        
        if self.check_success():
            return "Success: Skill created", True
        else:
            has_err, msg = self.check_error()
            return f"Failed: {msg}", False


def run_tests_on_browser(browser: str, test_cases: list) -> List[TestResult]:
    """Run all tests on a specific browser"""
    logger.info(f"\n{'='*60}")
    logger.info(f"STARTING TESTS ON {browser.upper()}")
    logger.info(f"{'='*60}")
    
    tester = OrangeHRMTester(browser=browser)
    results = []
    
    if not tester.setup():
        logger.error(f"Failed to setup {browser}")
        return results
    
    if not tester.login():
        logger.error(f"Failed to login on {browser}")
        tester.teardown()
        return results
    
    for tc in test_cases:
        result = tester.run_test(tc)
        results.append(result)
        
        icon = "✓" if result.status == TestStatus.PASSED else "✗" if result.status == TestStatus.FAILED else "⊘"
        logger.info(f"    {icon} {result.test_id}: {result.status.value}")
    
    tester.teardown()
    return results


def main():
    """Main entry point - runs tests on all 3 browsers IN PARALLEL"""
    print("=" * 60)
    print("OrangeHRM AUTOMATION TESTING")
    print("Requirement 5: Multi-Browser + Data-Driven + PARALLEL")
    print("=" * 60)
    
    start_time = datetime.now()
    all_results = []
    browsers_tested = []
    
    # Run on all 3 browsers IN PARALLEL using ThreadPoolExecutor
    print(f"\n🚀 Starting PARALLEL execution on {len(BROWSERS)} browsers: {', '.join(BROWSERS)}")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all browser tests to run in parallel
        future_to_browser = {
            executor.submit(run_tests_on_browser, browser, TEST_CASES): browser
            for browser in BROWSERS
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_browser):
            browser = future_to_browser[future]
            try:
                results = future.result()
                if results:
                    all_results.extend(results)
                    browsers_tested.append(browser)
                    print(f"✓ {browser.upper()} completed: {len(results)} tests")
            except Exception as e:
                logger.error(f"Error testing on {browser}: {e}")
    
    end_time = datetime.now()
    
    # Generate HTML Report
    if all_results:
        report_gen = ReportGenerator()
        report_path = report_gen.generate_html_report(
            results=all_results,
            start_time=start_time,
            end_time=end_time,
            browsers_tested=browsers_tested
        )
        print(f"\n✓ HTML Report generated: {report_path}")
    
    # Print Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    
    total = len(all_results)
    passed = sum(1 for r in all_results if r.status == TestStatus.PASSED)
    failed = sum(1 for r in all_results if r.status == TestStatus.FAILED)
    skipped = sum(1 for r in all_results if r.status == TestStatus.SKIPPED)
    
    print(f"Browsers Tested: {', '.join(browsers_tested)}")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Pass Rate: {(passed/total*100):.1f}%" if total > 0 else "N/A")
    print("=" * 60)


if __name__ == "__main__":
    main()
