@echo off
cls
echo.
echo ======================================================
echo PYTHON SERVER HEALTH CHECKER
echo ======================================================

set /p MODE="Enter URL to check instantly, or press ENTER for bulk CSV check: "

if defined MODE (
    echo Starting INSTANT check...
    REM Mode B: Check single URL via argument
    "C:/Program Files/Python311/python.exe" health_checker.py --url "%MODE%"
) else (
    echo Starting BULK check from url_list.csv...
    REM Mode A: Check bulk list from CSV file (no arguments needed)
    "C:/Program Files/Python311/python.exe" health_checker.py
)

echo.
echo ======================================================
echo REPORT GENERATED. Check server_health_report.xlsx
echo ======================================================

pause