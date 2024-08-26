@echo off
rem git cycle

rem batch file to automate git add .; git commit; git push
rem necessary because i borked paths
rem gonna define path to git.exe and then use that to run the command

set git_path=C:\Users\ColsonR\AppData\Local\Programs\Git\bin\git.exe

%git_path% add .
%git_path% commit
%git_path% push

pause
