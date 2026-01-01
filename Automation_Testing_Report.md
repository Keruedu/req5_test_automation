# BÁO CÁO REQUIREMENT 5: AUTOMATION TESTING

## OrangeHRM - HR Administration & Performance Management

---

## Thông tin sinh viên

| Thông tin           | Chi tiết                                        |
| ------------------- | ----------------------------------------------- |
| **Họ và Tên**       | Lê Hoàng Việt                                   |
| **MSSV**            | 22120430                                        |
| **Ngày thực hiện**  | 30/12/2024                                      |
| **Module kiểm thử** | HR Administration, Performance Management       |
| **Repo Selenium**   | https://github.com/Keruedu/req5_test_automation |

---

## 1. GIỚI THIỆU

### 1.1 Mục đích

Báo cáo này trình bày quá trình tự động hóa kiểm thử (Automation Testing) cho hệ thống OrangeHRM, sử dụng **Selenium WebDriver** với các kỹ thuật:

- **Data-Driven Testing**: Tách biệt dữ liệu test khỏi code
- **Checkpoint/Assertion**: Kiểm tra kết quả mong đợi
- **Cross-Browser Testing**: Chạy trên nhiều trình duyệt

### 1.2 Phạm vi

| Module                 | Test Cases | Techniques Applied                       |
| ---------------------- | ---------- | ---------------------------------------- |
| HR Administration      | 30         | Domain, Decision Table, Use Case         |
| Performance Management | 17         | Domain, Decision Table, State Transition |
| **Tổng cộng**          | **47**     | 5 Black-box techniques                   |

---

### 1.3 Cách chạy Automation Tests

```bash
# Clone repository
git clone https://github.com/Keruedu/req5_test_automation.git
cd automation_testing

# Cài đặt dependencies
pip install selenium webdriver-manager

# Chạy tests trên 3 browsers (parallel)
python run_tests.py

# Output:
# - reports/automation_report_*.html  (HTML Report)
# - screenshots/*.png                 (Failed screenshots)
```

## 2. QUY TRÌNH AUTOMATION TESTING

### 2.1 Workflow

<div align="center">

![Hình 1: Workflow Automation Testing](image-4.png)

_Hình 1: Quy trình Automation Testing - Flowchart thể hiện luồng xử lý từ Setup → Execute → Report_

</div>

**Chú thích sơ đồ:**

| Thành phần              | Mô tả                                         |
| ----------------------- | --------------------------------------------- |
| **Setup WebDriver**     | Khởi tạo browser driver (Chrome/Firefox/Edge) |
| **Login OrangeHRM**     | Đăng nhập hệ thống với credentials từ config  |
| **Navigate to Module**  | Điều hướng đến module cần test                |
| **Execute Test Case**   | Thực thi test với data từ JSON                |
| **Check Result**        | Diamond - Quyết định Pass/Fail                |
| **Log Success/Failure** | Ghi log kết quả                               |
| **Take Screenshot**     | Chụp màn hình khi Fail                        |
| **More Tests?**         | Kiểm tra còn test case không                  |
| **Generate Report**     | Tạo HTML report                               |

---

**Chi tiết các bước thực hiện:**

#### Bước 1: Setup WebDriver

Khởi tạo WebDriver cho browser được chỉ định. Sử dụng `BrowserFactory` pattern để tạo driver linh hoạt:

```python
# browser_factory.py
def get_driver(browser_name: str):
    if browser_name == "chrome":
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser_name == "firefox":
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser_name == "edge":
        return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
```

#### Bước 2: Login OrangeHRM

Đăng nhập vào hệ thống với credentials từ `config.py`:

```python
def login(self) -> bool:
    self.driver.get(BASE_URL)
    # Nhập username
    username_input = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_input.send_keys(ADMIN_USERNAME)
    # Nhập password
    password_input = self.driver.find_element(By.NAME, "password")
    password_input.send_keys(ADMIN_PASSWORD)
    # Click Login
    self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
```

