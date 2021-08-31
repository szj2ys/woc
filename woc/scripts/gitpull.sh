#!/bin/bash



# get git hash for commit message
#GITHASH=$(git rev-parse HEAD)
DATE=$(date +"%Y-%m-%d %H:%M:%S")
MSG="$DATE"
yapf -irp .

#git rm -r --cache .
# add commit, and push to github
git add . --all
git commit -m "$MSG"
git push

