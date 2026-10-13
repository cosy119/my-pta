@echo off
rem ============================================================
rem  Stop the local platform: kill whatever is LISTENING on PORT.
rem  Keep this file pure ASCII (cmd.exe parses .bat as the system
rem  codepage, i.e. GBK on zh-CN Windows).
rem ============================================================
setlocal EnableExtensions
cd /d "%~dp0"

set PORT=8765
set FOUND=

echo Looking for a listener on 127.0.0.1:%PORT% ...
for /f "tokens=5" %%P in ('netstat -ano ^| findstr /R /C:"127.0.0.1:%PORT% .*LISTENING"') do (
    echo   Killing PID %%P ...
    taskkill /F /T /PID %%P 1>nul 2>&1
    set FOUND=1
)

if defined FOUND (
    echo Stopped. Port %PORT% is now free.
) else (
    echo Nothing was listening on port %PORT%. Nothing to do.
)

pause
endlocal
