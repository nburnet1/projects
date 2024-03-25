cd /usr/local/bin/ignition/data/projects
git branch | grep \* | awk '{print $2}' > git.log
