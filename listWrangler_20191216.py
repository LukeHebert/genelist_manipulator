'''
Author: Luke Hebert
Date begun: December 16th, 2019
Description: finds either the intersection, union, or unique items from a set of n lists
	especially useful for comparing lists of genes
	inputs for unique option need to be .txt files; this could be easily tweaked though
	all input and output are forced to upper case; can be easily tweaked
'''

import os, sys

def getContents(paths_list):
	'''reads multiple files and assigns them to a dictionary with filepaths as keys and content lists as values'''
	contents_dict = {}
	for file in paths_list:
		contents_dict[file] = []
		with open(file, 'r') as inFile:
			for line in inFile:
				line = line.strip('\n').strip('\r')
				contents_dict[file].append(line.upper())
	return contents_dict

slash = '\\' if os.name == 'nt' else '/'

arguments_list = sys.argv[:]

#INTERSECTION OF N LISTS
if "-i" in arguments_list:
	#remove python program and -i arguments to make a pathway list
	inPaths_list = list(arguments_list)
	temp_pathsList = list(inPaths_list)
	for path in temp_pathsList:
		if (path == '-i') or ('.py' in path):
			inPaths_list.remove(path)
	#print out the pathway indexes so that user can select one as the output pathway directory
	print('\n')
	for i, path in enumerate(inPaths_list):
		print(str(i) + '\t' + path)
	#ask user to select output file name and directory
	outFileName = raw_input("\nPlease enter the name (not the path) of the output txt file (include the file suffix):")
	outPath_index = int(raw_input("\nPlease enter index of the file whose path will be used for the output file (an integer):"))
	if len(inPaths_list) < 2: #user must specify at least two input files for this option
		print('\nUser must specify at least two lists in order to find the intersection.')
	else:
		print("\nYou chose to find the intersection of " + str(len(inPaths_list)) + " lists.")
		contents_dict = getContents(inPaths_list) #read the input files into a dictionary
		intersection_list = [] #will fill this with intersection data only
		for key, val in contents_dict.iteritems(): #for each input file's list data
			if len(intersection_list) == 0: #if this is the first file's data evaluated, just copy it to output list
				intersection_list = list(val)
			else: #the heart of the algorithm
				temp_list = [item for item in val if item in intersection_list] #this should create the intersection of val and intersection_list
				intersection_list = list(temp_list) #update intersection_list using a deep copy
		completeOutPath = slash.join(inPaths_list[outPath_index].split(slash)[:-1] + [outFileName]) #not the most readable, but this is the output path/name
		#write intersection_list to the output file as a single column of data
		with open(completeOutPath, 'w') as outFile:
			for item in intersection_list:
				outFile.write(item + '\n')
	
	
#UNION OF N LISTS
elif "-n" in arguments_list:
	#remove python program and -n arguments to make a pathway list
	inPaths_list = list(arguments_list)
	temp_pathsList = list(inPaths_list)
	for path in temp_pathsList:
		if (path == '-n') or ('.py' in path):
			inPaths_list.remove(path)
	#print out the pathway indexes so that user can select one as the output pathway directory
	print('\n')
	for i, path in enumerate(inPaths_list):
		print(str(i) + '\t' + path)
	#ask user to select output file name and directory
	outFileName = raw_input("\nPlease enter the name (not the path) of the output txt file (include the file suffix):")
	outPath_index = int(raw_input("\nPlease enter index of the file whose path will be used for the output file (an integer):"))
	if len(inPaths_list) < 2: #user must specify at least two input files for this option
		print('\nUser must specify at least two lists in order to find the union.')
	else:
		print("\nYou chose to find the union of " + str(len(inPaths_list)) + " lists.")
		contents_dict = getContents(inPaths_list) #read the input files into a dictionary
		union_list = [] #will fill this with intersection data only
		for key, val in contents_dict.iteritems(): #for each input file's list data
			if len(union_list) == 0: #if this is the first file's data evaluated, just copy it to output list
				union_list = list(val)
			else: #the hearth of the algorithm
				temp_list = union_list + val #update union list with current file's data/list
				union_list = list(set(temp_list)) #remove any duplicates
		completeOutPath = slash.join(inPaths_list[outPath_index].split(slash)[:-1] + [outFileName]) #not the most readable, but this is the output path/name
		#write union_list to the output file as a single column of data
		with open(completeOutPath, 'w') as outFile:
			for item in union_list:
				outFile.write(item + '\n')

#ITEMS UNIQUE TO EACH OF N LISTS
elif "-o" in arguments_list:
	inPaths_list = list(arguments_list)
	#remove python program file and selection arguments from arguments list
	temp_pathsList = list(inPaths_list)
	for path in temp_pathsList:
		if (path == '-o') or ('.py' in path):
			inPaths_list.remove(path)
	if len(inPaths_list) < 2: #user must specify at least two input files for this option
		print('\nUser must specify at least two lists in order to find the uniques.')
	else:
		print("\nYou chose to find the unnique values from " + str(len(inPaths_list)) + " lists.")
		contents_dict = getContents(inPaths_list) #read the input files into a dictionary
		union_list = [] #will fill this with intersection data only
		for key, val in contents_dict.iteritems(): #for each input file's list data
			unique_list = list(val)
			temp_dict = contents_dict.copy()
			del temp_dict[key] #we want to check current list against all other lists, but not itself
			for key2, val2 in temp_dict.iteritems(): #go through all the lists except the current list of interest
				unique_list = [item for item in unique_list if item not in val2] #keep only those that are unique to unique_list
			outFilePath = key.replace(".txt", "_uniques.txt")
			with open(outFilePath, 'w') as outFile:
				for item in unique_list:
					outFile.write(item + '\n')

#SET OF ONE LIST
elif "-s" in arguments_list:
	print('\nYou have chosen to take the set of a single list.')
	inPath = ''
	for argument in arguments_list:
		if ('.py' not in argument) and ('-s' not in argument):
			inPath = str(argument) #deep copy
	outList = []
	with open(inPath, 'r') as inFile:
		for line in inFile:
			outList.append(line.strip('\n'))
	outSet = set(outList)
	outPath = inPath.replace(".txt", "_set.txt")
	with open(outPath, 'w') as outFile:
		for item in outSet:
			outFile.write(item.upper() + '\n')	