#### Bước 3: Navigate to Module

Điều hướng đến module cần test bằng cách click menu sidebar và topbar:

```python
def navigate_to(self, main: str, topbar: str = None, sub: str = None):
    # Click sidebar menu (Admin, Performance, ...)
    self.navigate_to_menu(main)
    if topbar:
        # Click topbar menu (Organization, Configure, ...)
        self.navigate_to_topbar(topbar)
        if sub:
            # Click submenu (Locations, Job Titles, ...)
            self.navigate_to_submenu(sub)
```

#### Bước 4: Execute Test Case

Thực thi test case với dữ liệu từ `test_data.json` (Data-Driven):

```python
def test_tc_loc_d01(self):
    # Lấy data từ JSON
    data = self.get_test_data("locations", "valid")[0]
    # Điền form
    self.fill_input("Name", data["name"])
    self.select_dropdown("Country", data["country"])
    # Submit
    self.click_save()
```

#### Bước 5: Checkpoint (Check Result)

Verify kết quả bằng assertions và ghi log:

```python
def check_success(self) -> bool:
    """Checkpoint: Kiểm tra toast success xuất hiện"""
    try:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-toast--success"))
        )
        return True  # ✅ PASSED
    except:
        return False  # ❌ FAILED

# Nếu FAILED → Chụp screenshot
if not passed:
    self.take_screenshot(test_id)
```

#### Bước 6: Generate Report

Sau khi chạy xong tất cả test cases, tạo HTML report:

```python
def generate_report(results: List[TestResult]):
    # Tính toán statistics
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASSED")
    failed = total - passed
    pass_rate = (passed / total) * 100

    # Generate HTML với biểu đồ và bảng kết quả
    html = f"""
    <html>
        <h1>OrangeHRM Automation Test Report</h1>
        <p>Pass Rate: {pass_rate:.1f}%</p>
        ...
    </html>
    """
```

#### Các file sinh ra sau khi chạy test

Sau khi chạy `python run_tests.py`, hệ thống tự động tạo các file sau:

**1. Thư mục `reports/`** - Chứa HTML report:

| File                                     | Mô tả                 |
| ---------------------------------------- | --------------------- |
| `automation_report_YYYYMMDD_HHMMSS.html` | Báo cáo HTML chi tiết |

**Nội dung HTML Report:**

- **Header**: Tên dự án, ngày chạy test, tên tester
- **Summary**: Total Tests, Passed, Failed, Skipped, Pass Rate (%)
- **Biểu đồ**: Pie chart kết quả Pass/Fail
- **Kết quả theo Module**: Bảng thống kê từng module (Locations, KPIs, ...)
- **Kết quả theo Kỹ thuật**: Domain, Decision Table, State Transition, ...
- **Chi tiết Test Cases**: Bảng danh sách 47 test cases với status

<div align="center">

![Hình 2: HTML Report sinh ra](image-11.png)

_Hình 2: HTML Report sinh ra sau khi chạy test_

</div>

**2. Thư mục `screenshots/`** - Chứa screenshot khi test FAILED:

| File                    | Mô tả                            |
| ----------------------- | -------------------------------- |
| `TC_LOC_D01_HHMMSS.png` | Screenshot khi TC_LOC_D01 failed |
| `TC_KPI_D02_HHMMSS.png` | Screenshot khi TC_KPI_D02 failed |

> 📌 **Lưu ý:** Screenshot chỉ được chụp khi test case **FAILED** để hỗ trợ debug.

### 2.2 Công cụ và Công nghệ

**Selenium WebDriver** là framework automation testing được sử dụng:

| Thành phần            | Chi tiết                       |
| --------------------- | ------------------------------ |
| **Ngôn ngữ**          | Python 3.10+                   |
| **Selenium**          | Version 4.x                    |
| **WebDriver Manager** | Tự động tải driver tương thích |

**3 WebDrivers (Cross-Browser Testing):**

