@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3 -c "import sys" >nul 2>&1
if not errorlevel 1 (
    py -3 model.py --variant 1
    echo.
    py -3 experiments.py --variant 1
) else (
    "C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1119-907-0_26.1119.907.0_x64__3k8sg7r9htsxt\dependencies\python\python.exe" model.py --variant 1
    echo.
    "C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1119-907-0_26.1119.907.0_x64__3k8sg7r9htsxt\dependencies\python\python.exe" experiments.py --variant 1
)
echo.
pause
