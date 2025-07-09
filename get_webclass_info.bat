@echo off
echo ===================================
echo WebClass Information Tool
echo ===================================
echo.

:: Change to script directory
cd PATH_TO_THIS_DIRECTORY

:: Create output directory if not exists
if not exist output mkdir output

:: Execute Python script
echo Getting WebClass information...
python .\src\main.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Success!
    echo Opening in browser...
    start .\output\webclass_info.html
) else (
    echo.
    echo An error occurred.
    echo.
    echo Recent log entries:
    findstr /n "^" .\output\webclass.log | findstr /b "[0-9]*:"
    echo.
    echo Please check the log file for details:
    echo .\output\webclass.log
    pause
)

echo.
echo =================================== 