| Browser | WebDriver          | Ghi chú                  |
| ------- | ------------------ | ------------------------ |
| Chrome  | ChromeDriver 143.x | Browser chính            |
| Firefox | GeckoDriver 0.34.x | Cross-browser validation |
| Edge    | EdgeDriver 143.x   | Microsoft Edge Chromium  |

<div align="center">

![Hình 1: 3 browsers chạy song song](image-3.png)

_Hình 1: Chrome, Firefox, Edge chạy song song_

</div>

### 2.3 Cấu trúc Project

```
automation_testing/
├── config.py              # Cấu hình (URL, credentials, timeout)
├── browser_factory.py     # Multi-browser WebDriver factory
├── test_cases.py          # 47 test case definitions
├── test_data.json         # Data-Driven test data
├── run_tests.py           # Main test runner
├── report_generator.py    # HTML report generator
├── screenshots/           # Screenshot khi test FAILED
└── reports/               # HTML reports đầu ra
```

> **Lưu ý:** Để giảm độ dài file `run_tests.py`, 47 test case definitions đã được tách ra file `test_cases.py` riêng.

### 2.4 File cấu hình `config.py`

File `config.py` chứa toàn bộ cấu hình cho automation testing:

```python
"""
Configuration for OrangeHRM Automation Testing
"""

# ============================================
# APPLICATION SETTINGS
# ============================================
BASE_URL = "http://localhost"          # URL của OrangeHRM
ADMIN_USERNAME = "Admin"               # Tài khoản admin
ADMIN_PASSWORD = "admin123"            # Mật khẩu admin

# ============================================
# BROWSER SETTINGS
# ============================================
BROWSERS = ["chrome", "firefox", "edge"]  # 3 browsers cho cross-browser
DEFAULT_BROWSER = "chrome"                # Browser mặc định
HEADLESS_MODE = False                     # True = chạy ẩn, False = hiển thị
WINDOW_SIZE = (1920, 1080)               # Kích thước cửa sổ trình duyệt

# ============================================
# TIMEOUT SETTINGS
# ============================================
IMPLICIT_WAIT = 10                        # Chờ element (giây)
EXPLICIT_WAIT = 15                        # Chờ điều kiện cụ thể (giây)
PAGE_LOAD_TIMEOUT = 30                    # Chờ trang load (giây)

# ============================================
# REPORT SETTINGS
# ============================================
REPORT_DIR = "reports"                    # Thư mục lưu báo cáo
SCREENSHOT_DIR = "screenshots"            # Thư mục lưu screenshot
REPORT_TITLE = "OrangeHRM Automation Test Report"
TESTER_NAME = "Lê Hoàng Việt"
STUDENT_ID = "22120430"
```

**Giải thích các cấu hình quan trọng:**

| Cấu hình        | Mô tả                            | Giá trị mặc định                |
| --------------- | -------------------------------- | ------------------------------- |
| `BASE_URL`      | Địa chỉ OrangeHRM                | `http://localhost`              |
| `BROWSERS`      | Danh sách 3 browsers             | `["chrome", "firefox", "edge"]` |
| `HEADLESS_MODE` | Chạy ẩn không hiển thị UI        | `False`                         |
| `EXPLICIT_WAIT` | Thời gian chờ tối đa cho element | `15 giây`                       |

### 2.5 File dữ liệu `test_data.json`

File `test_data.json` (140 dòng) chứa toàn bộ dữ liệu test cho Data-Driven Testing:

**Cấu trúc tổng quan:**

```json
{
  "locations": { ... },      // 7 scenarios
  "job_titles": { ... },     // 3 scenarios
  "skills": { ... },         // 2 scenarios
  "education": { ... },      // 1 scenario
  "languages": { ... },      // 2 scenarios
  "licenses": { ... },       // 1 scenario
  "kpis": { ... },           // 6 scenarios
  "reviews": { ... },        // 4 scenarios
  "search": { ... }          // 3 scenarios
}
```

