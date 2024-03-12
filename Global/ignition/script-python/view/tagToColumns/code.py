from copy import deepcopy
schema = {
	"field": "",
	"visible": True,
	"editable": True,
	"render": "auto",
	"justify": "auto",
	"align": "center",
	"resizable": True,
	"sortable": False,
	"sort": "none",
	"filter": {
			"enabled": False,
			"visible": "on-hover",
			"string": {
				"condition": "",
				"value": ""
			},
		"number": {
				"condition": "",
				"value": ""
		},
		"boolean": {
				"condition": ""
		},
		"date": {
				"condition": "",
				"value": ""
		}
	},
	"viewPath": "",
	"viewParams": {},
	"boolean": "checkbox",
	"number": "value",
	"progressBar": {
		"max": 100,
		"min": 0,
		"bar": {
				"color": "",
				"style": {
					"classes": ""
				}
		},
		"track": {
			"color": "",
			"style": {
				"classes": ""
			}
		},
		"value": {
			"enabled": True,
			"format": "0,0.##",
			"justify": "center",
			"style": {
				"classes": ""
			}
		}
	},
	"toggleSwitch": {
		"color": {
			"selected": "",
			"unselected": ""
		}
	},
	"nullFormat": {
		"includeNullStrings": False,
		"strict": False,
		"nullFormatValue": ""
	},
	"numberFormat": "0,0.##",
	"dateFormat": "HH:mm MM/DD/YY",
	"width": "",
	"strictWidth": False,
	"header": {
		"title": "",
		"justify": "left",
		"align": "center",
		"style": {
			"classes": ""
		}
	},
	"footer": {
		"title": "",
		"justify": "left",
		"align": "center",
		"style": {
			"classes": ""
		}
	},
	"style": {
		"classes": ""
	}
}
	
def dataToColumns(data, columnSchema=None, overrideSchema=None):
	tempList = []
	columnNames = data.getColumnNames()
	
	for columnName in columnNames:
		copiedSchema = deepcopy(schema)
		if overrideSchema is not None:
			copiedSchema.update(overrideSchema)
		if columnSchema is not None and columnName in columnSchema:
			copiedSchema.update(columnSchema[columnName])
		copiedSchema["field"] = columnName
		tempList.append(copiedSchema)	

	return tempList