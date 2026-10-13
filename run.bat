@echo off
rem ============================================================
rem  Local AI problem-generating and judging platform
rem  NOTE: keep this file pure ASCII. cmd.exe parses .bat with the
rem  system codepage (GBK on zh-CN Windows); non-ASCII bytes here
rem  would corrupt the script structure.
rem
rem  All real logic lives in run.py (auto-open browser, port-in-use
rem  fallback, error reporting). This file is only the entry point.
rem ============================================================
setlocal
cd /d "%~dp0"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1

set PY=D:\Pythontools\Python\python.exe
if not exist "%PY%" (
    echo [ERROR] Interpreter not found: %PY%
    echo         Edit run.bat and point PY to your python.exe
    pause
    exit /b 1
)

"%PY%" -X utf8 "%~dp0run.py"
set RC=%ERRORLEVEL%

endlocal & exit /b %RC%