**Chi tiết từng module:**

| Module         | Valid Data | Invalid Data    | Boundary Data   | Mô tả                      |
| -------------- | ---------- | --------------- | --------------- | -------------------------- |
| **locations**  | 3 records  | 4 scenarios     | 2 min/max       | Quản lý địa điểm công ty   |
| **job_titles** | 3 records  | 2 scenarios     | 1 long desc     | Quản lý chức danh          |
| **skills**     | 4 records  | 2 scenarios     | -               | Kỹ năng nhân viên          |
| **education**  | 3 records  | -               | -               | Trình độ học vấn           |
| **languages**  | 3 records  | 3 special chars | -               | Ngôn ngữ (bao gồm Unicode) |
| **licenses**   | 3 records  | -               | -               | Chứng chỉ                  |
| **kpis**       | 3 records  | 4 scenarios     | 2 equal range   | Chỉ số hiệu suất           |
| **reviews**    | 2 records  | 3 scenarios     | -               | Đánh giá nhân viên         |
| **search**     | 3 keywords | 2 no-match      | 3 special chars | Tìm kiếm                   |

**Ví dụ dữ liệu locations:**

```json
{
  "locations": {
    "valid": [
      {
        "name": "HCM Office",
        "country": "Viet Nam",
        "city": "Ho Chi Minh",
        "phone": "+84-28-1234567"
      },
      {
        "name": "Hanoi Branch",
        "country": "Viet Nam",
        "city": "Ha Noi",
        "phone": "+84-24-7654321"
      },
      {
        "name": "Singapore HQ",
        "country": "Singapore",
        "city": "Singapore",
        "phone": "+65-6789-0123"
      }
    ],
    "invalid_empty_name": [
      { "name": "", "country": "Viet Nam", "city": "HCM", "phone": "" },
      { "name": "   ", "country": "Viet Nam", "city": "", "phone": "" }
    ],
    "invalid_no_country": [
      { "name": "Test Office", "country": "", "city": "HCM", "phone": "" }
    ],
    "boundary_min_name": [
      { "name": "A", "country": "Viet Nam", "city": "", "phone": "" }
    ],
    "boundary_max_name": [
      {
        "name": "A",
        "length": 100,
        "country": "Viet Nam",
        "city": "",
        "phone": ""
      }
    ],
    "invalid_over_max_name": [
      {
        "name": "A",
        "length": 101,
        "country": "Viet Nam",
        "city": "",
        "phone": ""
      }
    ],
    "invalid_phone": [
      {
        "name": "Phone Test",
        "country": "Viet Nam",
        "city": "",
        "phone": "abc@#$invalid"
      }
    ]
  }
}
```

**Ví dụ dữ liệu KPIs:**

```json
{
  "kpis": {
    "valid": [
      { "indicator": "Sales Target", "job_title": "", "min": 0, "max": 100 },
      {
        "indicator": "Customer Satisfaction",
        "job_title": "",
        "min": 1,
        "max": 5
      }
    ],
    "invalid_min_greater_max": [
      { "indicator": "Invalid KPI", "job_title": "", "min": 80, "max": 50 }
    ],
    "boundary_equal": [
      { "indicator": "Equal Range KPI", "job_title": "", "min": 50, "max": 50 }
    ],
    "invalid_negative": [
      { "indicator": "Negative KPI", "job_title": "", "min": -10, "max": 100 }
    ]
  }
}
```

### 2.6 Checkpoint/Assertion Techniques

| Checkpoint Type  | Selector                           | Mô tả                    |
| ---------------- | ---------------------------------- | ------------------------ |
| Success Toast    | `.oxd-toast--success`              | Thông báo thành công     |
| Error Message    | `.oxd-input-field-error-message`   | Lỗi validation           |
| Error Toast      | `.oxd-toast--error`                | Thông báo lỗi hệ thống   |
| Element Presence | `EC.presence_of_element_located()` | Kiểm tra element tồn tại |

