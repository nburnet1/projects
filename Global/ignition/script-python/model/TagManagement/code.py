import com.inductiveautomation.ignition.common.model.values.BasicQualifiedValue
import java.util.Date
from copy import deepcopy
	
class TagStructure():
	STANDARDTAGDICT = {
		"memory" : [],
		"expr" : [],
		"derived" : [],
		"opc" : [],
		"reference" : [],
		"db" : []
	}

	def __init__(self, tagProvider, tagStructure, folders, tags, udts):
		self.tagStructure = tagStructure
		self.tagProvider = tagProvider
		self.folders = folders
		
		if len(tags) > 0:
			self.tags = tags
		else:
			self.tags = deepcopy(self.STANDARDTAGDICT)
		self.udts = udts
		
		self.handleMap = {
			"memory": {
				"format": lambda tagList: self.handleMemoryFormat(tagList),
				"checkList": lambda tagList: self.handleMemoryList(tagList),
				"readBlock": lambda tagList, readList: self.handleMemoryRead(tagList, readList),
				"compare" : lambda tag, otherTag: self.handleMemoryCompare(tag, otherTag),
				"structure": lambda currPath, tag:{
							"name" : currPath[1],
							"tagType": tag["tagType"],
							"value" : tag['value'],
							"dataType" : tag["dataType"],
							"valueSource" : tag["valueSource"],
						}
			},
			"expr": {
				"format": lambda tagList: self.handleDataType(tagList),
				"checkList": lambda tagList: self.handleExprList(tagList),
				"readBlock": lambda tagList, readList: self.handleExprRead(tagList, readList),
				"compare" : lambda tag, otherTag: self.handleExprCompare(tag, otherTag),
				"structure": lambda currPath, tag:{
							"name" : currPath[1],
							"tagType": tag["tagType"],
							"valueSource" : tag["valueSource"],
							'expression' : tag['expression'],
							"dataType" : tag['dataType'],
						}
			},
			"opc": {
				"format": lambda tagList: self.handleDataType(tagList),
				"checkList": lambda tagList: self.handleOPCList(tagList),
				"readBlock": lambda tagList, readList: self.handleOPCRead(tagList, readList),
				"compare" : lambda tag, otherTag: self.handleOPCCompare(tag, otherTag),
				"structure": lambda currPath, tag:{
							"name" : currPath[1],
							"tagType": tag["tagType"],
							"valueSource" : tag["valueSource"],
							"opcServer": tag["opcServer"],
							"opcItemPath": tag["opcItemPath"],
							"dataType" : tag["dataType"]
						}
			},
			"reference": {
				"format": lambda tagList: self.handleDataType(tagList),
				"checkList": lambda tagList: self.handleReferenceList(tagList),
				"readBlock": lambda tagList, readList: self.handleReferenceRead(tagList, readList),
				"compare" : lambda tag, otherTag: self.handleReferenceCompare(tag, otherTag),
				"structure": lambda currPath, tag:{
							"name" : currPath[1],
							"tagType": tag["tagType"],
							"valueSource" : tag["valueSource"],
							"sourceTagPath" : tag["sourceTagPath"],
							"dataType" : tag["dataType"]
						}
			},
			"derived": {
				"format": lambda tagList: self.handleDataType(tagList),
				"checkList": lambda tagList: self.handleDerivedList(tagList),
				"readBlock": lambda tagList, readList: self.handleDerivedRead(tagList, readList),
				"compare" : lambda tag, otherTag: self.handleDerivedCompare(tag, otherTag),
				"structure": lambda currPath, tag:{
							"name" : currPath[1],
							"tagType": tag["tagType"],
							"valueSource" : tag["valueSource"],
							"sourceTagPath" : tag["sourceTagPath"],
							"deriveExpressionGetter" : tag["deriveExpressionGetter"],
							"deriveExpressionSetter" : tag["deriveExpressionSetter"],
							"dataType" : tag["dataType"]
						}
			},
			"db": {
				"format": lambda tagList: self.handleDataType(tagList),
				"checkList": lambda tagList: self.handleDBList(tagList),
				"readBlock": lambda tagList, readList: self.handleDBRead(tagList, readList),
				"compare" : lambda tag, otherTag: self.handleDBCompare(tag, otherTag),
				"structure": lambda currPath, tag:{
							"name" : currPath[1],
							"tagType": tag["tagType"],
							"valueSource" : tag["valueSource"],
							"query" : tag["query"],
							"datasource": tag["datasource"],
							"dataType" : tag["dataType"]
						}
			}
		}

	def categorizeTags(self):
		for tag in self.tagStructure:
			if tag['tagType'] == 'Folder':
				self.folders.append(tag)
			elif tag['tagType'] == 'UdtInstance':
				self.udts.append(tag)
			else:
				self.tags[tag['valueSource']].append(tag)

	def commit(self, tagList, configureTag):
		configureList = []
		if len(tagList) > 0:
			basePath = self.splitPath(tagList[0]['fullPath'])
			for index, tag in enumerate(tagList):
				currPath = self.splitPath(tag['fullPath'])
				if currPath[0] != basePath[0]:
					system.tag.configure(basePath[0], configureList, "m")
					basePath = currPath
					configureList = []

				configureList.append(configureTag(currPath, tag))
				if index == len(tagList) - 1:
					system.tag.configure(basePath[0], configureList, "m")
					
	def commitTagStructure(self):
		# Folder Commit
		configureTag = lambda currPath, tag: {
			"name" : currPath[1],
			"tagType": tag["tagType"]
		}
		self.commit(self.folders,configureTag)
		
		# UDT Commit
		configureTag = lambda currPath, tag: {
			"name" : currPath[1],
			"tagType": tag["tagType"],
			"typeId": tag["typeId"],
			"parameters" : tag["parameters"] if "parameters" in tag else {}
		}
		self.commit(self.udts,configureTag)
		
		# Tag Commit
		for valueSource in self.tags:
			self.commit(self.tags[valueSource],self.handleMap[valueSource]['structure'])

	def compareTagPath(self, tagList, otherTagList):
		returnTag = []
		
		for tag in tagList:
			for otherTag in otherTagList:
