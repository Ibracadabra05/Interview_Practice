import utils

'''
	Class that abstracts the User entity.  
'''

class User:

	def __init__(self, name, software_vers, coach, students):
		self.name = name
		self.is_infected = False 
		self.software_vers = software_vers
		self.coach = coach
		self.students = students

	def getname(self):
		return self.name

	def setname(self, new_name):
		self.name = new_name

	def getversion(self):
		return self.software_vers 

	def setversion(self, new_version):
		self.software_vers = new_version

	def getcoach(self):
		return self.coach

	def setcoach(self, new_coach):
		temp = self.coach 
		self.coach = new_coach
		new_coach.addstudent(self)
		if temp is not None:
			temp.removestudent(self)

	def addstudent(self, new_student):
		if new_student in self.students:
			return None
		new_student.coach = self
		self.students.append(new_student)

	def removestudent(self, student):
		if student not in self.students:
			return None
		self.students.remove(student)

	def has_students(self):
		return len(self.students) > 0

	def getstudents(self):
		return self.students

	def infected(self):
		return self.is_infected == True

	def status(self):
		output = utils.USER_STATUS_INFECTED.format(self.getname()) if \
		self.is_infected else utils.USER_STATUS_NOT_INFECTED.format(self.getname())
		return output 

	def infect(self, newer_version):
		if newer_version < self.getversion():
			return None
		elif self.is_infected == True:
			print utils.ALREADY_INFECTED.format(self.getname())
			return None 
		self.is_infected = True
		self.setversion(newer_version)
		print utils.USER_INFECTED.format(self.getname())

		#infect students
		if self.has_students():
			for student in self.students:
				student.setversion(newer_version)
				student.is_infected = True 

		#infect coach
		if self.coach is not None:
			self.coach.is_infected = True 
			self.coach.setversion(newer_version)
		  

	def disinfect(self, older_version):
		'''
			This function is here in case the wrong group of users gets infected
			and starts sending us requests to fix all the bugs!
			In which case, we would call this function on them all 
		'''
		if self.getversion() < older_version:
			return None 
		self.is_infected = False 
		self.setversion(older_version)
		print utils.USER_DISINFECTED.format(self.getname())

