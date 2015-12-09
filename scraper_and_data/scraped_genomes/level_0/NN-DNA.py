import sys
from GC_content import calculate_gc_content
import numpy as np


num_files = int(raw_input('Input number of files:'))



#converts sequence into integers as input to NN as a list
def convert_to_integer(sequence):
	return_list = []
	for letter in sequence:
		if letter == 'A':
			return_list.append(1)
		elif letter == 'T':
			return_list.append(2)
		elif letter == 'G':
			return_list.append(3)
		else:
			return_list.append(4)
	return return_list



sequence = "";
for n_file in range(num_files):
	with open(str(sys.argv[n_file+1])) as input_file:
		#get the first garbage line
		line = input_file.readline()
		for line in input_file:
			#print line
			sequence += line
		print "length: ", len(sequence)
		print "gc content: ", calculate_gc_content(sequence)
		num_list = convert_to_integer(sequence)
		print num_list


np.random.seed(1)


initial_weights = 2*np.random.random((10000,1)) - 1
print "initial weights: ", initial_weights
y = np.array([[1],
			[1],
			[1],
			[0]])	






#def calculate_NN(sequence_list, correct_output_array):
