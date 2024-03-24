from __future__ import with_statement
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
	try:
		system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-status.sh", projectName])
	except Exception, e:
		print "Could not excecute git status", e
	
def getLog(projectName):
	import os
	
	logPath = "/usr/local/bin/ignition/data/projects/"+ (projectName if projectName != '.' else projectName) +"/git.log"
	logString = "log at " + logPath + " does not exist. Please try to perform an operation."
	
	if os.path.exists(logPath):
		try:
			with open(logPath, "r") as log:
				logString = log.read()
		except Exception, e:
			print "Error opening file:", e 
			
			
	return logString
	

def getProjectNames():
	import os
	projectDir = "/usr/local/bin/ignition/data/projects/"
	return os.listDir(projectDir)
	
def setTagRepo():
	from copy import deepcopy
#	projects = getProjectNames()
	
	gitSchema = {
		"name" : "root",
		"tagType" : "UdtInstance",
		"typeId" : "GitCommands",
		"parameters" : {
			"projectName" : "."
			}
	}
	
	system.tag.configure("[git]", gitSchema, "o")
	


def importTags():
	import os 
	#system.util.execute(["/usr/local/bin/ignition/data/projects/.scripts/git-startup-restore.sh"])
	
	projectDir = "/usr/local/bin/ignition/data/projects/.tags"
	
	tagDirs = os.listdir(projectDir)
	
	for tagProvider in tagDirs:
		filePath = projectDir + "/"+ tagProvider + "/tags.json"
		system.tag.importTags(filePath,"["+tagProvider+"]", "o")