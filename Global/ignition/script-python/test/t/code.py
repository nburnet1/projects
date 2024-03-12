class Test():
	METHOD_DELIMITER = "test_"
	def __init__(self):
		if self.__class__ == Test:
			raise TypeError("Test cannot be directly instantiated")
			
		self.instance = self
		self.attributes = dir(self)
		self.methods = [attr for attr in self.attributes if callable(getattr(self, attr)) and attr.startswith(self.METHOD_DELIMITER)]
		self.passed = 0
		self.ran = 0
		self.testList = []
		self.testName = self.__class__.__name__
		
	def __str__(self):
		raise NotImplementedError(self.__class__.__name__ + " has not implemented the __str__ built-in method")
		
		
	def toMethod(self, methodName):
		return getattr(self.instance, methodName)
		
	def test(self):
		for methodName in self.methods:
			methodToTest = self.toMethod(methodName)
			result = methodToTest()
			self.testList.append({
				"methodName" : methodName.split(self.METHOD_DELIMITER)[-1],
				"passed": result
			})
			if result:
				self.passed += 1
			self.ran += 1