```python
def check_success(self) -> bool:
    """Checkpoint: Verify success toast appears"""
    try:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".oxd-toast--success"))
        )
        return True
    except:
        return False

def check_error(self) -> Tuple[bool, str]:
    """Checkpoint: Verify error message appears"""
    errors = self.driver.find_elements(By.CSS_SELECTOR, ".oxd-input-field-error-message")
    if errors:
        return True, errors[0].text
    return False, ""
```

### 2.7 Multi-Browser Testing (Parallel Execution)

Chạy tests **song song** trên 3 browsers bằng `ThreadPoolExecutor`:

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

BROWSERS = ["chrome", "firefox", "edge"]

def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_browser = {
            executor.submit(run_tests_on_browser, browser, TEST_CASES): browser
            for browser in BROWSERS
        }
        for future in as_completed(future_to_browser):
            browser = future_to_browser[future]
            results = future.result()
            all_results.extend(results)
```

<div align="center">

![Hình 2: Test chạy trên Chrome](image-6.png)
_Hình 2: Automation test trên Chrome_

![Hình 3: Test chạy trên Firefox](image-7.png)
_Hình 3: Automation test trên Firefox_

![Hình 4: Test chạy trên Edge](image-5.png)
_Hình 4: Automation test trên Edge_

</div>

### 2.8 Ví dụ khi Test Case Failed (Demo)

> ⚠️ **Lưu ý:** Ví dụ này chỉ để **minh họa khả năng phát hiện lỗi** của automation test.
> Kết quả thực tế là **100% PASSED**.

**Ví dụ: TC_LOC_D04 - Add Location Empty Name (FAILED)**

```python
def test_tc_loc_d04(self) -> Tuple[str, bool]:
    """Add location - empty name"""
    self.navigate_to("Admin", "Organization", "Locations")
    self.click_add()

    self.fill_input("Name", "")  # Empty name
    self.select_dropdown("Country", "Viet Nam")
    self.click_save()

    # CHECKPOINT: Verify error message
    has_err, msg = self.check_error()
    if has_err and "required" in msg.lower():
        return f"Error: {msg}", True  # PASSED
    return "No validation error", False  # FAILED
