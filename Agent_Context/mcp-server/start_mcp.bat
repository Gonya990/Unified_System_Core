@echo off
echo Starting Antigravity MCP Server...

:: Check for Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Node.js not found. Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

:: Install dependencies if not installed
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)

:: Build the project
echo Building project...
call npm run build

:: Start the server
echo MCP Server is running!
echo Transport: StdIO (Connect via Gemini Desktop / Claude Device Code)
call npm start

pause
