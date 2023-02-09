cd /D "%~dp0"
REM taskkill /IM chrome.exe /F
@echo Started: %date% %time%
".venv\Scripts\activate.bat" && python main.py -h