#				print "newTag: %s \notherTag: %s" %(tag['fullPath'],otherTag['fullPath'])
#				print tag['fullPath'] == otherTag['fullPath']
				if tag['fullPath'] == otherTag['fullPath']:
					
					
					break
			else:
				returnTag.append(tag)
		
		return returnTag   

	def compareTagStructures(self, otherTagStructure):
		folders = []
		tags = {}
		udts = []
		
		folders = self.compareTagPath(self.folders, otherTagStructure.folders)
		tags = self.compareTagValues(otherTagStructure.tags)
		udts = self.compareUDTs(self.udts, otherTagStructure.udts)
		
		tempTagStructure = TagStructure(self.tagProvider, [], folders, tags, udts)
		tempTagStructure.setTagStructureFromLists()
		return tempTagStructure

	def compareTagValues(self, otherTagList):
		returnTagList = deepcopy(self.STANDARDTAGDICT)
		
		for valueSource in self.tags:
			for tag in self.tags[valueSource]:
				for otherTag in otherTagList[valueSource]:
					if tag['fullPath'] == otherTag['fullPath']:
						if self.handleMap[valueSource]['compare'](tag, otherTag) or tag['dataType'] != otherTag['dataType']:
							returnTagList[valueSource].append(tag)
						break
				else:
					returnTagList[valueSource].append(tag)
							
		return returnTagList
		
	def compareUDTs(self, tagList, otherTagList):
		returnTagList = []
		
		for tag in tagList:
			for otherTag in otherTagList:
				if tag['fullPath'] == otherTag['fullPath']:
					if tag['tagType'] != otherTag['tagType'] or tag['typeId'] != otherTag['typeId']:
						returnTagList.append(tag)
					break
			else:
				returnTagList.append(tag)
				
		return returnTagList

	def handleMemoryCompare(self, tag, otherTag):
		
		return tag['value'] != otherTag['value'] and tag['value'] is not None

	def handleExprCompare(self, tag, otherTag):    
		return tag['expression'] != otherTag['expression'] and tag['expression'] is not None

	def handleOPCCompare(self, tag, otherTag):
		return tag['opcServer'] != otherTag['opcServer'] or tag['opcItemPath'] != otherTag['opcItemPath'] 

	def handleDerivedCompare(self, tag, otherTag):
		return tag['sourceTagPath'] != otherTag['sourceTagPath'] or tag['deriveExpressionGetter'] != otherTag['deriveExpressionGetter'] \
		or tag['deriveExpressionSetter'] != otherTag['deriveExpressionSetter']

	def handleReferenceCompare(self, tag, otherTag):
		return tag['sourceTagPath'] != otherTag['sourceTagPath'] and tag['sourceTagPath'] is not None

	def handleDBCompare(self, tag, otherTag):
		return tag['query'] != otherTag['query'] or tag['datasource'] != otherTag['datasource']

	def handleMemoryFormat(self, tagList):
		for tag in tagList:
			tag['dataType'] = str(tag['dataType'])
			if 'value' not in tag:
				tag['value'] = None
			elif type(tag['value']) == com.inductiveautomation.ignition.common.model.values.BasicQualifiedValue:
				tag['value'] = str(tag['value'].value)
			else:
				tag['value'] = str(tag['value'])
		return tagList

	def handleDataType(self, tagList):
		for tag in tagList:
			tag['dataType'] = str(tag['dataType'])
			
		return tagList

	def handleDBRead(self, tagList, readList):
		tempList = [path + ".query" for path in readList]
		queryList = system.tag.readBlocking(tempList)
		tempList = [path + ".dataSource" for path in readList]
		dataSourceList = system.tag.readBlocking(tempList)
		
		for i in range(len(tagList)):
			tagList[i]['query'] = queryList[i].value
			tagList[i]['datasource'] = dataSourceList[i].value
			
		return tagList

	def handleDerivedRead(self, tagList, readList):
		tempList = [path + ".sourceTagPath" for path in readList]
		sourceList = system.tag.readBlocking(tempList)
		tempList = [path + ".deriveExpressionGetter" for path in readList]
		getterList = system.tag.readBlocking(tempList)
		tempList = [path + ".deriveExpressionSetter" for path in readList]
		setterList = system.tag.readBlocking(tempList)
		
		for i in range(len(tagList)):
			tagList[i]['sourceTagPath'] = sourceList[i].value
			tagList[i]['deriveExpressionGetter'] = getterList[i].value
			tagList[i]['deriveExpressionSetter'] = setterList[i].value
			
		return tagList

	def handleExprRead(self, tagList, readList):
		tempList = [path + ".expression" for path in readList]
		expressionList = system.tag.readBlocking(tempList)
		
		for i in range(len(tagList)):
			tagList[i]['expression'] = expressionList[i].value
			
		return tagList

	def handleMemoryRead(self, tagList, readList):
		return tagList

	def handleOPCRead(self, tagList, readList):
		tempList = [path + ".opcItemPath" for path in readList]
		itemList = system.tag.readBlocking(tempList)
		tempList = [path + ".opcServer" for path in readList]
		serverList = system.tag.readBlocking(tempList)
		
		for i in range(len(tagList)):
			tagList[i]['opcItemPath'] = itemList[i].value
			tagList[i]['opcServer'] = serverList[i].value
			
		return tagList

	def handleReferenceRead(self, tagList, readList):
		tempList = [path + ".sourceTagPath" for path in readList]
		sourceList = system.tag.readBlocking(tempList)
		
		for i in range(len(tagList)):
			tagList[i]['sourceTagPath'] = sourceList[i].value
			
		return tagList

	def handleDBList(self, tagList):
		return any('query' not in tag or 'datasource' not in tag for tag in tagList)
		
	def handleDerivedList(self, tagList):
		return any('sourceTagPath' not in tag or 'deriveExpressionGetter' not in tag or 'deriveExpressionSetter' not in tag for tag in tagList)
		
	def handleExprList(self, tagList):
		return any('expression' not in tag for tag in tagList)

	def handleMemoryList(self, tagList):
		return False

	def handleOPCList(self, tagList):
		return any('opcServer' not in tag or 'opcItemPath' not in tag for tag in tagList)
	 
	def handleReferenceList(self, tagList):
		return any('sourceTagPath' not in tag for tag in tagList)

	def printCategorized(self):
		print "Folders:"
		for folder in self.folders:
			print folder
		print 'UDTs:'
		for udt in self.udts:
			print udt
		print "Tags:"
		for tagSource in self.tags:
			print "Value Source: %s"  %tagSource
			for tag in self.tags[tagSource]:
				print tag

	def printTags(self):
		for tag in self.tagStructure:
			print(tag)

	def removeUDTTags(self):
		tempList = {tagSource: [tag for tag in tags if not any(self.splitPath(tag['fullPath'])[0] == udt['fullPath'] for udt in self.udts)] \
		for tagSource, tags in self.tags.items()}
		self.tags = tempList

	def setCompatibleTagValues(self):
		for valueSource in self.tags:
			if len(self.tags[valueSource]) != 0:
				needToRead = self.handleMap[valueSource]['checkList'](self.tags[valueSource])
				if needToRead:
					readList = [tag['fullPath'] for tag in self.tags[valueSource]]
					self.tags[valueSource] = self.handleMap[valueSource]['readBlock'](self.tags[valueSource], readList)
				
				self.tags[valueSource] = self.handleMap[valueSource]['format'](self.tags[valueSource])

	def setScrubbedTagStructure(self):
		self.tagStructure = [tag for tag in self.tagStructure if '_types_' not in tag['fullPath']]

	def setSortedTagStructure(self):
		# sorts data alphabetically by fullPath
		self.tagStructure = sorted(self.tagStructure, key=lambda k: k['fullPath'].lower())

	def setTagStructureFromLists(self):
		self.tagStructure = self.folders + self.udts + [tag for valueSource in self.tags.values() for tag in valueSource]

	def setToString(self):
		for tag in self.tagStructure:
			tag['fullPath'] = str(tag['fullPath'])
			tag['tagType'] = str(tag['tagType'])

	def splitPath(self, path):
		split =  path.rsplit("/",1)
		if len(split) != 2:
			split = path.split("]")
			split[0] += "]"
			
		return split

