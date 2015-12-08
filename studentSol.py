#!/usr/bin/env python3

import rpg

def get_clauses(merchant, level):
		# Append all clauses needed to find the correct equipment in the 'clauses' list.
		#
		# Minisat variables are represented with integers. As such you should use
		# the index attribute of classes Ability and Equipment from the rpg.py module
		# 
		# The equipments and abilities they provide read from the merchant file you passed
		# as argument are contained in the variable 'merchant'.
		# The enemies and abilities they require to be defeated read from the level file you
		# passed as argument are contained in the variable 'level'
		# 
		# For example if you want to add the clauses equ1 or equ2 or ... or equN (i.e. a
		# disjunction of all the equipment pieces the merchant proposes), you should write:
		# 
		# clauses.append(tuple(equ.index for equ in merchant.equipments))
		equipement=merchant.equipments
		abiNeeded=level.ability_names
		listN=[]
		listName=[]
		for abiN in abiNeeded:
			listTemp=[]
			listTemp2=[]
			for equip in equipement:
				provide=equip.provides
				for e in provide:
					if(abiN == str(e)):
						listTemp.append(equip.index)
						listTemp2.append(equip)
			if(len(listTemp)!=0):
				listN.append(tuple(listTemp))
				listName.append(tuple(listTemp2))
		#print(listN)
		#print(listName)
		listCon=[]
		for e in listName:
			listTemp=[]
			for conflict in e:
				listTemp.append((conflict.index,conflict.conflicts.index))
			listCon=listCon+listTemp

		print(listCon)
		#print(len(listCon))

		clauses = listN[:]+listCon[:]
		#print(clauses)
		return clauses

def get_nb_vars(merchant, level):
		# nb_vars should be the number of different variables present in your list 'clauses'
		# 
		# For example, if your clauses contain all the equipments proposed by merchant and
		# all the abilities provided by these equipment, you would have:
		# nb_vars = len(merchant.abilities) + len(merchant.equipments)
		i=0
		equipement=merchant.equipments
		abiNeeded=level.ability_names
		listName=[]
		listbis=[]
		for abiN in abiNeeded:
			listTemp=[]
			for equip in equipement:
				provide=equip.provides
				for e in provide:
					if(abiN == str(e)):
						listTemp.append(equip)
						if equip not in listbis:
							listbis.append(equip)
							i+=1
			if(len(listTemp)!=0):
				listName.append(tuple(listTemp))

		for e in listName:
			for conflict in e:
				if conflict.conflicts not in listbis:
					i+=1


		#print(i)
		nb_vars = i
		return nb_vars
