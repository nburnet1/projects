import openpyxl
import shutil
import os

def generateTagSpaceFromTable(pathToFile, sheet, tagProvider):
	tempPath = "IODB_TEMP." + pathToFile.rsplit(".")[1]
	shutil.copyfile(pathToFile, tempPath)
	
	wb = openpyxl.load_workbook(tempPath)
	if sheet == None:
		st = wb.get_active_sheet()
	else:
		st = wb.get_sheet_by_name(sheet)
	
	tagSchema = []
	fullPaths = []
	for row in st.rows:
		tag = {}
		path = tagProvider
		for col in row[:-1]:
			col.value = col.value.strip()
			path += ("/" if path[-1] != "]" else "") + col.value
			if path not in fullPaths:
				fullPaths.append(path)
				tagSchema.append({
					"fullPath" : path,
					"tagType" : "Folder"
				})
		value = row[-1].value.strip()
		loweredValue = value.lower()
		if loweredValue == "analog":
			typeId = "Analog PV"
		elif loweredValue == "bool":
			typeId = "Bool PV"
		elif loweredValue == "string":
			typeId = "String PV"
		path += "/" + value
		if path not in fullPaths:
			fullPaths.append(path)
			tagSchema.append({
				"fullPath" : path,
				"tagType" : "UdtInstance",
				"typeId" :  typeId,
			})
	wb.save(tempPath)
	TagManagement.generateTags(tagProvider, tagSchema)
			
		
			
	
	
	
	
	
	
	