def generateTags(tagProvider, newTagStructure):
	newTagObj = TagStructure(tagProvider, newTagStructure, [], {}, [])
	currentTagStructure = system.tag.browse(tagProvider, filter={"recursive":True}).getResults()
	currentTagObj = TagStructure(tagProvider, currentTagStructure, [], {}, [])
	
	# Gathering new tag structure: Remove tag types-> sort list by fullPath -> organize list into three categories -> type cast certain tag values
	print "\n\t", "New Tag Structure"
	newTagObj.setScrubbedTagStructure()
	newTagObj.setSortedTagStructure()
	newTagObj.categorizeTags()
	newTagObj.setCompatibleTagValues()
	newTagObj.printCategorized()
	
	print "\n\t", "Current Tag Structure"
	currentTagObj.setToString()
	currentTagObj.setScrubbedTagStructure()
	currentTagObj.categorizeTags()
	currentTagObj.removeUDTTags()
	currentTagObj.setCompatibleTagValues()
	currentTagObj.printCategorized()
	
	print "\n\t", "Tags to create and alter"
	uniqueTagObj = newTagObj.compareTagStructures(currentTagObj)
	uniqueTagObj.printCategorized()
	
	print "\n\t", "Tags to delete"
	deleteFolderList = currentTagObj.compareTagPath(currentTagObj.folders, newTagObj.folders)
	deleteTagList = deepcopy(TagStructure.STANDARDTAGDICT)
	for valueSource in currentTagObj.tags:
		deleteTagList[valueSource] = currentTagObj.compareTagPath(currentTagObj.tags[valueSource], newTagObj.tags[valueSource])
	deleteUDTList = currentTagObj.compareUDTs(currentTagObj.udts, newTagObj.udts)
	# Structured lists and then created the object
	deleteTagObj = TagStructure(tagProvider, [], deleteFolderList, deleteTagList, deleteUDTList)
	deleteTagObj.setTagStructureFromLists()
	deleteTagObj.printCategorized()
	
#		# Delete
	if len(deleteTagObj.tagStructure) > 0:
		system.tag.deleteTags([tag['fullPath'] for tag in deleteTagObj.tagStructure])
		# Create/ Alter
	if len(uniqueTagObj.tagStructure) > 0:
		uniqueTagObj.commitTagStructure()

	
def callGenerateTags():
	tag_provider = "[Some_Tags]"
	new_tag_structure = browse.getNewTagStructure(tag_provider)
#	new_tag_structure = browse.getTestTagStructure(tag_provider)

	generateTags(tag_provider, new_tag_structure)