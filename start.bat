@echo off
setlocal

if "%~1"=="" (
  echo Usage: onelive.exe ^<path-to-script.py^>
  exit /b 1
)

onelive.exe %1
