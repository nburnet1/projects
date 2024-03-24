from __future__ import with_statement
import os
from copy import deepcopy

def commit():
	import system
	import time
	
	tagProviders= system.db.runPrepQuery("Select NAME from TAGPROVIDERSETTINGS WHERE NAME != 'default'",database="IgnitionInternal")
	tagProviders = [tagProviders[row]['NAME'] for row in range(len(tagProviders))]
	
	for tp in tagProviders:
		filePath = "/usr/local/bin/ignition/data/projects/.tags/"+tp+"/tags.json"
		tags = system.tag.exportTags(filePath=filePath, tagPaths=["["+tp+"]"], recursive=True)
	time.sleep(5)
	system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-auto-commit.sh"])

def add():
	pass

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
	versionedDirList = os.listDir(projectDir)
	
	if ".git" in versionedDirList:
		versionedDirList.remove(".git")
		
	return versionedDirList
	
def setTagRepo():
	dirs = getVersionedDirectories()

	
	gitSchema = {
		"name" : "root",
		"tagType" : "UdtInstance",
		"typeId" : "GitCommands",
		"parameters" : {
			"projectName" : "."
			}
	}
	gitProjectList = []
	
	
	# Adds the root directory to the tag space 
	gitProjectList.append(deepcopy(gitSchema))
	

	for folder in dirs:
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