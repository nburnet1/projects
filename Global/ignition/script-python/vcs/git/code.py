from __future__ import with_statement
import os
from copy import deepcopy
import system
import time

PROJECT_PATH = "/usr/local/bin/ignition/data/projects/"

def commit():

	tagProviders= system.db.runPrepQuery("Select NAME from TAGPROVIDERSETTINGS WHERE NAME != 'default'",database="IgnitionInternal")
	tagProviders = [tagProviders[row]['NAME'] for row in range(len(tagProviders))]
	for tp in tagProviders:
		filePath = "/usr/local/bin/ignition/data/projects/.tags/"+tp+"/tags.json"
		tags = system.tag.exportTags(filePath=filePath, tagPaths=["["+tp+"]"], recursive=True)
	time.sleep(5)
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-auto-commit.sh"])
	
def commitTest(commitMessage):
	"""Commits the the changes staged at root of the repo
		
		Shell equivalent:
			git commit -m "$commitMessage"
			
	"""
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-commit.sh", commitMessage])

def add(projectName):
	"""Stages the changes made within a given folder
	
		Shell equivalent:
			git add $projectName
	"""
	
	# This indicates a reserved project name called '.tags.' Will export tags to be versioned
	if projectName == ".tags":
		exportTags()
		
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-add.sh", projectName])

def branch():
	"""Gets the branch of the repo.
	
		Shell equivalent:
			git branch
	"""
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-branch.sh"])
	
def push():
	"""Pushes the changes to the repo
		
		Shell equivalent:
			git push
	"""
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-push.sh"])

def status(projectName):
	"""Gets the status of the repo. Shows changes, stages, commits.
	
		Shell equivalent:
			git status $projectName
	"""
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-status.sh", projectName])

	
def getLog(projectName):
	"""Attempts to open a file that shows general logging.
	"""
	
	logPath = "/usr/local/bin/ignition/data/projects/" + projectName + "/git.log"
	logString = "log at " + logPath + " does not exist. Please try to perform an operation."
	
	if os.path.exists(logPath):
		try:
			with open(logPath, "r") as log:
				logString = log.read()
		except Exception, e:
			print "Error opening file:", e 
			
	return logString
	
def getCommitLog():
	"""Gets the output of git log 
	"""
	logPath = "/usr/local/bin/ignition/data/projects/commit.log"
	logString = "commit log at " + logPath + " does not exist. Please perform the corresponding operation to get commit history."
	
	if os.path.exists(logPath):
		try:
			with open(logPath, "r") as log:
				logString = log.read()
		except Exception, e:
			print "Error opening file:", e 
			
	return logString

def setCommitLog():
	"""Runs the shell script that activates git log and stores in commit.log
	
		Shell Equivalent:
			git log --pretty --graph
			
	"""
	# stores git log output into stand alone file
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-log.sh"])
	

def getVersionedDirectories():
	"""This will get directories that are 'versionable'
	"""
	versionDirPath = "/usr/local/bin/ignition/data/projects/"
	versionedDirList = os.listdir(versionDirPath)
	
	elementsToRemove = [".git",".resources", ".gitignore", "conversion-report.txt"]
	for element in elementsToRemove:
		if element in versionedDirList:
			versionedDirList.remove(element)
		
	return versionedDirList
	
def setTagRepo():
	dirs = getVersionedDirectories()
	gitProjectList = []
	
	# rootSchema allows us to commit and push our changes
	rootSchema = {
		"name" : "__root__",
		"tagType" : "UdtInstance",
		"typeId" : "RootCommands",
		"parameters" : {
			"projectName" : "."
			}
	}
	gitProjectList.append(rootSchema)
	
	gitSchema = {
		"name" : "",
		"tagType" : "UdtInstance",
		"typeId" : "GitCommands",
		"parameters" : {
			"projectName" : ""
			}
	}
	
	# Checks for hidden folders and applies specific logic
	dirsVisible = []
	for folder in dirs:
		if "." in folder:
			tempSchema = deepcopy(gitSchema)
			tempSchema["name"] = folder[1:]
			tempSchema["parameters"]["projectName"] = folder
			gitProjectList.append(tempSchema)
		else:
			dirsVisible.append(folder)
			
	# Gets the left overs from the past for loop check
	for folder in dirsVisible:
		tempSchema = deepcopy(gitSchema)
		tempSchema["name"] = folder
		tempSchema["parameters"]["projectName"] = folder
		gitProjectList.append(tempSchema)
	
	system.tag.configure("[git]", gitProjectList, "o")
	
def exportTags():
	tagProviders= system.db.runPrepQuery("Select NAME from TAGPROVIDERSETTINGS WHERE NAME != 'default'",database="IgnitionInternal")
	tagProviders = [tagProviders[row]['NAME'] for row in range(len(tagProviders))]
	for tp in tagProviders:
		filePath = "/usr/local/bin/ignition/data/projects/.tags/"+tp+"/tags.json"
		tags = system.tag.exportTags(filePath=filePath, tagPaths=["["+tp+"]"], recursive=True)

def importTags():
	#system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-startup-restore.sh"])
	
	projectDir = "/usr/local/bin/ignition/data/projects/.tags"
	
	tagDirs = os.listdir(projectDir)
	
	for tagProvider in tagDirs:
		filePath = projectDir + "/"+ tagProvider + "/tags.json"
		system.tag.importTags(filePath,"["+tagProvider+"]", "o")