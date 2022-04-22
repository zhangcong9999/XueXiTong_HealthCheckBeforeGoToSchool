@echo off

@REM Set variable of the current directory path
set CurrentDir=%~dp0

@REM Set the varible of the task scheduler name to "HealthCheck"
set taskname="HealthCheck"

@REM Set the file path of the batch script to be run.
set RunClockinScript=%CurrentDir%RunClockin.bat

@REM Delete the existing task scheduler and create a new one named "HealCheck". It will run the script RunClockin.bat at 06:30:00 every morning.
schtasks /Delete /TN %taskname% /F
schtasks /create /tn %taskname% /tr %RunClockinScript% /sc daily /st 06:30:00 /F
pause
