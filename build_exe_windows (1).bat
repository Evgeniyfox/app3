@echo off
title Metallurgy Advisor Pro - Build EXE

echo.
echo ============================================================
echo   Metallurgy Advisor Pro - Create standalone EXE
echo ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Install Python 3.11+ and add to PATH.
    pause & exit /b 1
)
for /f "tokens=*" %%v in ('python --version') do echo   Python: %%v

:: Install dependencies
echo.
echo   [1/3] Installing dependencies...
pip install streamlit pandas numpy scikit-learn joblib matplotlib seaborn ^
    python-docx openpyxl pyinstaller --quiet --upgrade
if errorlevel 1 (
    echo [ERROR] pip install failed.
    pause & exit /b 1
)
echo   [OK] Dependencies installed.

:: Check required files
echo.
echo   [2/3] Checking files...
if not exist metallurgy_advisor_pro.py (
    echo [ERROR] metallurgy_advisor_pro.py not found in current folder!
    pause & exit /b 1
)
if not exist launcher_pyinstaller.py (
    echo [ERROR] launcher_pyinstaller.py not found in current folder!
    pause & exit /b 1
)
if not exist metallurgy.spec (
    echo [ERROR] metallurgy.spec not found in current folder!
    pause & exit /b 1
)
echo   [OK] All files found.

:: Clean previous build
if exist build    rmdir /s /q build
if exist dist     rmdir /s /q dist

:: Build EXE
echo.
echo   [3/3] Building EXE (takes 3-5 minutes, please wait)...
python -m PyInstaller metallurgy.spec
if errorlevel 1 (
    echo [ERROR] PyInstaller failed. See output above.
    pause & exit /b 1
)

echo.
echo ============================================================
echo   SUCCESS!
echo   File: dist\MetallurgyAdvisorPro.exe (~210 MB)
echo.
echo   Double-click MetallurgyAdvisorPro.exe to run.
echo   Browser opens automatically after 3 seconds.
echo   If browser did not open - go to: http://localhost:8501
echo ============================================================
echo.
pause