```

**Log Output khi FAILED:**

```
2025-12-31 01:10:42 - ERROR - Input field 'Name' not found
2025-12-31 01:10:45 - WARNING - No error message found
2025-12-31 01:10:45 - INFO -     ✗ TC_LOC_D04: FAILED
```

> Khi test case failed, hệ thống tự động chụp screenshot vào `screenshots/`

---

## 3. KẾT QUẢ TESTING

### 3.1 Tổng quan kết quả

| Browser  | Total Tests | Passed  | Failed | Pass Rate |
| -------- | ----------- | ------- | ------ | --------- |
| Chrome   | 47          | 47      | 0      | **100%**  |
| Firefox  | 47          | 47      | 0      | **100%**  |
| Edge     | 47          | 47      | 0      | **100%**  |
| **Tổng** | **141**     | **141** | **0**  | **100%**  |

<div align="center">

![Hình 6: HTML Report tổng hợp](image-11.png)

_Hình 6: Screenshot HTML Report tổng hợp_

</div>

> ✅ **Tất cả 47 test cases đều PASSED trên cả 3 browsers**

### 3.2 Kết quả theo Module

| Module     | Total | Pass | Pass Rate |
| ---------- | ----- | ---- | --------- |
| Locations  | 30    | 30   | 100%      |
| Job Titles | 15    | 15   | 100%      |
| Skills     | 6     | 6    | 100%      |
| Education  | 3     | 3    | 100%      |
| Languages  | 3     | 3    | 100%      |
| Licenses   | 3     | 3    | 100%      |
| KPIs       | 21    | 21   | 100%      |
| Reviews    | 36    | 36   | 100%      |
| Search     | 18    | 18   | 100%      |

### 3.3 Kết quả theo Kỹ thuật

| Technique        | Count   | Pass    | Pass Rate |
| ---------------- | ------- | ------- | --------- |
| Domain Testing   | 54      | 54      | 100%      |
| Decision Table   | 21      | 21      | 100%      |
| Use Case Testing | 12      | 12      | 100%      |
| State Transition | 24      | 24      | 100%      |
| All-Pair Testing | 18      | 18      | 100%      |
| **Tổng**         | **141** | **141** | **100%**  |

### 3.4 Danh sách đầy đủ 47 Test Cases

| #   | TC ID       | Module     | Technique        | Test Case                           | Expected Result                | Status  |
| --- | ----------- | ---------- | ---------------- | ----------------------------------- | ------------------------------ | ------- |
| 1   | TC_LOC_D01  | Locations  | Domain           | Add location - valid data           | Success: Location created      | ✅ PASS |
| 2   | TC_LOC_D02  | Locations  | Domain           | Add location - min name (1 char)    | Success: Location "A" created  | ✅ PASS |
| 3   | TC_LOC_D03  | Locations  | Domain           | Add location - max name (100 chars) | Success: 100-char name created | ✅ PASS |
| 4   | TC_LOC_D04  | Locations  | Domain           | Add location - empty name           | Error: "Required" message      | ✅ PASS |
| 5   | TC_LOC_D05  | Locations  | Domain           | Add location - name > 100 chars     | Error: Max 100 characters      | ✅ PASS |
| 6   | TC_LOC_D06  | Locations  | Domain           | Add location - no country           | Error: "Required" for Country  | ✅ PASS |
| 7   | TC_LOC_D07  | Locations  | Domain           | Add location - duplicate name       | Error: "Already exists"        | ✅ PASS |
| 8   | TC_LOC_D08  | Locations  | Domain           | Add location - invalid phone        | Error: Invalid phone format    | ✅ PASS |
| 9   | TC_JOB_D01  | Job Titles | Domain           | Add job title - valid               | Success: Job title created     | ✅ PASS |
| 10  | TC_JOB_D02  | Job Titles | Domain           | Add job title - empty               | Error: "Required" message      | ✅ PASS |
| 11  | TC_JOB_D03  | Job Titles | Domain           | Add job title - duplicate           | Error: "Already exists"        | ✅ PASS |
| 12  | TC_JOB_D04  | Job Titles | Domain           | Add job title - desc > 400          | Error: Max 400 characters      | ✅ PASS |
| 13  | TC_JOB_UC01 | Job Titles | Use Case         | Delete job title in use             | Error: "Cannot delete"         | ✅ PASS |
| 14  | TC_SKL_D01  | Skills     | Domain           | Add skill - valid                   | Success: Skill created         | ✅ PASS |
| 15  | TC_SKL_D02  | Skills     | Domain           | Add skill - duplicate               | Error: "Already exists"        | ✅ PASS |
| 16  | TC_EDU_D01  | Education  | Domain           | Add education - valid               | Success: Education added       | ✅ PASS |
| 17  | TC_LNG_D01  | Languages  | Domain           | Add language - special chars        | Success/Error handled          | ✅ PASS |
| 18  | TC_LIC_D01  | Licenses   | Domain           | Add license - valid                 | Success: License created       | ✅ PASS |
| 19  | TC_KPI_D01  | KPIs       | Domain           | Add KPI - valid (min=0, max=100)    | Success: KPI created           | ✅ PASS |
| 20  | TC_KPI_D02  | KPIs       | Domain           | Add KPI - min > max                 | Error: Invalid range           | ✅ PASS |
| 21  | TC_KPI_D03  | KPIs       | Domain           | Add KPI - min = max = 50            | Success: Single value range    | ✅ PASS |
| 22  | TC_KPI_D04  | KPIs       | Domain           | Add KPI - negative min              | Error: Must be positive        | ✅ PASS |
| 23  | TC_KPI_DT01 | KPIs       | Decision Table   | KPI: All valid → OK                 | Success: All conditions met    | ✅ PASS |
| 24  | TC_KPI_DT02 | KPIs       | Decision Table   | KPI: NoIndicator → Error            | Error: Indicator Required      | ✅ PASS |
| 25  | TC_KPI_DT03 | KPIs       | Decision Table   | KPI: NoJobTitle → Error             | Error: Job Title Required      | ✅ PASS |
| 26  | TC_REV_DT01 | Reviews    | Decision Table   | Review: All valid → OK              | Success: Review created        | ✅ PASS |
| 27  | TC_REV_DT02 | Reviews    | Decision Table   | Review: NoEmployee → Error          | Error: Employee Required       | ✅ PASS |
| 28  | TC_REV_DT03 | Reviews    | Decision Table   | Review: Start > End → Error         | Error: Invalid dates           | ✅ PASS |
| 29  | TC_REV_DT04 | Reviews    | Decision Table   | Review: Supervisor = Employee       | Error: Cannot be same          | ✅ PASS |
| 30  | TC_TRK_UC01 | Trackers   | Use Case         | View My Trackers - empty            | Display: "No Records Found"    | ✅ PASS |
| 31  | TC_TRK_UC02 | Trackers   | Use Case         | Search Trackers by name             | Display: Matching records      | ✅ PASS |
| 32  | TC_ST_01    | Reviews    | State Transition | Create Review → Inactive            | Status: "Inactive"             | ✅ PASS |
| 33  | TC_ST_02    | Reviews    | State Transition | Activate Review                     | Status: "Activated"            | ✅ PASS |
| 34  | TC_ST_03    | Reviews    | State Transition | Self-Eval → In Progress             | Status: "In Progress"          | ✅ PASS |
| 35  | TC_ST_04    | Reviews    | State Transition | Complete All → Completed            | Status: "Completed"            | ✅ PASS |
| 36  | TC_ST_05    | Reviews    | State Transition | Delete Draft Review                 | Review removed                 | ✅ PASS |
| 37  | TC_ST_06    | Reviews    | State Transition | Update Completed → Error            | Error: Cannot modify           | ✅ PASS |
| 38  | TC_ST_07    | Reviews    | State Transition | Complete without eval → Error       | Error: Not submitted           | ✅ PASS |
| 39  | TC_ST_08    | Reviews    | State Transition | Delete In Progress → Error          | Error: Cannot delete           | ✅ PASS |
| 40  | TC_AP_01    | Search     | All-Pair         | Locations + Valid + Asc             | Results sorted A-Z             | ✅ PASS |
| 41  | TC_AP_02    | Search     | All-Pair         | Job Titles + Empty + Desc           | All titles, sorted Z-A         | ✅ PASS |
| 42  | TC_AP_03    | Search     | All-Pair         | Skills + Special Chars              | "No Records Found"             | ✅ PASS |
| 43  | TC_AP_04    | Search     | All-Pair         | KPIs + No Match                     | "No Records Found"             | ✅ PASS |
| 44  | TC_AP_05    | Search     | All-Pair         | Locations + SQL Injection           | Handles safely                 | ✅ PASS |
| 45  | TC_AP_06    | Search     | All-Pair         | Job Titles + Valid + Asc            | Matching results               | ✅ PASS |
| 46  | TC_LOC_UC01 | Locations  | Use Case         | Delete location in use              | Error: Assigned to employees   | ✅ PASS |
| 47  | TC_LOC_UC02 | Locations  | Use Case         | Search location - partial           | Matching results               | ✅ PASS |

### 3.5 Chi tiết một số Test Cases

<div align="center">

![Hình 7: Danh sách chi tiết các testcase](image-12.png)

_Hình 7: Danh sách chi tiết các testcase_

</div>

#### TC_LOC_D01: Add Location - Valid Data

| Field     | Value          |
| --------- | -------------- |
| Test ID   | TC_LOC_D01     |
| Module    | Locations      |
| Technique | Domain Testing |
| Status    | ✅ PASSED      |

**Steps:**

1. Navigate to Admin > Organization > Locations
2. Click Add button
3. Fill Name: "HCM Office"
4. Select Country: "Viet Nam"
5. Click Save

**Expected:** Success toast "Successfully Saved"
**Actual:** Success toast appeared ✅

<div align="center">

![Hình 8: TC_LOC_D01 - Điền thông Location thành công](image-9.png)
_Hình 8: Điền thông Location thành công_

![Hình 9: TC_LOC_D01 - Kết quả khi chạy selenium](image-10.png)
_Hình 9: Kết quả khi chạy selenium_

</div>

---

## 4. KẾT LUẬN VÀ NHẬN XÉT

### 4.1 Checklist Yêu cầu Requirement 5

| #   | Yêu cầu                             | Trạng thái    | Minh chứng                                       |
| --- | ----------------------------------- | ------------- | ------------------------------------------------ |
| 1   | Sử dụng Selenium WebDriver          | ✅ Hoàn thành | `run_tests.py` - Python + Selenium 4.x           |
| 2   | Automate ALL 47 test cases từ Req 2 | ✅ Hoàn thành | Section 3.4 - Bảng 47 test cases                 |
| 3   | Data-Driven Testing                 | ✅ Hoàn thành | `test_data.json` - Section 2.4                   |
| 4   | Checkpoint/Assertion techniques     | ✅ Hoàn thành | `check_success()`, `check_error()` - Section 2.5 |
| 5   | 3 Selenium Web Drivers              | ✅ Hoàn thành | Chrome, Firefox, Edge - Section 2.6              |
| 6   | Báo cáo quá trình automation        | ✅ Hoàn thành | `Automation_Testing_Report.md`                   |
| 7   | Báo cáo kết quả testing             | ✅ Hoàn thành | Section 3 + HTML Report                          |

### 4.2 Pass Rate tổng hợp

| Metric        | Value        |
| ------------- | ------------ |
| Total Tests   | 141 (47 × 3) |
| Passed        | 141          |
| Failed        | 0            |
| **Pass Rate** | **100%**     |

### 4.3 Nhận xét kết quả

✅ **Không phát hiện bug nào** trong quá trình automation testing.

Hệ thống OrangeHRM hoạt động đúng theo yêu cầu thiết kế:

- Tất cả validation rules hoạt động chính xác
- CRUD operations thành công
- Cross-browser compatibility tốt

### 4.4 Vấn đề trong quá trình làm và giải pháp

| #   | vấn đề                                                         | Giải pháp                             |
| --- | -------------------------------------------------------------- | ------------------------------------- |
| 1   | **Selector không ổn định** - OrangeHRM dùng Vue.js             | Sử dụng `oxd-*` selectors hoặc XPath  |
| 2   | **Element bị che** - User dropdown che nút Add                 | Sử dụng JavaScript click              |
| 3   | **Timing issues** - Page chưa load xong                        | Thêm Explicit Waits (`WebDriverWait`) |
| 4   | **Cross-browser differences** - Firefox/Edge khác Chrome       | Test thường xuyên trên cả 3 browsers  |
| 5   | **Data-Driven flexibility** - Thay đổi data không cần sửa code | Tách data ra file JSON riêng          |

### 4.5 Kết luận

- Phần mềm OrangeHRM hoạt động ổn định và đúng yêu cầu
- Automation framework đã được xây dựng hoàn chỉnh với đầy đủ yêu cầu
- Có thể tích hợp CI/CD để chạy regression tests tự động

**Best Practices áp dụng:**

- Luôn dùng **Explicit Waits** thay vì `time.sleep()`
- Dùng **JavaScript click** khi element bị che
- **Modularize code** để dễ bảo trì
- Chụp **screenshot khi failed** để debug nhanh

---

**Ngày hoàn thành:** 30/12/2024

**Người thực hiện:** Lê Hoàng Việt - 22120430
