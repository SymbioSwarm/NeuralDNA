import sys
from GC_content import calculate_gc_content
import numpy as np
import tarfile
import time


def sigmoid(x,deriv=False):
	if(deriv==True):
	    return x*(1-x)

	return 1/(1+np.exp(-x))


def convert_to_integer(sequence):
	return_list = []
	for letter in sequence:
		if letter == 'A':
			return_list.append(-10)
		elif letter == 'T':
			return_list.append(1)
		elif letter == 'G':
			return_list.append(10)
		else:
			return_list.append(20)
	return return_list


def convert_to_GC_placement(sequence):
	return_list = []
	for letter in sequence:
		if letter == 'A':
			return_list.append(0)
		elif letter == 'T':
			return_list.append(0)
		elif letter == 'G':
			return_list.append(1)
		else:
			return_list.append(1)
	return return_list





#samples n values from a given sequence, at equal intervals.  
def sample_nth(sequence, n):
	return_list = []
	count = 0
	interval_size = n
	print interval_size
	while count < len(sequence):
		return_list.append(sequence[count])
		count += interval_size
	return return_list	

#num_files = int(raw_input('Input number of files:'))
tar = tarfile.open("CHINA_.tar")
sequence = ""
INTERVAL_SIZE=1000;
CAPPED_SIZE = 100;
sample_list = ""
tar_list = tar.getnames()
counter = 0
true_output = []
training_input = []
for n_file in tar.getmembers():
	#with open(str(sys.argv[n_file])) as input_file:
	#get the first garbage line
	input_file = tar.extractfile(n_file)
	line = input_file.readline()
	for line in input_file:
		#print line
		sequence += line.rstrip('\n')
	print "length: ", len(sequence)
	print "gc content: ", calculate_gc_content(sequence)
	if tar_list[counter][4:] == "NEG":
		true_output.append([0])
	else:
		true_output.append([1])
	sample_list = sample_nth(sequence, INTERVAL_SIZE)
	sample_list = sample_list[:CAPPED_SIZE] #cut off the end to make the number of "features" equal
	print "samplemple list length: ", len(sample_list)
	sequence = ""
	while len(sample_list) < CAPPED_SIZE:
		sample_list.append(0)

	training_input.append(convert_to_GC_placement(sample_list))
	counter += 1


#print sample_list
#print convert_to_integer(sample_list)
np.random.seed(1)
print "training input: ",len(training_input)
print "training_input[0]: ",len(training_input[1])
#print training_input

weights_level0 = 2*np.random.random((100, 39)) - 1
weights_level1 = 2*np.random.random((100,1)) - 1

#print weights_level0
#time.sleep(6)
#print "initial weights: ", weights
#print "length of weights: ", len(weights)

truth = np.array(true_output)
#x = np.array(training_input, dtype=(np.int32, 10))
previous = np.zeros((100,1))	
my_array = np.empty((len(training_input), 100))
for i, x in enumerate(training_input):
    my_array[i] = x

print my_array.shape
print my_array
print truth

#def calculate_NN(sequence_list, correct_output_array):
#time.sleep(10)
for iterator in xrange(1000):
	l0 = my_array
	prediction = sigmoid(np.dot(l0, weights_level1))
	print "prediction: ", prediction
	error = truth - prediction 
	#print error
	#print "error: ",error
	delta = error * sigmoid(prediction, deriv=True)
	#print "delta: ",np.dot(my_array.T, delta)
	weights_level1 += np.dot(l0.T, delta)
	print iterator
	#print weights_level1
	#difference = weights - previous
	#print difference
	#previous = weights
	time.sleep(.1)
print weights_level1