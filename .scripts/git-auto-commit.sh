cd /usr/local/bin/ignition/data/projects
NOW=$(date +"%m-%d-%Y %H:%M:%S")
git add .
git commit -m "Designer save @ $NOW"
git push
