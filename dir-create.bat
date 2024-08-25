@echo off
REM Create directories Ch1 through Ch26 in current directory
for %%F in {1..26} do (
    mkdir "Ch%%F"
    echo Created directory Ch%%F
)

echo All directories have been created.
