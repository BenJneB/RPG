"""Group #16 --- Fichefet Pierrick --- Daubry Benjamin"""
#! /usr/bin/env python3
################################################################################
#
#		Implementation of the wedding problem class
#
################################################################################
from search import *
import sys
import time

#################
# Problem class #
#################

class Wedding(Problem):
	def __init__(self, init):
		self.affinitiesTable = [] # The affinity matrix
		self.numberOfPeople = 0 
		self.numberOfTable = 0 
		self.createTablesAssignment(init)
		self.allPossibleActions = self.allPossibleActions() # Set of all possible actions
		self.actionsAlreadyDone = [] # Set of all actions that have been done. 


	def successor(self, state):
		successors = []
		listOfSonsValues = []
		count = 0
		actionList = self.allPossibleActions
		lastValue = state.value
		lastAction = state.m
		lastPeople = state.p
		lastState = state.tables
		for action in actionList:
			peopleLine1 = action[0][0]
			peopleCol1 = action[0][1]
			peopleLine2 = action[1][0]
			peopleCol2 = action[1][1]
			swappedPeople1 = lastState[peopleLine1][peopleCol1]
			swappedPeople2 = lastState[peopleLine2][peopleCol2]
			#if(lastPeople != [swappedPeople1,swappedPeople2] and lastPeople != [swappedPeople2,swappedPeople1]):
			#if ([swappedPeople1,swappedPeople2] not in self.actionsAlreadyDone) and ([swappedPeople2,swappedPeople1] not in self.actionsAlreadyDone):
			newState = cloneState(lastState)
			newState[peopleLine1][peopleCol1] = swappedPeople2
			newState[peopleLine2][peopleCol2] = swappedPeople1
			newState[peopleLine1].sort()
			newState[peopleLine2].sort()
			newValue = quickValue(state,newState,action)
			if(count == 0):
				listOfSonsValues.append(newValue)
			elif(newValue > max(listOfSonsValues)):
				listOfSonsValues.append(newValue)
			if((newValue in listOfSonsValues) or (count < 5)):
				yield [state,self.numberOfPeople,self.numberOfTable,action,[swappedPeople1,swappedPeople2],newState]
			count += 1

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
			if(numberOfLine == 0):
				self.numberOfPeople = line
			elif(numberOfLine == 1):
				self.numberOfTable = line
			else:
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
						if(Affinity not in keysAffinity): 					# If this affinity already exist we need to add a new people
							dicoOfNoSitPeople[Affinity]=[peopleColIndex] 	# in the dictionnary at this key Otherwise we add this people at
						else:												# this new key.
							dicoOfNoSitPeople[Affinity].append(peopleColIndex)
					peopleColIndex+=1
					keysAffinity = list(dicoOfNoSitPeople.keys())

				orderedAffinities = []
				for elem in keysAffinity:
					orderedAffinities.append(int(float(elem))) # We want to order int not string.
				orderedAffinities.sort(reverse=True) 
				tablesAssignment.append([])
				tablesAssignment[tableIndex].append(peopleLineIndex)
				listOfSitPeople.append(peopleLineIndex)
				numberOfPeople = 1 # peopleLineIndex have already been assigned so just need to find tableMaxPeople-1 peoples. 
				key = 0
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
		self.initial = (self.numberOfPeople, self.numberOfTable, [[0,0],[0,0]],[0,0],tablesAssignment)

	"""Return all possible actions, An action is a 2-uple containing the row and column of peoples who are going to be swapped"""
	"""action = [[row1,column1],[row2,column2]]"""
	def allPossibleActions(self):
		tableMaxPeople = self.numberOfPeople/self.numberOfTable
		actionList = []
	
		line1 = 0
		while(line1<self.numberOfTable-1):
			col1 = 0
			while (col1 < tableMaxPeople):
				line2 = line1+1
				while(line2 < self.numberOfTable):
					col2 = 0
					while(col2 < tableMaxPeople):
						action = [[line1,col1],[line2,col2]]
						actionList.append(action)
						col2 += 1
					line2 += 1
				col1 += 1
			line1 += 1
		return actionList

###############
# State class #
###############

class State:

	def __init__(self, n, t, m, p, tables, value):
		self.n = n
		self.t = t
		self.m = m
		self.p = p
		self.tables = tables
		self.value = value

###############
# LSNode class #
###############

class LSNode:
    """A node in a local search. You will not need to subclass this class 
        for local search."""

    def __init__(self, problem, state, step):
        """Create a local search Node."""
        self.problem = problem
        self.state = state
        self.step = step
        self._value = None

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def value(self):
        """Returns the value of the state contained in this node."""
        if self._value is None:
            self._value = self.problem.value(self.state)
        return self._value

    def expand(self):
        """Yields nodes reachable from this node. [Fig. 3.8]"""
        for (oldState,numberOfPeople,numberOfTable,move,people,tablesAssignment) in self.problem.successor(self.state):
            yield LSNode(self.problem, State(numberOfPeople, numberOfTable, move, people, tablesAssignment, quickValue(oldState,tablesAssignment,move)), self.step + 1)

