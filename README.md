# Automation Testing - Requirement 5

## Mô tả

Automation Testing cho OrangeHRM sử dụng Selenium với:

- ✅ **Multi-browser**: Chrome, Firefox, Edge
- ✅ **Data-Driven Testing**: Test data từ JSON
- ✅ **HTML Report**: Báo cáo chi tiết với thống kê
- ✅ **47 Test Cases** từ Requirement 3

## Cấu trúc Files

```
automation_testing/
├── config.py           # Cấu hình (URL, credentials, timeouts)
├── browser_factory.py  # Multi-browser WebDriver (Chrome/Firefox/Edge)
├── test_data.json      # Test data cho Data-Driven testing
├── report_generator.py # Tạo HTML report
├── run_tests.py        # Main entry point
├── selenium_tests.py   # Test implementations chi tiết
└── README.md           # Hướng dẫn
```

## Cài đặt

```bash
pip install selenium webdriver-manager
```

## Chạy Tests

### Chạy trên tất cả 3 browsers (Chrome, Firefox, Edge)

```bash
cd automation_testing
python run_tests.py
```

### Chạy test chi tiết

```bash
python selenium_tests.py
```

## Yêu cầu đã đáp ứng

| Yêu cầu                 | Trạng thái | File                            |
| ----------------------- | ---------- | ------------------------------- |
| Selenium Automation     | ✅         | selenium_tests.py, run_tests.py |
| Data-Driven Testing     | ✅         | test_data.json                  |
| 3 WebDrivers (browsers) | ✅         | browser_factory.py              |
| Checkpoint/Assertion    | ✅         | check_success(), check_error()  |
| HTML Report             | ✅         | report_generator.py             |

## Test Cases Distribution

| Technique        | Count  | %    |
| ---------------- | ------ | ---- |
| Domain Testing   | 18     | 38%  |
| Decision Table   | 7      | 15%  |
| Use Case         | 4      | 9%   |
| State Transition | 8      | 17%  |
| All-Pair         | 6      | 13%  |
| Other            | 4      | 8%   |
| **Total**        | **47** | 100% |

## Output

- **Console**: Log kết quả test real-time
- **HTML Report**: `reports/automation_report_YYYYMMDD_HHMMSS.html`
- **Screenshots**: `screenshots/` (khi test fail)
