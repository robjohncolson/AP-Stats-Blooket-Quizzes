#!/bin/bash

#revert files to last commit
git reset --hard HEAD~1
#reset directory to last commit
git clean -fdn
#ask if user wants to continue
read -p "Do you want to continue? (y/n)" CONTINUE
if [ "$CONTINUE" != "y" ]; then
    exit 1
fi
#user git to clean the directory to last commit
git clean -fd


 




