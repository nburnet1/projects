def getNewTagStructure(tagProvider):
    return[
            {
                'fullPath': '{}FolderToAdd'.format(tagProvider),
                'name': 'FolderToAdd',
                'tagType': 'Folder'
            },
            {
                'fullPath': '{}Hello'.format(tagProvider),
                'dataType': 'Int4',
                'name': 'Hello',
                'tagType': 'AtomicTag',
                'attributes': [],
                'valueSource': 'memory',
                'value': 654
            },
            {
            	'fullPath' : '{}fol1'.format(tagProvider),
            	'tagType': 'Folder'
            },
            {
                'fullPath': '{}newTypeInstance'.format(tagProvider),
                'name': 'newTypeInstance',
                'tagType': 'UdtInstance',
                'typeId': 'test_type',
            },
            {
                'fullPath': '{}Seed'.format(tagProvider),
                'name': 'Seed',
                'tagType': 'UdtInstance',
                'typeId': 'Seed',
            },
            {
                'fullPath': '{}test_num'.format(tagProvider),
                'dataType': 'Int4',
                'name': 'test_num',
                'tagType': 'AtomicTag',
                'attributes': [],
                'valueSource': 'memory',
                'value': 125
            },
            {
                'fullPath': '{}Testa'.format(tagProvider),
                'name': 'Testa',
                'tagType': 'Folder'
            },
            {
                'fullPath': '{}Testa/basicNum'.format(tagProvider),
                'dataType': 'Int4',
                'name': 'basicNum',
                'tagType': 'AtomicTag',
                'attributes': [],
                'valueSource': 'memory',
                'value': 1234
            },
            {
                'fullPath': '{}Testa/Hey Folder'.format(tagProvider),
                'name': 'Hey Folder',
                'tagType': 'Folder'
            },
            {
                'fullPath': '{}Testa/Testa_embedded'.format(tagProvider),
                'name': 'Testa_embedded',
                'tagType': 'Folder'
            },
            {
                'fullPath': '{}Testa/Testa_embedded/testString'.format(tagProvider),
                'dataType': 'String',
                'name': 'testString',
                'tagType': 'AtomicTag',
                'attributes': [],
                'valueSource': 'memory',
                'value': 'Hey I am a String'
            },
            {
                'fullPath': '{}Testa1'.format(tagProvider),
                'name': 'Testa1',
                'tagType': 'Folder'
            },
            {
            	'fullPath': '{}fol1/fol2'.format(tagProvider),
                'tagType' : 'Folder'                    
            },
            {
            	'fullPath': '{}fol1/aNewInstance'.format(tagProvider),
            	"tagType" : 'UdtInstance',
            	'typeId' : 'test_type',
            	'parameters' : {'testParameter': 17}
            },
            {
            	'fullPath' : "{}Testa1/thisATestUDT".format(tagProvider),
            	'tagType' : "UdtInstance",
            	'typeId' : "testUDTFolder/newUDTTag",
            	'parameters' : {'testParameter' : 1544}
            },
            {
            	'fullPath' : '{}expressionDude'.format(tagProvider),
            	'dataType' : 'DateTime',
            	'expression' : 'now(1000)',
            	'valueSource' : 'expr',
            	'tagType' : 'AtomicTag'
            },
            {
            	'fullPath' : '{}Testa1/someExpr'.format(tagProvider),
            	'dataType' : 'Int4',
            	'expression' : '64+65',
            	'valueSource' : 'expr',
            	'tagType' : 'AtomicTag'
            },
            {
            	'fullPath' : '{}aDataSet'.format(tagProvider),
            	'dataType' : 'DataSet',
            	'valueSource': 'memory',
            	'tagType' : 'AtomicTag'
            },
            {
            	'fullPath' : '{}express'.format(tagProvider),
            	'dataType' : 'Int4',
            	'expression': '5+5*5',
            	'valueSource' : 'expr',
            	'tagType' : 'AtomicTag',
            	'dataType': 'Int4'
            },
            {
            	'fullPath' : '{}someQuery'.format(tagProvider),
            	'query' : 'select * from tank; ',
            	'datasource' : 'Sample_SQLite_Database',
            	'tagType' : 'AtomicTag',
            	'valueSource' : 'db',
            	'dataType' : 'DataSet'
            },
            {
              "valueSource": "reference",
              "sourceTagPath": "[Sample_Tags]Ramp/Ramp1",
              "fullPath": "{}refTag".format(tagProvider),
              "tagType": "AtomicTag",
              'dataType': 'Int4'
            },
            {
              "valueSource": "opc",
              "opcItemPath": "ns=1;s=[Sample_Device]_Meta:Random/RandomInteger2",
              "fullPath": "{}opcTag".format(tagProvider),
              "tagType": "AtomicTag",
              "opcServer": "Ignition OPC UA Server",
              'dataType': 'Int4'
            },
            {
              "valueSource": "derived",
              "deriveExpressionGetter": "{source} + 10",
              "deriveExpressionSetter": "{value} - 20",
              "sourceTagPath": "[Sample_Tags]Ramp/Ramp1",
              "fullPath": "{}derivedTag".format(tagProvider),
              "tagType": "AtomicTag",
              'dataType': 'Int4'
            }
        ]
        
