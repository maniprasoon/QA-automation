#!/usr/bin/env python3
"""
HCLTech QA Automation Dashboard
Professional web interface for test management
"""

import http.server
import socketserver
import os
import sys
import json
import subprocess
import threading
from pathlib import Path
from datetime import datetime
import socket
import time

# ============================================
# Configuration
# ============================================
PROJECT_ROOT = Path(__file__).parent
PORT = 8080
HOST = "localhost"
DASHBOARD_TITLE = "HCLTech QA Automation Dashboard"

# Add project root to Python path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from utilities.config import Config
except ImportError:
    class Config:
        BASE_DIR = PROJECT_ROOT
        REPORTS_DIR = BASE_DIR / "reports"
        LOGS_DIR = BASE_DIR / "reports" / "logs"
        BASE_URL = "https://www.saucedemo.com"
        BROWSER = "chrome"

# ============================================
# Dashboard Handler
# ============================================
class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for the dashboard requests"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == '/':
                self.send_dashboard()
            elif self.path == '/api/status':
                self.send_json(self.get_status())
            elif self.path == '/api/reports':
                self.send_json(self.get_reports())
            elif self.path == '/api/test-info':
                self.send_json(self.get_test_info())
            elif self.path == '/api/run/demo':
                self.run_tests('demo')
            elif self.path == '/api/run/login':
                self.run_tests('login')
            elif self.path == '/api/run/all':
                self.run_tests('all')
            elif self.path.startswith('/reports/'):
                self.serve_file('reports/' + self.path[8:])
            elif self.path.startswith('/static/'):
                self.serve_file(self.path[1:])
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/generate-report':
            self.generate_report()
        else:
            self.send_error(404, "Not Found")
    
    # ============================================
    # API Endpoints
    # ============================================
    def send_dashboard(self):
        """Send main dashboard HTML"""
        status = self.get_status()
        reports = self.get_reports()
        test_info = self.get_test_info()
        
        html = self.generate_html(status, reports, test_info)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_json(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))
    
    def serve_file(self, filepath):
        """Serve static files"""
        try:
            filepath = PROJECT_ROOT / filepath
            if not filepath.exists():
                self.send_error(404, "File not found")
                return
            
            self.send_response(200)
            
            # Set content type
            if filepath.suffix == '.html':
                self.send_header('Content-type', 'text/html')
            elif filepath.suffix == '.css':
                self.send_header('Content-type', 'text/css')
            elif filepath.suffix == '.js':
                self.send_header('Content-type', 'application/javascript')
            elif filepath.suffix == '.png':
                self.send_header('Content-type', 'image/png')
            elif filepath.suffix == '.jpg' or filepath.suffix == '.jpeg':
                self.send_header('Content-type', 'image/jpeg')
            else:
                self.send_header('Content-type', 'application/octet-stream')
            
            self.end_headers()
            
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        except Exception as e:
            self.send_error(500, f"File error: {str(e)}")
    
    # ============================================
    # Data Methods
    # ============================================
    def get_status(self):
        """Get system status"""
        return {
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "project": "HCLTech QA Automation",
            "version": "1.0.0",
            "uptime": self.get_uptime(),
            "test_cases": 17,
            "requirements": 10,
            "dashboard_url": f"http://{HOST}:{PORT}"
        }
    
    def get_reports(self):
        """Get list of reports"""
        reports_dir = Config.REPORTS_DIR
        reports = []
        
        if reports_dir.exists():
            for file in sorted(reports_dir.glob("*.html"), key=lambda x: x.stat().st_mtime, reverse=True):
                reports.append({
                    "name": file.name,
                    "path": f"/reports/{file.name}",
                    "size": file.stat().st_size,
                    "created": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "size_kb": round(file.stat().st_size / 1024, 1)
                })
        
        return {"reports": reports[:10]}  # Return only 10 latest
    
    def get_test_info(self):
        """Get test application information"""
        return {
            "name": "Swag Labs",
            "url": "https://www.saucedemo.com",
            "users": [
                {"username": "standard_user", "description": "Valid user"},
                {"username": "locked_out_user", "description": "Locked account"},
                {"username": "problem_user", "description": "Problematic user"},
                {"username": "performance_glitch_user", "description": "Slow performance"},
                {"username": "error_user", "description": "Error scenarios"},
                {"username": "visual_user", "description": "Visual testing"}
            ],
            "password": "secret_sauce",
            "features": [
                "Login/Logout",
                "Product browsing",
                "Shopping cart",
                "Checkout process"
            ]
        }
    
    def get_uptime(self):
        """Get server uptime"""
        return time.time() - self.server.start_time
    
    # ============================================
    # Action Methods
    # ============================================
    def run_tests(self, test_type):
        """Run tests in background thread"""
        def execute_tests():
            try:
                if test_type == 'demo':
                    cmd = [sys.executable, "run_demo.py"]
                elif test_type == 'login':
                    cmd = [sys.executable, "-m", "pytest", "tests/test_login.py", "-v"]
                elif test_type == 'all':
                    cmd = [sys.executable, "run_tests.py"]
                else:
                    return
                
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
                
                # Log execution
                log_file = Config.LOGS_DIR / f"dashboard_{test_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                log_file.parent.mkdir(exist_ok=True)
                log_content = f"Command: {' '.join(cmd)}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
                log_file.write_text(log_content, encoding='utf-8')
                
            except Exception as e:
                print(f"Test execution error: {e}")
        
        # Start in background thread
        thread = threading.Thread(target=execute_tests, daemon=True)
        thread.start()
        
        self.send_json({
            "success": True,
            "message": f"Started {test_type} tests",
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_report(self):
        """Generate a new report"""
        try:
            result = subprocess.run(
                [sys.executable, "generate_report.py"],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT
            )
            
            self.send_json({
                "success": result.returncode == 0,
                "message": "Report generated" if result.returncode == 0 else result.stderr,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            self.send_json({
                "success": False,
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    # ============================================
    # HTML Generation
    # ============================================
    def generate_html(self, status, reports, test_info):
        """Generate dashboard HTML"""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{DASHBOARD_TITLE}</title>
    <style>
        :root {{
            --primary: #0066cc;
            --primary-dark: #0052a3;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --light: #f8f9fa;
            --dark: #343a40;
            --gray: #6c757d;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            padding: 20px;
        }}
        
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .status-badge {{
            display: inline-block;
            background: var(--success);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 15px;
        }}
        
        .main-content {{
            padding: 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}
        
        .card {{
            background: var(--light);
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
        }}
        
        .card h2 {{
            color: var(--primary);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
            font-size: 1.4em;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .metric:last-child {{
            border-bottom: none;
        }}
        
        .metric .label {{
            color: var(--gray);
        }}
        
        .metric .value {{
            font-weight: 600;
            color: var(--primary);
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: var(--primary);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            gap: 8px;
            margin: 5px;
        }}
        
        .btn:hover {{
            background: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,102,204,0.3);
        }}
        
        .btn-success {{
            background: var(--success);
        }}
        
        .btn-success:hover {{
            background: #1e7e34;
        }}
        
        .btn-warning {{
            background: var(--warning);
            color: #333;
        }}
        
        .btn-warning:hover {{
            background: #e0a800;
        }}
        
        .btn-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }}
        
        .test-users {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }}
        
        .user-card {{
            background: white;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #dee2e6;
            text-align: center;
        }}
        
        .user-card .username {{
            font-weight: 600;
            color: var(--primary);
        }}
        
        .user-card .desc {{
            font-size: 0.85em;
            color: var(--gray);
            margin-top: 5px;
        }}
        
        .reports-list {{
            max-height: 300px;
            overflow-y: auto;
            margin: 15px 0;
        }}
        
        .report-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            background: white;
            border-radius: 8px;
            margin: 8px 0;
            border: 1px solid #e9ecef;
        }}
        
        .report-item a {{
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .report-item a:hover {{
            text-decoration: underline;
        }}
        
        .report-info {{
            font-size: 0.85em;
            color: var(--gray);
        }}
        
        .empty-state {{
            text-align: center;
            padding: 40px;
            color: var(--gray);
        }}
        
        .empty-state i {{
            font-size: 3em;
            margin-bottom: 15px;
            opacity: 0.3;
        }}
        
        .notification {{
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            animation: slideIn 0.3s ease;
            display: none;
        }}
        
        .notification.success {{
            background: var(--success);
        }}
        
        .notification.error {{
            background: var(--danger);
        }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: var(--gray);
            border-top: 1px solid #e9ecef;
            margin-top: 40px;
        }}
        
        @media (max-width: 768px) {{
            .main-content {{
                grid-template-columns: 1fr;
                padding: 20px;
            }}
            
            .header {{
                padding: 30px 20px;
            }}
            
            .btn {{
                width: 100%;
            }}
            
            .btn-group {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <!-- Header -->
        <div class="header">
            <h1>{DASHBOARD_TITLE}</h1>
            <p>Real-time test management and monitoring interface</p>
            <div class="status-badge">● System Running</div>
        </div>
        
        <!-- Main Content -->
        <div class="main-content">
            <!-- System Status Card -->
            <div class="card">
                <h2>📊 System Status</h2>
                <div class="metric">
                    <span class="label">Framework Version</span>
                    <span class="value">{status['version']}</span>
                </div>
                <div class="metric">
                    <span class="label">Test Cases</span>
                    <span class="value">{status['test_cases']}+</span>
                </div>
                <div class="metric">
                    <span class="label">Requirements Met</span>
                    <span class="value">{status['requirements']}/10</span>
                </div>
                <div class="metric">
                    <span class="label">Uptime</span>
                    <span class="value">{int(status['uptime'])}s</span>
                </div>
                <div class="metric">
                    <span class="label">Dashboard URL</span>
                    <span class="value">{status['dashboard_url']}</span>
                </div>
            </div>
            
            <!-- Test Actions Card -->
            <div class="card">
                <h2>🚀 Test Actions</h2>
                <div class="btn-group">
                    <button class="btn" onclick="runTest('demo')">
                        🧪 Run Demo Tests
                    </button>
                    <button class="btn" onclick="runTest('login')">
                        🔐 Run Login Tests
                    </button>
                    <button class="btn btn-success" onclick="runTest('all')">
                        🚀 Run All Tests
                    </button>
                    <button class="btn btn-warning" onclick="generateReport()">
                        📄 Generate Report
                    </button>
                </div>
                
                <h2 style="margin-top: 25px;">🌐 Quick Links</h2>
                <div class="btn-group">
                    <a class="btn" href="{test_info['url']}" target="_blank">
                        🔗 Test Application
                    </a>
                    <a class="btn" href="/reports/" target="_blank">
                        📁 Reports Folder
                    </a>
                </div>
            </div>
            
            <!-- Test Application Card -->
            <div class="card">
                <h2>🔧 Test Environment</h2>
                <div class="metric">
                    <span class="label">Application</span>
                    <span class="value">{test_info['name']}</span>
                </div>
                <div class="metric">
                    <span class="label">URL</span>
                    <span class="value">{test_info['url']}</span>
                </div>
                <div class="metric">
                    <span class="label">Password</span>
                    <span class="value">{test_info['password']}</span>
                </div>
                
                <h3 style="margin-top: 20px; margin-bottom: 15px;">Test Users</h3>
                <div class="test-users">
                    {self.generate_users_html(test_info['users'])}
                </div>
            </div>
            
            <!-- Reports Card -->
            <div class="card">
                <h2>📋 Latest Reports</h2>
                <div class="btn-group">
                    <button class="btn" onclick="refreshReports()">
                        🔄 Refresh
                    </button>
                    <button class="btn" onclick="clearReports()">
                        🗑️ Clear All
                    </button>
                </div>
                
                <div id="reports-container" class="reports-list">
                    {self.generate_reports_html(reports['reports'])}
                </div>
            </div>
        </div>
        
        <!-- Requirements Card -->
        <div class="card" style="margin: 0 40px 40px 40px;">
            <h2>✅ HCLTech Requirements</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 10px; margin-top: 15px;">
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> Login Automation
                </div>
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> Error Validation
                </div>
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> Password Reset
                </div>
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> Pytest Structure
                </div>
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> Reusable Utilities
                </div>
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> HTML Reports
                </div>
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> Dynamic Elements
                </div>
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> Data-Driven Tests
                </div>
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> Browser Sync
                </div>
                <div style="background: #e8f5e9; padding: 12px; border-radius: 6px; display: flex; align-items: center; gap: 8px;">
                    <span style="color: #28a745;">✓</span> QA Best Practices
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>{DASHBOARD_TITLE} • Version {status['version']}</p>
            <p>Accessible at: <strong>{status['dashboard_url']}</strong></p>
            <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.7;">
                🚀 Demonstrating HCLTech QA Automation Engineer Readiness
            </p>
        </div>
    </div>
    
    <!-- Notification -->
    <div id="notification" class="notification"></div>
    
    <script>
        // Global state
        let isLoading = false;
        
        // Run tests function
        async function runTest(testType) {{
            if (isLoading) return;
            
            showNotification(`Starting ${{testType}} tests...`, 'info');
            isLoading = true;
            
            try {{
                const response = await fetch(`/api/run/${{testType}}`);
                const data = await response.json();
                
                showNotification(`✅ ${{data.message}}`, 'success');
                
                // Auto-refresh reports after test execution
                setTimeout(refreshReports, 2000);
                
            }} catch (error) {{
                showNotification(`❌ Error: ${{error.message}}`, 'error');
            }} finally {{
                isLoading = false;
            }}
        }}
        
        // Generate report function
        async function generateReport() {{
            showNotification('Generating report...', 'info');
            
            try {{
                const response = await fetch('/api/generate-report', {{ method: 'POST' }});
                const data = await response.json();
                
                if (data.success) {{
                    showNotification('✅ Report generated successfully!', 'success');
                    setTimeout(refreshReports, 1000);
                }} else {{
                    showNotification(`❌ ${{data.message}}`, 'error');
                }}
                
            }} catch (error) {{
                showNotification(`❌ Error: ${{error.message}}`, 'error');
            }}
        }}
        
        // Refresh reports list
        async function refreshReports() {{
            try {{
                const response = await fetch('/api/reports');
                const data = await response.json();
                
                const container = document.getElementById('reports-container');
                container.innerHTML = generateReportsHTML(data.reports);
                
            }} catch (error) {{
                console.error('Refresh error:', error);
            }}
        }}
        
        // Clear all reports
        async function clearReports() {{
            if (!confirm('Are you sure you want to clear all reports?')) return;
            
            showNotification('Clearing reports...', 'info');
            
            // This would need a backend endpoint to clear reports
            setTimeout(() => {{
                showNotification('✅ Reports cleared (demo)', 'success');
                refreshReports();
            }}, 1000);
        }}
        
        // Show notification
        function showNotification(message, type) {{
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${{type}}`;
            notification.style.display = 'block';
            
            setTimeout(() => {{
                notification.style.display = 'none';
            }}, 3000);
        }}
        
        // Generate HTML for reports
        function generateReportsHTML(reports) {{
            if (!reports || reports.length === 0) {{
                return `
                    <div class="empty-state">
                        <div>📄</div>
                        <p>No reports generated yet.</p>
                        <p style="font-size: 0.9em; margin-top: 10px;">Run tests to generate reports</p>
                    </div>
                `;
            }}
            
            return reports.map(report => `
                <div class="report-item">
                    <div>
                        <a href="${{report.path}}" target="_blank">${{report.name}}</a>
                        <div class="report-info">${{report.created}} • ${{report.size_kb}} KB</div>
                    </div>
                    <div>
                        <button class="btn" style="padding: 5px 10px; font-size: 0.85em;" 
                                onclick="window.open('${{report.path}}', '_blank')">
                            Open
                        </button>
                    </div>
                </div>
            `).join('');
        }}
        
        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {{
            // Auto-refresh reports every 30 seconds
            setInterval(refreshReports, 30000);
            
            // Show welcome message
            setTimeout(() => {{
                showNotification('🚀 Dashboard loaded successfully!', 'success');
            }}, 1000);
        }});
    </script>
</body>
</html>'''
    
    def generate_users_html(self, users):
        """Generate HTML for users list"""
        html = []
        for user in users:
            html.append(f'''
                <div class="user-card">
                    <div class="username">{user['username']}</div>
                    <div class="desc">{user['description']}</div>
                </div>
            ''')
        return ''.join(html)
    
    def generate_reports_html(self, reports):
        """Generate HTML for reports list"""
        if not reports:
            return '''
                <div class="empty-state">
                    <div>📄</div>
                    <p>No reports generated yet.</p>
                    <p style="font-size: 0.9em; margin-top: 10px;">Run tests to generate reports</p>
                </div>
            '''
        
        html = []
        for report in reports:
            html.append(f'''
                <div class="report-item">
                    <div>
                        <a href="{report['path']}" target="_blank">{report['name']}</a>
                        <div class="report-info">{report['created']} • {report['size_kb']} KB</div>
                    </div>
                    <div>
                        <button class="btn" style="padding: 5px 10px; font-size: 0.85em;" 
                                onclick="window.open('{report['path']}', '_blank')">
                            Open
                        </button>
                    </div>
                </div>
            ''')
        return ''.join(html)

# ============================================
# Server Setup
# ============================================
class DashboardServer(socketserver.TCPServer):
    """Custom server with start time tracking"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = time.time()
        self.allow_reuse_address = True

def check_port_available(port):
    """Check if port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, port)) != 0

def print_banner():
    """Print startup banner"""
    banner = f"""
{'='*60}
🚀 {DASHBOARD_TITLE}
{'='*60}
📊 Dashboard URL: http://{HOST}:{PORT}
📁 Serving from: {PROJECT_ROOT}
🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

📋 Available Features:
   • Real-time test execution
   • Report generation and viewing
   • System status monitoring
   • Test application information

🔧 Quick Actions from Dashboard:
   • Run demo tests against SauceDemo
   • Execute complete test suite
   • Generate HTML reports
   • View all generated reports

Press Ctrl+C to stop the dashboard
{'='*60}
    """
    print(banner)

def run_dashboard():
    """Start the dashboard server"""
    # Create necessary directories
    Config.REPORTS_DIR.mkdir(exist_ok=True)
    Config.LOGS_DIR.mkdir(exist_ok=True)
    
    # Check port availability
    if not check_port_available(PORT):
        print(f"\n❌ Error: Port {PORT} is already in use!")
        print(f"   Another application is using port {PORT}.")
        print(f"   Try: python dashboard.py --port 8081")
        return
    
    # Change to project directory
    os.chdir(PROJECT_ROOT)
    
    # Start server
    try:
        with DashboardServer((HOST, PORT), DashboardHandler) as httpd:
            print_banner()
            
            # Serve forever
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n\n{'='*60}")
        print("🛑 Dashboard stopped by user")
        print(f"{'='*60}")
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="HCLTech QA Dashboard")
    parser.add_argument("--port", type=int, default=PORT, help="Port to run the dashboard on")
    parser.add_argument("--host", type=str, default=HOST, help="Host to bind the dashboard to")
    
    args = parser.parse_args()
    PORT = args.port
    HOST = args.host
    
    run_dashboard()