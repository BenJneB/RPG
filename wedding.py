#! /usr/bin/env python3
################################################################################
#
#		Implementation of the wedding problem class
#
################################################################################
from search import *
import sys

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
		actionList = self.allPossibleActions
		lastValue = state.value
		lastAction = state.m
		lastState = state.tables
		for action in actionList:
			#if action not in self.actionsAlreadyDone:
			if action != lastAction: # Don't want to do the action than the last one. Avoiding loop.
				peopleLine1 = action[0][0]
				peopleCol1 = action[0][1]
				peopleLine2 = action[1][0]
				peopleCol2 = action[1][1]
				swappedPeople1 = lastState[peopleLine1][peopleCol1]
				swappedPeople2 = lastState[peopleLine2][peopleCol2]
				newState = clone(lastState)
				newState[peopleLine1][peopleCol1] = swappedPeople2
				newState[peopleLine2][peopleCol2] = swappedPeople1
				if(not(self.value(newState) < lastValue-30)):
					yield [self.numberOfPeople,self.numberOfTable,action,newState]

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
			elif (numberOfLine == 1): # Save the number of table
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

	def __init__(self, n, t, m, tables, value):
		self.n = n
		self.t = t
		self.m = m
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
        for (numberOfPeople,numberOfTable,move,tablesAssignment) in self.problem.successor(self.state):
            yield LSNode(self.problem, State(numberOfPeople, numberOfTable, move, tablesAssignment, self.problem.value(tablesAssignment)), self.step + 1)

######################
# Auxiliary Function #
######################

def clone(List):
	cloneList = []
	for line in List:
		cloneList.append(list(line))
	return cloneList

def maxValueTable(listNodes):
	firstRun = True
	maxValueTable = None
	for node in listNodes:
		state = node.state
		if(firstRun):
			maxValueTable = node
			firstRun = False
		elif (maxValueTable.state.value < state.value):
			maxValueTable = node
		elif (maxValueTable.state.value == state.value):
			choice = random.choice([maxValueTable,node])
			maxValueTable = choice
	return maxValueTable

def partition(listNodes, start, end):
    pivot = listNodes[end] 
    pivotValue = pivot.state.value                    # Partition around the last value
    bottom = start-1                           # Start outside the area to be partitioned
    top = end                                  # Ditto

    done = 0
    while not done:                            # Until all elements are partitioned...

        while not done:                        # Until we find an out of place element...
            bottom = bottom+1                  # ... move the bottom up.

            if bottom == top:                  # If we hit the top...
                done = 1                       # ... we are done.
                break

            if listNodes[bottom].state.value > pivotValue:           # Is the bottom out of place?
                listNodes[top] = listNodes[bottom]       		# Then put it at the top...
                break                          					# ... and start searching from the top.

        while not done:                        # Until we find an out of place element...
            top = top-1                        # ... move the top down.
            
            if top == bottom:                  # If we hit the bottom...
                done = 1                       # ... we are done.
                break

            if listNodes[top].state.value < pivotValue:              # Is the top out of place?
                listNodes[bottom] = listNodes[top]       		# Then put it at the bottom...
                break                          					# ...and start searching from the bottom.

    listNodes[top] = pivot                 		# Put the pivot in its place.
    return top                                 # Return the split point


def quicksort(listNodes,start,end):
    if start < end:                            # If there are two or more elements...
        split = partition(listNodes, start, end)    # ... partition the sublist...
        quicksort(listNodes, start, split-1)        # ... and sort both halves.
        quicksort(listNodes, split+1, end)
    else:
        return

def fiveMaxValueTables(listNodes):
	firstRun = True
	maxValueTables = []
	for node in listNodes:
		state = node.state
		if (len(maxValueTables) < 5):
			maxValueTables.append(node)
		elif(maxValueTables[0].state.value < state.value):
			maxValueTables[0] = node
		elif(maxValueTables[0].state.value == state.value):
			choice = random.choice([node,maxValueTables[0]])
			maxValueTables[0] = choice
		quicksort(maxValueTables,0,len(maxValueTables)-1)
	return maxValueTables

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
    currentState = State(problem.initial[0],problem.initial[1],problem.initial[2],problem.initial[3], problem.value(problem.initial[3]))
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
    currentState = State(problem.initial[0],problem.initial[1],problem.initial[2],problem.initial[3], problem.value(problem.initial[3]))
    current = LSNode(problem, currentState, 0)
    best = current
    for step in range(limit):
    	if callback is not None:
    		callback(current)
    	current = maxValueTable(list(current.expand()))
    	wedding.actionsAlreadyDone.append(current.state.m)
    	if current.state.value > best.state.value:
    		best = current
    return best

if __name__ == '__main__':
	wedding = Wedding(sys.argv[1])
	initState = State(wedding.initial[0],wedding.initial[1],wedding.initial[2],wedding.initial[3], wedding.value(wedding.initial[3]))
	printState(initState)

	node = maxvalue(wedding, 100)
	printState(node.state)

	#node2 = randomized_maxvalue(wedding, 100)	
	#printState(node2.state)
	#state = node.state
	#print(state)
