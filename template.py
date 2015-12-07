#! /usr/bin/env python3
################################################################################
#
#		Implementation of the wedding problem class
#
################################################################################
from search import *

#################
# Problem class #
#################

class Wedding(Problem):
	def __init__(self, init):
		self.createTablesAssignment(init)
		self.affinitiesTable = []
		self.numberOfPeople = 0
		self.numberOfTable = 0

	def successor(self, state):
		successors = []
		actionList = allPossibleActions(state)
		for action in actionList:
			peopleLine1 = action[0][0]
			peopleCol1 = action[0][1]
			peopleLine2 = action[1][0]
			peopleCol2 = action[1][1]
			swappedPeople1 = state[peopleLine1][peopleCol1]
			swappedPeople2 = state[peopleLine2][peopleCol2]
			state[peopleLine1][peopleCol1] = swappedPeople2
			state[peopleLine2][peopleCol2] = swappedPeople1
			yield [self.numberOfPeople,self.numberOfTable,action,state]
			state[peopleLine1][peopleCol1] = swappedPeople1
			state[peopleLine2][peopleCol2] = swappedPeople2

	def value(self, state):
		affinitiesTable = self.affinitiesTable
		tableMaxPeople = self.numberOfPeople/self.numberOfTable
		value = 0
		for table in state:
			for people in table:
				peopleIndex = 0
				while(peopleIndex < tableMaxPeople):
					value += int(float(affinitiesTable[people][table[peopleIndex]]))
					peopleIndex += 1
		return value

	"""This function return a table representing the affinities between each people"""
	def createAffinitiesTable(self, path):
		affinitiesTable = []
		f = open(path,'r')
		numberOfLine = 0
		numberOfColumn = 0

		for line in f:
			affinitiesColTable = []
			minus = False # check Whether we have a negative value or not.
			for col in line:
				if(col != " " and col != '\n' and col != "-"):
					if(minus):
						affinitiesColTable.append("-"+col)
						minus = False
					else:
						affinitiesColTable.append(col)
				elif(col == "-"):
					minus = True
				numberOfColumn += 1

			if (numberOfLine == 0): # Save the number of people
				self.numberOfPeople = affinitiesColTable[0]
				i=1
				while(i<len(affinitiesColTable)):
					self.numberOfPeople += affinitiesColTable[i]
					i += 1
			elif (numberOfLine == 1): # Save the number of table available
				self.numberOfTable = affinitiesColTable[0]
				i=1
				while(i<len(affinitiesColTable)):
					self.numberOfTable += affinitiesColTable[i]
					i += 1
			else:	
				affinitiesTable.append(affinitiesColTable)
			numberOfLine += 1
		f.close
		self.numberOfPeople = int(float(self.numberOfPeople))
		self.numberOfTable = int(float(self.numberOfTable))

		return affinitiesTable

	"""This function return the initial repartition of people at each table."""
	def createTablesAssignment(self, path):
		self.affinitiesTable = self.createAffinitiesTable(path)
		tableMaxPeople = self.numberOfPeople/self.numberOfTable # Maximum number of people et each table
		tablesAssignment = [] 
		tableIndex = 0 
		peopleLineIndex = 0
		listOfSitPeople = [] # List of people who have been assigned to a table
		for lineAffinities in self.affinitiesTable:
			if(tableIndex >= self.numberOfTable): # All table are full, so we stop
				break
			dicoOfNoSitPeople = {}
			keysAffinity = list(dicoOfNoSitPeople.keys()) # List of all the value used as key represanting an affinity.
			peopleColIndex = 0
			if (peopleLineIndex not in listOfSitPeople): # If peopleLineIndex have already been assigned don't need to assigne it again.
				for Affinity in lineAffinities:
					if(peopleLineIndex != peopleColIndex and peopleColIndex not in listOfSitPeople):
						if(Affinity not in keysAffinity): 					# If this affinity already exist we 
							dicoOfNoSitPeople[Affinity]=[peopleColIndex] 	# need to add a new people in the dictionnary at this key
						else:												# Otherwise we add this people at this new key.
							dicoOfNoSitPeople[Affinity].append(peopleColIndex)
					peopleColIndex+=1
					keysAffinity = list(dicoOfNoSitPeople.keys())

				orderedAffinities = []
				for elem in keysAffinity:
					orderedAffinities.append(int(float(elem))) # We want to order int not string.
				orderedAffinities.sort(reverse=True) 
				numberOfPeople = 1 # peopleLineIndex have already been assigned so just need to find tableMaxPeople-1 peoples. 
				key = 0
				tablesAssignment.append([])
				tablesAssignment[tableIndex].append(peopleLineIndex)
				listOfSitPeople.append(peopleLineIndex)
				while (numberOfPeople < tableMaxPeople):						# taking all people having best affinities 
					for elem in dicoOfNoSitPeople[str(orderedAffinities[key])]:	# with peopleLineIndex
						if (numberOfPeople < tableMaxPeople):
							tablesAssignment[tableIndex].append(elem)
							listOfSitPeople.append(elem)
						numberOfPeople += 1
					key += 1
					
				tablesAssignment[tableIndex].sort()
				tableIndex += 1
			peopleLineIndex += 1
		self.initial = (self.numberOfPeople, self.numberOfTable, [[0,0],[0,0]],tablesAssignment)

###############
# State class #
###############

class State:

	def __init__(self, n, t, m, tables, value):
		self.n = n
		self.t = t
		self.m = m
		self.tables = tables
		self.value = value

	def expand(self, problem):
		for (numberOfPeople,numberOfTable,move,tablesAssignment) in problem.successor(self.state):
			yield State(numberOfPeople, numberOfTable, move, tablesAssignment, value(tablesAssignment))

######################
# Auxiliary Function #
######################

"""Return all possible actions, An action is a 2-uple containing the row and column of peoples who are going to be swapped"""
"""action = [[row1,column1],[row2,column2]]"""
def allPossibleActions(state):
	numberOfTable = len(state)
	tableMaxPeople = len(state[0])
	numberOfPeople = numberOfTable*tableMaxPeople
	actionList = []
	
	line1 = 0
	while(line1<numberOfTable-1):
		col1 = 0
		while (col1 < tableMaxPeople):
			line2 = line1+1
			while(line2 < numberOfTable):
				col2 = 0
				while(col2 < tableMaxPeople):
					action = [[line1,col1],[line2,col2]]
					actionList.append(action)
					col2 += 1
				line2 += 1
			col1 += 1
		line1 += 1
	return actionList

################
# Local Search #
################

def randomized_maxvalue(problem, limit=100, callback=None):
	pass

def maxvalue(problem, limit=100, callback=None):
	pass

if __name__ == '__main__':
	wedding = Wedding(sys.argv[1])
	print(wedding.initial)

	node = randomized_maxvalue(wedding, 100)	
	# node = maxvalue(wedding, 100)
	
	state = node.state
	print(state)
