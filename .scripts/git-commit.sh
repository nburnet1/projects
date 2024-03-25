cd /usr/local/bin/ignition/data/projects
NOW=$(date +"%m-%d-%Y %H:%M:%S")
commitMessage="$1" || commitMessage="Designer save @ $NOW"
git commit -m "$commitMessage" &> git.log
