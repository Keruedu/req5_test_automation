"""
HTML Report Generator for Automation Testing
Creates professional HTML reports with test results and screenshots
"""

import os
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

from config import REPORT_DIR, REPORT_TITLE, TESTER_NAME, STUDENT_ID


class TestStatus(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


@dataclass
class TestResult:
    test_id: str
    test_name: str
    module: str
    technique: str
    browser: str
    status: TestStatus
    expected: str
    actual: str
    duration: float
    screenshot: str = ""
    error_message: str = ""


class ReportGenerator:
    """Generate HTML reports for automation test results"""
    
    def __init__(self, report_dir: str = REPORT_DIR):
        self.report_dir = report_dir
        self._ensure_report_dir()
    
    def _ensure_report_dir(self):
        """Create report directory if not exists"""
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def generate_html_report(self, results: List[TestResult], 
                             start_time: datetime, 
                             end_time: datetime,
                             browsers_tested: List[str]) -> str:
        """Generate comprehensive HTML report"""
        
        # Calculate statistics
        total = len(results)
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        failed = sum(1 for r in results if r.status == TestStatus.FAILED)
        skipped = sum(1 for r in results if r.status == TestStatus.SKIPPED)
        errors = sum(1 for r in results if r.status == TestStatus.ERROR)
        pass_rate = (passed / total * 100) if total > 0 else 0
        duration = (end_time - start_time).total_seconds()
        
        # Group by browser
        browser_results = {}
        for r in results:
            if r.browser not in browser_results:
                browser_results[r.browser] = []
            browser_results[r.browser].append(r)
        
        # Group by module
        module_results = {}
        for r in results:
            if r.module not in module_results:
                module_results[r.module] = {"passed": 0, "failed": 0, "skipped": 0, "error": 0}
            if r.status == TestStatus.PASSED:
                module_results[r.module]["passed"] += 1
            elif r.status == TestStatus.FAILED:
                module_results[r.module]["failed"] += 1
            elif r.status == TestStatus.SKIPPED:
                module_results[r.module]["skipped"] += 1
            else:
                module_results[r.module]["error"] += 1
        
        # Group by technique
        technique_results = {}
        for r in results:
            if r.technique not in technique_results:
                technique_results[r.technique] = 0
            technique_results[r.technique] += 1
        
        html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{REPORT_TITLE}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{ 
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white; 
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header .subtitle {{ opacity: 0.9; font-size: 1.2em; }}
        .info-bar {{
            display: flex;
            justify-content: space-around;
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }}
        .info-item {{ text-align: center; }}
        .info-item .label {{ color: #666; font-size: 0.9em; }}
        .info-item .value {{ font-weight: bold; color: #333; font-size: 1.1em; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-card .number {{ font-size: 2.5em; font-weight: bold; }}
        .stat-card .label {{ color: #666; margin-top: 5px; }}
        .stat-card.total .number {{ color: #3498db; }}
        .stat-card.passed .number {{ color: #27ae60; }}
        .stat-card.failed .number {{ color: #e74c3c; }}
        .stat-card.skipped .number {{ color: #f39c12; }}
        .stat-card.errors .number {{ color: #9b59b6; }}
        
        .section {{ padding: 30px; }}
        .section-title {{ 
            font-size: 1.5em; 
            color: #2c3e50; 
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }}
        
        .browser-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .browser-tab {{
            padding: 10px 20px;
            background: #e0e0e0;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }}
        .browser-tab.active {{ background: #3498db; color: white; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{ 
            background: #2c3e50; 
            color: white;
            font-weight: 600;
        }}
        tr:hover {{ background: #f5f5f5; }}
        
        .status {{ 
            padding: 5px 15px; 
            border-radius: 20px; 
            font-weight: bold;
            font-size: 0.85em;
        }}
        .status.passed {{ background: #d4edda; color: #155724; }}
        .status.failed {{ background: #f8d7da; color: #721c24; }}
        .status.skipped {{ background: #fff3cd; color: #856404; }}
        .status.error {{ background: #f5c6cb; color: #721c24; }}
        
        .progress-bar {{
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
        }}
        .progress-bar .fill {{
            height: 100%;
            background: linear-gradient(90deg, #27ae60, #2ecc71);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        
        .module-chart {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .module-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #3498db;
        }}
        .module-card h4 {{ color: #2c3e50; margin-bottom: 10px; }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            background: #2c3e50;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .info-bar {{ flex-direction: column; gap: 10px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 {REPORT_TITLE}</h1>
            <p class="subtitle">OrangeHRM - HR Administration & Performance Management</p>
        </div>
        
        <div class="info-bar">
            <div class="info-item">
                <div class="label">Tester</div>
                <div class="value">{TESTER_NAME}</div>
            </div>
            <div class="info-item">
                <div class="label">MSSV</div>
                <div class="value">{STUDENT_ID}</div>
            </div>
            <div class="info-item">
                <div class="label">Ngày thực hiện</div>
                <div class="value">{start_time.strftime('%d/%m/%Y %H:%M')}</div>
            </div>
            <div class="info-item">
                <div class="label">Thời gian chạy</div>
                <div class="value">{duration:.1f}s</div>
            </div>
            <div class="info-item">
                <div class="label">Browsers</div>
                <div class="value">{', '.join(browsers_tested)}</div>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card total">
                <div class="number">{total}</div>
                <div class="label">Total Tests</div>
            </div>
            <div class="stat-card passed">
                <div class="number">{passed}</div>
                <div class="label">Passed ✓</div>
            </div>
            <div class="stat-card failed">
                <div class="number">{failed}</div>
                <div class="label">Failed ✗</div>
            </div>
            <div class="stat-card skipped">
                <div class="number">{skipped}</div>
                <div class="label">Skipped ⊘</div>
            </div>
            <div class="stat-card errors">
                <div class="number">{errors}</div>
                <div class="label">Errors ⚠</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📊 Pass Rate</h2>
            <div class="progress-bar">
                <div class="fill" style="width: {pass_rate}%">{pass_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📁 Kết quả theo Module</h2>
            <div class="module-chart">
"""
        
        for module, stats in module_results.items():
            module_total = stats["passed"] + stats["failed"] + stats["skipped"] + stats["error"]
            module_pass_rate = (stats["passed"] / module_total * 100) if module_total > 0 else 0
            html_content += f"""
                <div class="module-card">
                    <h4>{module}</h4>
                    <p>✓ Passed: {stats["passed"]} | ✗ Failed: {stats["failed"]}</p>
                    <p>Pass Rate: {module_pass_rate:.1f}%</p>
                </div>
"""
        
        html_content += """
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">🔬 Kết quả theo Kỹ thuật</h2>
            <table>
                <tr>
                    <th>Kỹ thuật</th>
                    <th>Số lượng Test Cases</th>
                </tr>
"""
        
        for technique, count in technique_results.items():
            html_content += f"""
                <tr>
                    <td>{technique}</td>
                    <td>{count}</td>
                </tr>
"""
        
        html_content += """
            </table>
        </div>
        
        <div class="section">
            <h2 class="section-title">📋 Chi tiết Test Cases</h2>
            <table>
                <tr>
                    <th>Test ID</th>
                    <th>Test Name</th>
                    <th>Module</th>
                    <th>Browser</th>
                    <th>Status</th>
                    <th>Duration</th>
                </tr>
"""
        
        for result in results:
            status_class = result.status.value.lower()
            html_content += f"""
                <tr>
                    <td><strong>{result.test_id}</strong></td>
                    <td>{result.test_name}</td>
                    <td>{result.module}</td>
                    <td>{result.browser}</td>
                    <td><span class="status {status_class}">{result.status.value}</span></td>
                    <td>{result.duration:.2f}s</td>
                </tr>
"""
        
        html_content += f"""
            </table>
        </div>
        
        <div class="footer">
            <p>🎓 Môn học: Kiểm thử phần mềm</p>
            <p>📅 Báo cáo được tạo lúc: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Save report
        report_filename = f"automation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        report_path = os.path.join(self.report_dir, report_filename)
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return report_path