def getTestTagStructure(tagProvider):
	return[
		{
			'fullPath' : '{}BreadLine1/Run History Details'.format(tagProvider),
			'tagType' : 'Folder'
		},
		{
			'fullPath' : '{}BreadLine1'.format(tagProvider),
			'tagType' : 'Folder'
		},

		{
			"valueSource": "memory",
			"dataType": "DataSet",
			"fullPath": "{}BreadLine1/Run History Details/Data Every 4 Minutes".format(tagProvider),
			"tagType" : 'AtomicTag'
		},
		{
			"valueSource": "memory",
			"dataType": "DataSet",
			"fullPath": "{}BreadLine1/Run History Details/Data Every 24 Minutes".format(tagProvider),
			"tagType" : 'AtomicTag'
		},
		{
			"valueSource": "memory",
			"dataType": "DataSet",
			"fullPath": "{}BreadLine1/Run History Details/Data Every 1 Minutes".format(tagProvider),
			"tagType" : 'AtomicTag'
		},
		{
			"fullPath": "{}Timer Triggers".format(tagProvider),
			"typeId": "UDTs/Timer Triggers",
			"tagType": "UdtInstance",
		},
		
	]
        
        
def getCurrentTagStructure():
    return [
    {'fullPath': '[Some_Tags]_types_', 'hasChildren': True, 'name': '_types_', 'tagType': 'Folder'},
    {'fullPath': '[Some_Tags]_types_/Seed', 'hasChildren': True, 'name': 'Seed', 'tagType': 'UdtType', 'typeId': None, 'value': [None, 'Bad_Unsupported', 'Thu Jan 04 08:05:51 EST 2024 (1704373551482)']},
    {'fullPath': '[Some_Tags]_types_/Seed/GenerateTags', 'formatString': None, 'hasChildren': False, 'dataType': 'DateTime', 'name': 'GenerateTags', 'tagType': 'AtomicTag', 'attributes': ['scripting'], 'valueSource': 'expr', 'value': ['now()', 'Good', 'Thu Jan 04 12:56:36 EST 2024 (1704390996968)']},
    {'fullPath': '[Some_Tags]_types_/Seed/Test Tag', 'formatString': None, 'hasChildren': False, 'dataType': 'Int4', 'name': 'Test Tag', 'tagType': 'AtomicTag', 'attributes': [], 'valueSource': 'memory', 'value': [0, 'Good', 'Thu Jan 04 11:51:02 EST 2024 (1704387062917)']},
    {'fullPath': '[Some_Tags]Seed', 'hasChildren': True, 'name': 'Seed', 'tagType': 'UdtInstance', 'typeId': 'Seed', 'value': [None, 'Bad_Unsupported', 'Thu Jan 04 08:05:51 EST 2024 (1704373551482)']},
    {'fullPath': '[Some_Tags]Seed/GenerateTags', 'formatString': 'h:mm:ss', 'hasChildren': False, 'dataType': 'DateTime', 'name': 'GenerateTags', 'tagType': 'AtomicTag', 'attributes': ['scripting'], 'valueSource': 'expr', 'value': ['Thu Jan 04 12:56:33 EST 2024', 'Good', 'Thu Jan 04 12:56:33 EST 2024 (1704390993673)']},
    {'fullPath': '[Some_Tags]Testa1', 'hasChildren': False, 'name': 'Testa1', 'tagType': 'Folder'},
    {'fullPath': '[Some_Tags]Yoooo', 'hasChildren': False, 'name': 'Testa1', 'tagType': 'Folder'},
    {'fullPath': '[Some_Tags]DeleteUDT', 'hasChildren': True, 'name': 'getDeleted', 'tagType': 'UdtInstance', 'typeId': 'DeleteUDT', 'value': [None, 'Bad_Unsupported', 'Thu Jan 04 08:05:51 EST 2024 (1704373551482)']},
    {'fullPath': '[Some_Tags]Seed/Test Tag', 'formatString': '#,##0.##', 'hasChildren': False, 'dataType': 'Int4', 'name': 'Test Tag', 'tagType': 'AtomicTag', 'attributes': ['override'], 'valueSource': 'memory', 'value': [1600, 'Good', 'Thu Jan 04 12:56:36 EST 2024 (1704390996966)']},
    {'fullPath': '[Some_Tags]Seed/deleteMe', 'formatString': '#,##0.##', 'hasChildren': False, 'dataType': 'Int4', 'name': 'Test Tag', 'tagType': 'AtomicTag', 'attributes': ['override'], 'valueSource': 'memory', 'value': [1600, 'Good', 'Thu Jan 04 12:56:36 EST 2024 (1704390996966)']}
	]