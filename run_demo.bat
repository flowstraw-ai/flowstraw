@echo off
REM ===================================================
REM FlowStraw One-Click Demo Launcher (Windows)
REM ===================================================

SETLOCAL

REM Change this if your project is elsewhere
SET PROJECT_DIR=%~dp0

cd /d "%PROJECT_DIR%"

echo.
echo ================================
echo   FlowStraw Demo Launcher
echo ================================
echo.

REM ---- Activate venv if present ----
IF EXIST "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) ELSE (
    echo [WARN] No venv found. You can create one with:
    echo        python -m venv venv
    echo        venv\Scripts\activate
    echo.
)

REM ---- Run the demo menu ----
python flowstraw_demo.py

echo.
echo [DONE] Exiting launcher.
echo.
PAUSE
ENDLOCAL
