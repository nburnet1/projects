cd /usr/local/bin/ignition/data/projects/$1
# Args:
# project name
git status . > /usr/local/bin/ignition/data/projects/$1/git.log
