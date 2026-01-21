@echo off
echo ========================================
echo Starting HCLTech QA Automation Suite
echo ========================================

REM Start Dashboard in a new window
start cmd /k "cd /d %~dp0 && python dashboard.py"
timeout /t 3 /nobreak > nul

REM Generate and open report
python generate_report.py

echo.
echo ========================================
echo Dashboard: http://localhost:8080
echo Press any key to exit...
pause > nul