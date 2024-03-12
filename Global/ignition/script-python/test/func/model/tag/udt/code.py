class UDTTest(test.func.ft.FunctionTest):
	def __init__(self):
		if self.__class__ == UDTTest:
			raise TypeError("UDTTest cannot be directly instantiated")
		test.func.ft.FunctionTest.__init__(self)
		
		
		