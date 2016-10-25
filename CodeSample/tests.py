import unittest
import utils 
from User import User 

class TestUserMethods(unittest.TestCase):

	def test(self): 
		mike = User('Mike', 1.0, None, [])
		jane = User('Jane', 1.0, mike, [])
		ibrahim = User('Ibrahim', 1.0, None, [])
		mike.addstudent(jane)
		#name property test
		self.assertEqual(jane.getname(), 'Jane')
		jane.setname('Janet')
		self.assertEqual(jane.getname(), 'Janet')
		jane.setname('Jane')
	
		#version property test
		self.assertEqual(jane.getversion(), 1.0)
		self.assertFalse(jane.infected())
	
		#coach relationship test
		self.assertEqual(jane.getcoach(), mike)
		jane.setcoach(ibrahim)
		self.assertEqual(jane.getcoach(), ibrahim)
		jane.setcoach(mike)
		self.assertIsNone(mike.getcoach())

		#is coached by relationship test 
		self.assertIn(jane, mike.getstudents())
		self.assertNotIn(jane, ibrahim.getstudents())
		self.assertFalse(ibrahim.has_students())

		#status test 
		self.assertNotEqual(jane.status(), utils.USER_STATUS_INFECTED.format(jane.getname()))
		self.assertEqual(jane.status(), utils.USER_STATUS_NOT_INFECTED.format(jane.getname()))

		#infection test
		mike.infect(2.0)
		self.assertTrue(mike.infected())
		self.assertIsNone(mike.infect(2.0))
		self.assertIsNone(mike.infect(1.0))
		self.assertTrue(jane.infected())
		self.assertFalse(ibrahim.infected())

		#disinfection test
		jane.disinfect(1.0)
		self.assertFalse(jane.infected())
		self.assertIsNone(jane.disinfect(2.0))

class TestSimpleDfsAlgo(unittest.TestCase):
	"""
		This was just to see that my depth-first search algorithm
		is correct. 
	"""
	def testdfs(self):
		
		graph = {'A': ['B', 'C'], \
        		'B': ['A', 'D', 'E'], \
        		'C': ['A', 'F'], \
        		'D': ['B'], \
        		'E': ['B', 'F'], \
        		'F': ['C', 'E']} 
		result = utils.simple_dfs(graph, 'A')
		self.assertEqual(result, ['A', 'C', 'F', 'E', 'B', 'D'])


class TestTotalInfection(unittest.TestCase):
	def testTotalInfection(self):
		mike = User('Mike', 1.0, None, [])
		ibrahim = User('Ibrahim', 1.0, None, [])
		jane = User('Jane', 1.0, None, [])
		john = User('John', 1.0, None, [])
		ellen = User('Ellen', 1.0, None, [])
		tyrone = User('Tyrone', 1.0, None, [])
		dmitri = User('Dmitri', 1.0, None, [])
		
		mike.addstudent(ibrahim)
		mike.addstudent(jane)
		mike.addstudent(dmitri)

		ibrahim.addstudent(john)
		ibrahim.addstudent(ellen)
		
		jane.addstudent(tyrone)


		"""
			Connected network looks like:

				Mike
		     /        \      \
		 Ibrahim     Jane   Dmitri
		/      \       |
	   John   Ellen   Tyrone


		"""

		#starting from mike
		results = utils.total_infection(mike, 2.0)

		#all of them have to be infected
		for user in results:
			self.assertTrue(user.infected())
			self.assertEqual(user.getversion(), 2.0)

		self.assertIn(mike, results)
		self.assertIn(ibrahim, results)
		self.assertIn(jane, results)
		self.assertIn(dmitri, results)
		self.assertIn(tyrone, results)
		self.assertIn(ellen, results)
		self.assertIn(john, results)

		#disinfect
		for user in results:
			user.disinfect(1.0)

		#new network with disconnected component, say Tayo is another instructor
		jose = User('Jose', 1.0, None, [])
		tayo = User('Tayo', 1.0, None, [])
		sahil = User('Sahil', 1.0, None, [])

		tayo.addstudent(sahil)
		tayo.addstudent(jose)


		#Tayo and his students should not be infected but mike's group should, starting from Jane
		results = utils.total_infection(jane, 2.0)

		for user in results:
			self.assertTrue(user.infected())
			self.assertEqual(user.getversion(), 2.0)

		self.assertIn(mike, results)
		self.assertIn(ibrahim, results)
		self.assertIn(jane, results)
		self.assertIn(dmitri, results)
		self.assertIn(tyrone, results)
		self.assertIn(ellen, results)
		self.assertIn(john, results)

		self.assertFalse(tayo.infected())
		self.assertEqual(tayo.getversion(), 1.0)
		for user in tayo.getstudents():
			self.assertFalse(user.infected())
			self.assertEqual(user.getversion(), 1.0)

		self.assertNotIn(tayo, results)
		self.assertNotIn(jose, results)
		self.assertNotIn(sahil, results)
		

class TestLimitedInfection(unittest.TestCase): 
	def testLimitedInfection(self):

		#Mike's group
		mike = User('Mike', 1.0, None, [])
		ibrahim = User('Ibrahim', 1.0, None, [])
		jane = User('Jane', 1.0, None, [])
		john = User('John', 1.0, None, [])
		ellen = User('Ellen', 1.0, None, [])
		tyrone = User('Tyrone', 1.0, None, [])
		dmitri = User('Dmitri', 1.0, None, [])
		
		mike.addstudent(ibrahim)
		mike.addstudent(jane)
		mike.addstudent(dmitri)

		ibrahim.addstudent(john)
		ibrahim.addstudent(ellen)
		
		jane.addstudent(tyrone)

		#Tayo's group
		jose = User('Jose', 1.0, None, [])
		tayo = User('Tayo', 1.0, None, [])
		sahil = User('Sahil', 1.0, None, [])

		tayo.addstudent(sahil)
		tayo.addstudent(jose)


		#test-case to find exact number of members
		results = utils.limited_infection([ellen, jose], 2.0, 3)

		self.assertEqual(len(results), 3)

		for member in results:
			self.assertTrue(member.infected())

		self.assertIn(tayo, results)
		self.assertIn(jose, results)
		self.assertIn(sahil, results)

		self.assertNotIn(mike, results)
		self.assertNotIn(ibrahim, results)
		self.assertNotIn(jane, results)
		self.assertNotIn(dmitri, results)
		self.assertNotIn(tyrone, results)
		self.assertNotIn(ellen, results)
		self.assertNotIn(john, results)

		self.assertFalse(mike.infected())
		self.assertFalse(ibrahim.infected())
		self.assertFalse(jane.infected())
		self.assertFalse(dmitri.infected())
		self.assertFalse(tyrone.infected())
		self.assertFalse(ellen.infected())
		self.assertFalse(john.infected())

		#disinfect for next test
		for member in results:
			member.disinfect(1.0)

		#test-case to find approximate number of members i.e. connected
		#component with the closest number of members to target. 
		results = utils.limited_infection([ellen, jose], 2.0, 9)

		self.assertEqual(len(results), 7)

		for member in results:
			self.assertTrue(member.infected())

		self.assertIn(mike, results)
		self.assertIn(ibrahim, results)
		self.assertIn(jane, results)
		self.assertIn(dmitri, results)
		self.assertIn(tyrone, results)
		self.assertIn(ellen, results)
		self.assertIn(john, results)

		self.assertNotIn(tayo, results)
		self.assertNotIn(jose, results)
		self.assertNotIn(sahil, results)


if __name__ == '__main__':
    unittest.main()