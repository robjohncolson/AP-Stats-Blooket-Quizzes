@echo off
REM this script will reset the repo to the previous commit.
REM before resetting the repo, user will be asked if they are sure.
set /p confirm=Are you sure you want to reset the repo to the previous commit? (Y/N): 
if /i "%confirm%" neq "Y" (
    echo Operation cancelled.
    exit /b
)


git reset --hard HEAD~1
git clean -fd
