from test.t import Test

class FunctionTest(Test):
	def __init__(self):
		if self.__class__ == FunctionTest:
			raise TypeError("FunctionTest cannot be directly instantiated")
		Test.__init__(self)
		
	def __str__(self):
		justNum = 20
		tempString = ""
		tempString += "*"*15 +  " Function Test:     "+ str(self.testName) +" "+ "*"*15 + "\n"
		tempString += "Results: ".ljust(justNum) + str(self.passed) + "/" + str(self.ran) + "\n"
		tempString += "Total Passed: ".ljust(justNum) + str(self.passed) + "\n"
		tempString += "Total Failed: ".ljust(justNum) + str(self.ran - self.passed) + "\n"
		tempString += "\n"
		tempString += "| Method Name ".ljust(justNum)+ "  | Result |" + "\n"
		tempString += "-"* 32 + "\n"
		for test in self.testList:
			tempString += "| "+test["methodName"].ljust(justNum)+ "| " +("Passed |" if test["passed"] else "Failed | !")+ "\n"
		tempString += "-"*32+"\n"
		tempString += "*"*15 + " End Function Test: "+ self.testName +"*"*15
		
		return tempString