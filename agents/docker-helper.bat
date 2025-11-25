@echo off
REM Pharma Researcher Docker Helper Script for Windows
REM This script provides convenient commands for Docker operations

setlocal enabledelayedexpansion

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop.
    exit /b 1
)

REM Main command dispatcher
if "%1"=="" goto help
if "%1"=="build" goto build
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="logs" goto logs
if "%1"=="jupyter" goto jupyter
if "%1"=="shell" goto shell
if "%1"=="status" goto status
if "%1"=="backup" goto backup
if "%1"=="clean" goto clean
if "%1"=="help" goto help
goto unknown

:build
echo [INFO] Building Docker image...
docker-compose build
if errorlevel 1 (
    echo [ERROR] Build failed
    exit /b 1
)
echo [SUCCESS] Docker image built successfully
goto end

:start
echo [INFO] Starting pharma researcher...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Start failed
    exit /b 1
)
echo [SUCCESS] Application started
echo [INFO] View logs with: docker-helper.bat logs
goto end

:stop
echo [INFO] Stopping pharma researcher...
docker-compose down
echo [SUCCESS] Application stopped
goto end

:restart
echo [INFO] Restarting pharma researcher...
docker-compose restart
echo [SUCCESS] Application restarted
goto end

:logs
docker-compose logs -f pharma_researcher
goto end

:jupyter
echo [INFO] Starting with Jupyter Lab...
docker-compose --profile jupyter up -d
echo [SUCCESS] Jupyter Lab started at http://localhost:8888
goto end

:shell
echo [INFO] Opening shell in container...
docker-compose exec pharma_researcher /bin/bash
goto end

:status
docker-compose ps
echo.
docker stats --no-stream pharma_researcher 2>nul
if errorlevel 1 echo [INFO] Container not running
goto end

:backup
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set BACKUP_FILE=pharma_output_backup_%mydate%_%mytime%.zip
echo [INFO] Creating backup: %BACKUP_FILE%
powershell Compress-Archive -Path output -DestinationPath %BACKUP_FILE%
echo [SUCCESS] Backup created: %BACKUP_FILE%
goto end

:clean
echo [INFO] Cleaning up Docker resources...
docker-compose down --rmi all -v
echo [SUCCESS] Cleanup complete
goto end

:help
echo Pharma Researcher Docker Helper
echo.
echo Usage: docker-helper.bat [command]
echo.
echo Commands:
echo     build       Build the Docker image
echo     start       Start the application in background
echo     stop        Stop the application
echo     restart     Restart the application
echo     logs        View application logs (follow mode)
echo     jupyter     Start with Jupyter Lab
echo     shell       Open bash shell in container
echo     status      Show container status and resource usage
echo     backup      Backup output directory
echo     clean       Remove containers, images, and volumes
echo     help        Show this help message
echo.
echo Examples:
echo     docker-helper.bat build
echo     docker-helper.bat start
echo     docker-helper.bat logs
goto end

:unknown
echo [ERROR] Unknown command: %1
echo Run 'docker-helper.bat help' for usage information
exit /b 1

:end
endlocal
