#! /bin/bash

COMMIT_MSG=$(git diff HEAD HEAD~1 --stat | sed 's/^ //g' | sed 's/ | /: /g' | sed 's/ [+-]*$//g' | sed ':a;N;$!ba;s/\n/, /g')
#show user commit message
echo "Commit message: $COMMIT_MSG"
#ask user if they want to continue
read -p "Do you want to continue? (y/n)" CONTINUE
if [ "$CONTINUE" != "y" ]; then
    exit 1
fi
git commit -m "$COMMIT_MSG"

