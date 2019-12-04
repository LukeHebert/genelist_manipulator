'''
Authors: Luke Hebert, Craig Baker, Paul Hillman
Description: takes two .txt files each containing one gene per line; ouputs the intersections of both gene lists
'''

import sys

file1_str, file2_str, outFile_str = sys.argv[1], sys.argv[2], sys.argv[3]

file1_list = []
with open(file1_str) as file1:
	for line in file1:
		line = line.strip('\r').strip('\n')
		file1_list.append(line)

file2_list = []
with open(file2_str) as file2:
	for line in file2:
		line = line.strip('\r').strip('\n')
		file2_list.append(line)
		
file1_set, file2_set = set(file1_list), set(file2_list)

overlap_list = [gene for gene in file1_set if gene in file2_set]

with open(outFile_str, 'w') as outFile:
	for gene in overlap_list:
		outFile.write(gene + '\n')
