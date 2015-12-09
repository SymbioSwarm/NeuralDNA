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
tar = tarfile.open("LEVANT_.tar")
sequence = ""
NUM_TRAINING_EXAMPLES = 19
INTERVAL_SIZE=800;
CAPPED_SIZE = 150;
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
	if tar_list[counter][4:] == "NEG" or tar_list[counter][3:] == "NEG" or tar_list[counter][2:] == "NEG":
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

weights_level0 = 2*np.random.random((CAPPED_SIZE, NUM_TRAINING_EXAMPLES)) - 1
weights_level1 = 2*np.random.random((NUM_TRAINING_EXAMPLES, 21)) -1
weights_level2 = 2*np.random.random((21,15)) - 1
weights_level3 = 2*np.random.random((15,1)) -1

#print weights_level0
#time.sleep(30)
#print "initial weights: ", weights
#print "length of weights: ", len(weights)

truth = np.array(true_output)
#x = np.array(training_input, dtype=(np.int32, 10))
#previous = np.zeros((100,1))	
my_array = np.empty((len(training_input), CAPPED_SIZE))
for i, x in enumerate(training_input):
    my_array[i] = x

#print my_array.shape
#print my_array
#print truth
learning_rate = 0.6
#def calculate_NN(sequence_list, correct_output_array):
#time.sleep(10)
for iterator in xrange(1000):
	layer0 = my_array
	prediction_layer1 = sigmoid(np.dot(layer0, weights_level0))
	#print prediction_layer1
	#time.sleep(5)
	prediction_layer2 = sigmoid(np.dot(prediction_layer1, weights_level1))
	prediction_layer3 = sigmoid(np.dot(prediction_layer2, weights_level2))	
	prediction_layer4 = sigmoid(np.dot(prediction_layer3, weights_level3))

	print "prediction: ", prediction_layer4
	prediction_layer4_error = truth - prediction_layer4 
	#print error
	#print "error: ",error
	layer4_delta = prediction_layer4_error * sigmoid(prediction_layer4, deriv=True)
	prediction_layer3_error = np.dot(layer4_delta, weights_level3.T)
	layer3_delta = prediction_layer3_error * sigmoid(prediction_layer3, deriv=True)

	#Simple Backpropogation of weights to previous layers
	prediction_layer2_error = np.dot(layer3_delta, weights_level2.T)	
	layer2_delta = prediction_layer2_error * sigmoid(prediction_layer2, deriv=True)
	prediction_layer1_error = np.dot(layer2_delta, weights_level1.T)
	layer1_delta = prediction_layer1_error * sigmoid(prediction_layer1, deriv=True)

	weights_level0 += np.dot(layer0.T, layer1_delta)
	weights_level1 += np.dot(prediction_layer1.T, layer2_delta) * learning_rate
	weights_level2 += np.dot(prediction_layer2.T, layer3_delta) * learning_rate
	weights_level3 += np.dot(prediction_layer3.T, layer4_delta) * learning_rate
	print iterator
	#print weights
	#difference = weights - previous
	#print difference
	#previous = weights
	time.sleep(.001)
print weights_level3


def predict(interval_size, capped_size):
	with open(str(sys.argv[1])) as input_file:
		input_file.readline() #get first line
		sequence = ""
		for line in input_file:
			#get the sequence into the GC placement
			sequence += line.rstrip('\n')
		sample_list = sample_nth(sequence, interval_size)
		sample_list = sample_list[:capped_size]
		sample_list = convert_to_GC_placement(sample_list)
			
			#push through the network
		layer0 = sample_list
		prediction_layer1 = sigmoid(np.dot(layer0, weights_level0))
		prediction_layer2 = sigmoid(np.dot(prediction_layer1, weights_level1))
		prediction_layer3 = sigmoid(np.dot(prediction_layer2, weights_level2))
		prediction_layer4 = sigmoid(np.dot(prediction_layer3, weights_level3))
		print prediction_layer4



predict(INTERVAL_SIZE, CAPPED_SIZE)