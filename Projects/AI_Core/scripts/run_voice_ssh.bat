@echo off
REM Batch wrapper to run voice_assistant_local.py in test-file mode via SSH
REM Usage: run_voice_ssh.bat C:\path\to\test.wav [no-tts]
SET PROJECT_DIR=C:\Users\gonya\my-ai-project
cd /d %PROJECT_DIR%
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

set FILE=%1
if "%FILE%"=="" set FILE=%PROJECT_DIR%\test_input.wav
set NO_TTS=%2
set CMD=python voice_assistant_local.py --file "%FILE%"
if /I "%NO_TTS%"=="no-tts" set CMD=%CMD% --no-tts

echo Running: %CMD%
%CMD%
