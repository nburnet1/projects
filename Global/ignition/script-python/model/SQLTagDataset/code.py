import com.inductiveautomation.ignition.common.BasicDataset
import com.inductiveautomation.ignition.common.model.values.BasicQualifiedValue
import java.util.ArrayList
import java.sql.Date
import java.sql.Timestamp
import re 

class SQLTagDataset():
	"""This class will provide quick CRUD capabilites between Tag Datasets and SQL tables.

	Attributes:
		tag (dataset): The contents of a dataset tag (Not the tag path).
		database (str): The database that contains the table that will be manipulated
		tableName (str): The name of the table that will be accessed
		insertIdentity (bool): whether INSERT_IDENTITY will be set to on. Useful for manually setting primary keys
	"""
	def __init__(self, tag, database, tableName, insertIdentity=False):
		self.tag = self._sanitizeTag(tag)
		self.database = self._sanitizeData(database)
		self.tableName = self._sanitizeData(tableName)
		self.insertIdentity = insertIdentity

	def _sanitizeData(self, text):
		"""This private method is ran to ensure that SQLI is prevented

		Parameters:
			text (str): the value that will be compared against the regular expression
		"""
		pattern = r'[\'";\\%;<>&|\(\){}^]'
		return re.sub(pattern, '', text)
		
	def _sanitizeTag(self, tag):
		"""This checks some possible types that could be unintentionally passed
		"""
		if type(tag) == java.util.ArrayList:	
			return system.dataset.toPyDataSet(tag[0].value)
		elif type(tag) == com.inductiveautomation.ignition.common.model.values.BasicQualifiedValue:
			return system.dataset.toPyDataSet(tag.value)
		elif type(tag) == com.inductiveautomation.ignition.common.BasicDataset:
			return system.dataset.toPyDataSet(tag)

	def _getColumnString(self, parenthesis):
		"""Utility that generates the column strings for CRUD statements

		Parameters:
			parenthesis (bool): boolean value that indicates whether to include parenthesis or not. (True for inserts, False for select)
		"""
		columnNames = list(self.tag.getColumnNames())
		columnString = "(" if parenthesis else ""
		for columnName in columnNames:
			columnName = self._sanitizeData(columnName)
			columnString += (columnName + ", ") if " " not in columnName else ("["+columnName+"], ")
			
		columnString = columnString[:-2]
		columnString += ") " if parenthesis else " "

		return columnString

	def _isDate(self, value):
		"""Checks to see if the value is of a type date
		"""
		return type(value) == java.util.Date or type(value) == java.sql.Date or type(value) == java.sql.Timestamp
	def _setDate(self, date):
		return system.date.setTime(date, date.getHours(), date.getMinutes(), 0)

	def audit(self, auditColumn, auditDs):
		"""Allows auditing to be performed when values are changed. This will by default update the current time in the specified column.

			Ad hoc method that gives some auditing capabilities. Use auditing at db level if possible.
   
		Parameters:
			auditColumn (str): the column where the time will be inserted into.
			auditDs (dataset): contains the data that was generated from an update. Can get this from self.update
		"""
		auditColumn = self._sanitizeData(auditColumn)
		txId = system.db.beginTransaction(timeout = 5000, database=self.database)
		updateString = ""
		args = []
		conditionalColumn = auditDs.getColumnName(0)
		
		
		for row in range(auditDs.getRowCount()):
			tempString = "UPDATE " + self.tableName + " SET "
			tempString += auditColumn + " = ? WHERE " + conditionalColumn + "= ?;\n"
			updateString += tempString
			args.append(system.date.now())
			args.append(auditDs.getValueAt(row, conditionalColumn))

		system.db.runPrepUpdate(updateString, args, self.database, txId)
		system.db.commitTransaction(txId)
		system.db.closeTransaction(txId)
		
		
		
		
	def destructiveInsert(self):
		"""Drops entire table and inserts the dataset. Be sure to check insertIdentity var depending on dataset.

			This method will fail if the table is being referenced by a FK constraint
		"""
		txId = system.db.beginTransaction(timeout=5000, database=self.database)

		# The destructive part of the method will not work if referenced by FK
		insertString = "TRUNCATE TABLE " + self.tableName + ";\n"
		
		args = []
		insertString += "SET IDENTITY_INSERT " + self.tableName + " ON;\n" if self.insertIdentity else ""
		
		for row in range(self.tag.getRowCount()):
			tempString = "INSERT INTO " + self.tableName + " " +self._getColumnString(True) + "VALUES ("

			for col in self.tag.getColumnNames():
				tempString += "?, "
				args.append(self.tag.getValueAt(row,col))

			tempString = tempString [:-2] + ");\n"

			insertString += tempString

		insertString += "SET IDENTITY_INSERT " + self.tableName + " OFF;\n" if self.insertIdentity else ""

		system.db.runPrepUpdate(insertString, args, self.database, txId)
		system.db.commitTransaction(txId)
		system.db.closeTransaction(txId)

	def safeInsert(self, conditionalColumn):
		"""Inserts into table only if it does not exist within the given conditional
  
		Parameters:
			conditionalColumn (str): This is the column that will check to see if the row already exists
		"""
		txId = system.db.beginTransaction(timeout=5000, database=self.database)
		conditionalColumn = self._sanitizeData(conditionalColumn)

		insertString = ""
		args = []
		insertString += "SET IDENTITY_INSERT " + self.tableName + " ON;\n" if self.insertIdentity else ""
		for row in range(self.tag.getRowCount()):
			existString = "IF NOT EXISTS (SELECT 1 FROM " + self.tableName + " WHERE " + conditionalColumn + " = ?)\n"
			args.append(self.tag.getValueAt(row,conditionalColumn))
			tempString = "BEGIN\n\tINSERT INTO " + self.tableName + " " +self._getColumnString(True) + "VALUES ("

			for col in self.tag.getColumnNames():
				tempString += "?, "
				args.append(self.tag.getValueAt(row,col))

			tempString = tempString [:-2] + ")\nEND\n"

			insertString += existString + tempString

		insertString += "SET IDENTITY_INSERT " + self.tableName + " OFF;\n" if self.insertIdentity else ""

		
		system.db.runPrepUpdate(insertString, args, self.database, txId)
		system.db.commitTransaction(txId)
		system.db.closeTransaction(txId)
	
	def select(self, selectConditional=""):
		"""A query that has an optional conditional and returns a dataset. Can be used for comparison

		Parameters:
			selectConditional (str): the select conditional is what will be used to gather and compare data (Could be a PK, FK, etc)
		"""
		txId = system.db.beginTransaction(timeout=5000, database=self.database)

		columnString = self._getColumnString(parenthesis=False)
		selectConditional = self._sanitizeData(selectConditional)

		queryString = "SELECT " + columnString+ "FROM " + self.tableName
		queryString += " WHERE " + selectConditional if selectConditional else ""
		queryString += ";"

		queryDs = system.db.runPrepQuery(queryString, [], database=self.database, tx=txId)

		system.db.commitTransaction(txId)
		system.db.closeTransaction(txId)

		return queryDs

	def update(self, conditionalColumn, selectConditional=""):
		"""This method will be used to update the table when inserts are not needed.
  
		Parameters:
		    conditionalColumn (str): the column that will be used as a means of comparing
			selectConditional (str): Used to call select method. Doing this to encapsulate the return select value
		"""
		conditionalColumn = self._sanitizeData(conditionalColumn)
		returnList = []
		queryDs = self.select(selectConditional)
		
		txId = system.db.beginTransaction(timeout=5000, database=self.database)
		
		updateString = ""
		args = []

		# These will get lists of the values based on the conditionalColumn
		queryConditionalList = queryDs.getColumnAsList(queryDs.getColumnIndex(conditionalColumn))
		tagConditionalList = self.tag.getColumnAsList(self.tag.getColumnIndex(conditionalColumn))
		
		for index, datum in enumerate(tagConditionalList):
			for queryIndex, queryDatum in enumerate(queryConditionalList):
				if datum == queryDatum:
					# Prepare update
					tempUpdate = "UPDATE " + self.tableName + " SET "
					changeFound = False
					# Gathers the values from the index that matched
					for columnHeader in self.tag.getColumnNames():
						# Checks to see if values match if not, update
						tagValue = self.tag.getValueAt(index, columnHeader)
						queryValue = queryDs.getValueAt(queryIndex, columnHeader)
						#Performs date check due to nanoseconds being recorded
						if self._isDate(tagValue) and self._isDate(queryValue):
							tagValue = self._setDate(tagValue)
							queryValue = self._setDate(queryValue)
						
						if tagValue != queryValue:
							tempUpdate += (columnHeader + " ") if " " not in columnHeader else ("["+columnHeader+"] ")
							tempUpdate += "= " + "?, "
							args.append(tagValue)
							changeFound = True
				
					# If changes are found, add WHERE clause
					if changeFound:

						returnList.append([self.tag.getValueAt(index, conditionalColumn)])
						
						tempUpdate = tempUpdate[:-2] 
						tempUpdate += " WHERE " + conditionalColumn + " = ?"
						args.append(datum)
						updateString += tempUpdate + ";\n"
					else:
						updateString += ""
					
		# If zero, then means that nothing needs to be updated
		if len(updateString) != 0:
			system.db.runPrepUpdate(updateString, args, self.database, txId)

		system.db.commitTransaction(txId)
		system.db.closeTransaction(txId)

		return system.dataset.toPyDataSet(system.dataset.toDataSet([conditionalColumn], returnList))
				