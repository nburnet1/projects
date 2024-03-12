import com.inductiveautomation.ignition.common.BasicDataset
import com.inductiveautomation.ignition.common.model.values.BasicQualifiedValue
import java.util.ArrayList
import re

def sanitizeData(text):	
	pattern = r'[\'";\\%;<>&|\(\)\[\]{}^]'
	return re.sub(pattern, '', text)


def tagToSQLTable(tag, database, tableName, insertIdentity):
	# Be sure to pass the tag itself, not the tag path. 
	if type(tag) == java.util.ArrayList:	
		tag = tag[0].value
		tag = system.dataset.toPyDataSet(tag)
	elif type(tag) == com.inductiveautomation.ignition.common.model.values.BasicQualifiedValue:
		tag = system.dataset.toPyDataSet(tag.value)
	elif type(tag) == com.inductiveautomation.ignition.common.BasicDataset:
		tag = system.dataset.toPyDataSet(tag)
		
	if database == None:
		database = ""
			
	tableName = sanitizeData(tableName)
	
	txId = system.db.beginTransaction(timeout=5000, database=database)
	
	system.db.runUpdateQuery("TRUNCATE TABLE " + tableName, database=database, tx=txId)
	columnNames = list(tag.getColumnNames())
	columnString = "("
	for columnName in columnNames:
		columnName = sanitizeData(columnName)
		columnString += (columnName + ", ") if " " not in columnName else ("["+columnName+"], ")
		
	columnString = columnString[:-2]
	columnString += ") "
	
	statement = "INSERT INTO " + tableName + " " + columnString
	
	if insertIdentity:
			system.db.runUpdateQuery("SET IDENTITY_INSERT " + tableName + " ON;", database=database, tx=txId)
	
	for row in range(tag.getRowCount()):
		values = "VALUES ("
		argList = []
		for col in columnNames:
			tagValue = tag.getValueAt(row,col)
			argList.append(tagValue)
			values += "?, "
		
		values = values[:-2]
		values += ");"
		values = statement + values	

		system.db.runPrepUpdate(values, argList, database=database, tx=txId)


	if insertIdentity:	
			system.db.runUpdateQuery("SET IDENTITY_INSERT " + tableName + " OFF;", database=database, tx=txId)
			
				
	
	system.db.commitTransaction(txId)
	system.db.closeTransaction(txId)
	
def SQLTableToDataSetTag(dataSet, fullPath):
	return system.tag.write(fullPath, dataSet)
	
	
def prettyPrintPyDataSet(result):
	column_widths = []
	for col in range(result.getColumnCount()):
	    max_width = max(len(result.getColumnName(col)), max(len(str(result.getValueAt(row, col))) for row in range(result.getRowCount())))
	    column_widths.append(max_width)
	
	# Print the column headers
	for col in range(result.getColumnCount()):
	    print "{:<{width}}".format(result.getColumnName(col), width=column_widths[col] + 2),
	print
	
	# Print the rows
	for row in range(result.getRowCount()):
	    for col in range(result.getColumnCount()):
	        print "{:<{width}}".format(result.getValueAt(row, col), width=column_widths[col] + 2),
	    print
	    