######################
# Auxiliary Function #
######################

def quickValue(oldState,newTables,action):
	oldValue = oldState.value
	oldTable1 = oldState.tables[action[0][0]]
	oldTable2 = oldState.tables[action[1][0]]
	newTable1 = newTables[action[0][0]]
	newTable2 = newTables[action[1][0]]
	oldTableValue = singleTableValue(oldTable1) + singleTableValue(oldTable2) 
	newTableValue = singleTableValue(newTable1) + singleTableValue(newTable2)
	return oldValue - oldTableValue + newTableValue

def singleTableValue(table):
	affinitiesTable = wedding.affinitiesTable
	tableMaxPeople = wedding.numberOfPeople/wedding.numberOfTable
	value = 0
	for people in table:
		peopleIndex = 0
		while(peopleIndex < tableMaxPeople):
			value += int(float(affinitiesTable[people][table[peopleIndex]]))
			peopleIndex += 1
	return value

def cloneState(List):
	cloneList = []
	for line in List:
		cloneList.append(list(line))
	return cloneList

def maxValueTable(listNodes):
	listNodes2 = sorted(listNodes,key=lambda a:a.state.value,reverse = True)
	firstElem = listNodes2[0]
	firstAction = firstElem.state.m
	firstTable1 = firstElem.state.tables[firstAction[0][0]]
	firstTable2 = firstElem.state.tables[firstAction[1][0]]
	for node in listNodes2:
		action = node.state.m
		table1 = node.state.tables[action[0][0]]
		table2 = node.state.tables[action[1][0]]
		if(firstElem.state.value == node.state.value and firstTable1+firstTable2 > table1+table2):
			#if(listNodes2[0].state.value == 490 or listNodes2[0].state.value == 491):
			#	print(firstTable1+firstTable2,">",table1+table2,firstTable1+firstTable2 > table1+table2)
			firstElem = node
			firstTable1 = table1
			firstTable2 = table2
		elif(firstElem.state.value != node.state.value):
			break
	#printState(firstElem.state)
	return firstElem

def fiveMaxValueTables(listNodes):
	listNodes2 = sorted(listNodes,key=lambda a:a.state.value,reverse = True)
	listElem = []
	i = 0
	j = 0
	for node in listNodes2:
		if(i < 5):
			listElem.append(node)
			if(listElem[i].state.value != listElem[j].state.value):
				j = i
		elif (listElem[4].state.value == node.state.value):
			listElem.append(node)
		else:
			break
		i+=1

	if(len(listElem) == 5):
		return listElem
	
	bestTable1 = listElem[j:len(listElem)]
	bestTable2 = sorted(bestTable1,key=lambda a:a.state.tables[a.state.m[0][0]]+a.state.tables[a.state.m[1][0]],reverse = True)

	return listElem[0:j]+bestTable2[j:len(bestTable2)]

def printState(state):
	print(state.value)
	for table in state.tables:
		table.sort()
		for people in table:
			sys.stdout.write(str(people))
			sys.stdout.write(" ")
		sys.stdout.write("\n")

################
# Local Search #
################

def randomized_maxvalue(problem, limit=100, callback=None):
    currentState = State(problem.initial[0],problem.initial[1],problem.initial[2],problem.initial[3],problem.initial[4], problem.value(problem.initial[4]))
    current = LSNode(problem, currentState, 0)
    best = current
    for step in range(limit):
    	if callback is not None:
    		callback(current)
    	current = random.choice(fiveMaxValueTables(list(current.expand())))
    	wedding.actionsAlreadyDone.append(current.state.m)
    	if current.state.value > best.state.value:
    		best = current
    return best

def maxvalue(problem, limit=100, callback=None):
    currentState = State(problem.initial[0],problem.initial[1],problem.initial[2],problem.initial[3],problem.initial[4], problem.value(problem.initial[4]))
    current = LSNode(problem, currentState, 0)
    best = current
    for step in range(limit):
    	if callback is not None:
    		callback(current)
    	#print("##############steeeeeeeeep####################"" = ",step)
    	current = maxValueTable(list(current.expand()))
    	#print(current.state.p)
    	#printState(current.state)
    	wedding.actionsAlreadyDone.append(current.state.p)
    	wedding.actionsAlreadyDone.append(current.state.p.reverse())
    	if (current.state.value > best.state.value):
    		best = current
    return best

if __name__ == '__main__':
	wedding = Wedding(sys.argv[1])
	initState = State(wedding.initial[0],wedding.initial[1],wedding.initial[2],wedding.initial[3],wedding.initial[4], wedding.value(wedding.initial[4]))
	printState(initState)

	start_time = time.time()
	node = maxvalue(wedding)
	interval = time.time()-start_time
	printState(node.state)
	print(interval)

	#node2 = randomized_maxvalue(wedding, 100)	
	#printState(node2.state)
	#state = node.state
	#print(state)
