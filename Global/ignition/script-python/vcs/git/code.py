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

def add():
	pass

def branch():
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-branch.sh"])

def push():
	pass

def status(projectName):
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-status.sh", projectName])

	
def getLog(projectName):
	
	logPath = "/usr/local/bin/ignition/data/projects/" + projectName + "/git.log"
	logString = "log at " + logPath + " does not exist. Please try to perform an operation."
	
	if os.path.exists(logPath):
		try:
			with open(logPath, "r") as log:
				logString = log.read()
		except Exception, e:
			print "Error opening file:", e 
			
			
	return logString
	

def getVersionedDirectories():
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
	


def importTags():
	#system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-startup-restore.sh"])
	
	projectDir = "/usr/local/bin/ignition/data/projects/.tags"
	
	tagDirs = os.listdir(projectDir)
	
	for tagProvider in tagDirs:
		filePath = projectDir + "/"+ tagProvider + "/tags.json"
		system.tag.importTags(filePath,"["+tagProvider+"]", "o")