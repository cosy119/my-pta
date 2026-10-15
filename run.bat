@echo off
rem ============================================================
rem  Local AI problem-generating and judging platform
rem  NOTE: keep this file pure ASCII. cmd.exe parses .bat with the
rem  system codepage (GBK on zh-CN Windows); non-ASCII bytes here
rem  would corrupt the script structure.
rem
rem  Find Python 3.13, check dependencies, then start run.py.
rem ============================================================
setlocal
cd /d "%~dp0"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PYTHONDONTWRITEBYTECODE=1

set "PY_CMD="
set "PY_ARGS="

rem Prefer the Windows Python launcher, which finds Python even when it is not on PATH.
call py -3.13 -c "import sys" 1>nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py"
    set "PY_ARGS=-3.13"
)

rem Also support installations that put Python 3.13 on PATH without the launcher.
if not defined PY_CMD (
    call python -c "import sys; sys.exit(sys.version_info[:2] != (3, 13))" 1>nul 2>&1
    if not errorlevel 1 set "PY_CMD=python"
)

if not defined PY_CMD (
    echo [ERROR] Python 3.13 was not found.
    echo         Install Python 3.13 from python.org and run this file again.
    echo         Make sure the Python launcher or python.exe is on PATH.
    pause
    endlocal & exit /b 1
)

call %PY_CMD% %PY_ARGS% -c "import fastapi, uvicorn, httpx, pydantic, yaml, dotenv, openai" 1>nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python dependencies are missing.
    echo         Install them with:
    echo         %PY_CMD% %PY_ARGS% -m pip install -r "%~dp0requirements.txt"
    pause
    endlocal & exit /b 1
)

call %PY_CMD% %PY_ARGS% -X utf8 "%~dp0run.py"
set RC=%ERRORLEVEL%

endlocal & exit /b %RC%
