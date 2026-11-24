@echo off
cd /d "%~dp0"
py -3 -c "import tkinter" >nul 2>&1
if not errorlevel 1 (
    py -3 main.py
    exit /b
)
set "TCL_LIBRARY=%~dp0runtime_tcl\tcl8.6"
set "TK_LIBRARY=%~dp0runtime_tcl\tk8.6"
"C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1119-907-0_26.1119.907.0_x64__3k8sg7r9htsxt\dependencies\python\python.exe" main.py
if errorlevel 1 pause
