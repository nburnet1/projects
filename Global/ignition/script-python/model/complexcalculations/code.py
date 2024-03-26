def numComplex(num, num1):
	num += num1 * num
	return num
	
def stringComplex(string1, string2, string3):
	return string1 * string2 + string3
	
	


class TestComplexCalculations(test.unit.ut.UnitTest):
	def __init_(self):
		self.__init__(test.unit.ut.UnitTest)
		
	def test_numComplex_pass(self):
		num = 2
		num1 = 4
		
		return numComplex(num,num1) == 10
		
	def test_numComplex_fail_string(self):
		try:
			num = 5
			num1  = 'asdf'
			return numComplex(num,num1) 
		except:
			return False
		