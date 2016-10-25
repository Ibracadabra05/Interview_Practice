from User import User 
import sys
import math 

# For debugging purposes. 

USER_INFECTED = "{0} has been infected."

USER_DISINFECTED = "{0} has been disinfected."

ALREADY_INFECTED = "{0} has already been infected."

USER_STATUS_INFECTED = "{0} is infected."

USER_STATUS_NOT_INFECTED = "{0} is not infected. Please infect said user first."


def depth_first_infect(user):
	""" 
		Depth-first search starting from a specific user. 
		total_infection helper function. 
		Parameters:
			user - User from which our depth-first infection search starts. 
			version - Version of software to infect with. 
	"""
	if not user.infected(): 
		print utils.USER_STATUS_NOT_INFECTED.format(user.getname())
		return None

	infected = []
	stack = [user]
	while stack:
		vertex = stack.pop()
		if vertex not in infected:
			if not vertex.infected():
				vertex.infect(user.getversion())
			infected.append(vertex)
			for student in vertex.getstudents():
				if student not in infected:
					stack.append(student)

		if vertex.getcoach():
			if vertex.getcoach() not in infected:
				stack.append(vertex.getcoach())
	return infected 


def simple_dfs(graph, user):
	""" 
		Basic depth-first search algorithm.
		Mostly for a test case where I make sure
		the traversal is done correctly. 
	"""
	visited = []
	stack = [user]
	while stack:
		vertex = stack.pop()
		if vertex not in visited:
			visited.append(vertex)
			for neighbor in graph[vertex]:
				if neighbor not in visited:
					stack.extend(neighbor)
	return visited  


def dfs_without_infect(user):
	"""
		Depth-first search to see number of users that could 
		be infected without infected them. 
		Parameters:
			user - User from which our depth-first search starts.
	"""
	visited = []
	stack = [user]
	while stack:
		vertex = stack.pop()
		if vertex not in visited:
			visited.append(vertex)
			for student in vertex.getstudents():
				if student not in visited:
					stack.append(student)

		if vertex.getcoach():
			if vertex.getcoach() not in visited:
				stack.append(vertex.getcoach())
	return visited 

def total_infection(user, new_version):
	"""
		Total infection algorithm. Starting from a given user, 
		the entire connected component of the coaching graph containing that 
		user becomes infected.
		Parameters:
			user - User from which infection spreads
			new_version - version of software to infect connected coaching component 
			of users with 
	"""

	if not user.infected():
		user.infect(new_version)

	return depth_first_infect(user)


def limited_infection(users, new_version, target_num_users):
	"""
		Limited infection algorithm. Starting from a given user,
		infect those close to a given number of users.
		
		This function works for when there is a connected component with
		exactly the same number of users as our target; if the exact number isn't found,
		the closest approximate number of targets is chosen. 

		Parameters:
			users - Couple of users one could start infecting from.
			new_version - version of software to infect connected coaching component 
			of users with.
			target_num_users - Target number of users we want to infect. If this number is 
			found at any point in our search. Algorithm stops searching for network components and 
			proceeds to infect what has been already found. 

	"""
	connected_components = []
	
	#retrieve potential "infection groups" by getting entire connected components from all users
	for user in users:
		curr_result  = dfs_without_infect(user)
		connected_components.append(curr_result)
		if len(curr_result) == target_num_users:
			break
		

	#get the connected network with the closest number of users to our target
	closest_index = 0
	minimum_diff = sys.maxint
	for i in range(len(connected_components)):
		curr_len = len(connected_components[i])
		curr_diff = math.fabs(curr_len - target_num_users)
		if curr_diff < minimum_diff:
			closest_index = i 
			minimum_diff = curr_diff 

	sample_group = connected_components[closest_index]

	#infect them all!
	for user in sample_group:
		user.infect(new_version)

	return sample_group 

