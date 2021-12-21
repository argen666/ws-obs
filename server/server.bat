@echo off
"C:\Python39\python.exe" sanik.py %*
:: if the exit code is >= 1, then pause
if errorlevel 1 pause
