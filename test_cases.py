"""
Test Case Definitions for OrangeHRM Automation Testing
Contains 47 test cases for Requirement 5
"""

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


def get_test_case_by_id(test_id: str) -> dict:
    """Get a specific test case by ID"""
    for tc in TEST_CASES:
        if tc["id"] == test_id:
            return tc
    return None


def get_test_cases_by_module(module: str) -> list:
    """Get all test cases for a specific module"""
    return [tc for tc in TEST_CASES if tc["module"] == module]


def get_test_cases_by_technique(technique: str) -> list:
    """Get all test cases for a specific technique"""
    return [tc for tc in TEST_CASES if tc["technique"] == technique]
