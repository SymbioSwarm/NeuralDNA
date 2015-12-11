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


#initialize weight dictionary for each region
weights_level0_all = {'S-America' : [], 
					  'N-America' : [],
					  'Levant' : [],
					  'E-Asia' : [],
					  'Australia' : [],
					  'C-America:' : [],
					  'Sub-Africa' : [],
					  'W-Europe' : [],
					  'SSE-Asia' : []
					  };
weights_level1_all = {'S-America' : [], 
					  'N-America' : [],
					  'Levant' : [],
					  'E-Asia' : [],
					  'Australia' : [],
					  'C-America:' : [],
					  'Sub-Africa' : [],
					  'W-Europe' : [],
					  'SSE-Asia' : []
					  };
weights_level2_all = {'S-America' : [], 
					  'N-America' : [],
					  'Levant' : [],
					  'E-Asia' : [],
					  'Australia' : [],
					  'C-America:' : [],
					  'Sub-Africa' : [],
					  'W-Europe' : [],
					  'SSE-Asia' : []
					  };
weights_level3_all = {'S-America' : [], 
					  'N-America' : [],
					  'Levant' : [],
					  'E-Asia' : [],
					  'Australia' : [],
					  'C-America:' : [],
					  'Sub-Africa' : [],
					  'W-Europe' : [],
					  'SSE-Asia' : []
					  };




#samples n values from a given sequence, at equal intervals.  
def sample_nth(sequence, n):
	return_list = []
	count = 0
	interval_size = n
	#print interval_size
	while count < len(sequence):
		return_list.append(sequence[count])
		count += interval_size
	return return_list	


#trains the feed-forward NN with backpropogation and 4 hidden layers.
#	
def train_NN(NUM_TRAINING_EXAMPLES, dictname, tarname):
	tar = tarfile.open(tarname)	
	sequence = ""
	
	INTERVAL_SIZE=450;
	CAPPED_SIZE = 250;
	sample_list = ""
	tar_list = tar.getnames()
	counter = 0
	true_output = []
	training_input = []
	for n_file in tar.getmembers():
		
		#get the first garbage line
		input_file = tar.extractfile(n_file)
		line = input_file.readline()
		for line in input_file:
			#this is because the files have newline characters for each printable line.  Need to add them together to one string.
			sequence += line.rstrip('\n')
		
		if tar_list[counter][4:] == "NEG" or tar_list[counter][3:] == "NEG" or tar_list[counter][2:] == "NEG":
			true_output.append([0])
		else:
			true_output.append([1])
		sample_list = sample_nth(sequence, INTERVAL_SIZE)
		sample_list = sample_list[:CAPPED_SIZE] #cut off the end to make the number of "features" equal
		
		sequence = ""
		while len(sample_list) < CAPPED_SIZE:
			sample_list.append(0)

	    #convert A, C, T, G to 0,1 for GC placement
		training_input.append(convert_to_GC_placement(sample_list))
		counter += 1


	np.random.seed(1)
	
	#initialize weights to random values with mean 0 
	weights_level0 = 2*np.random.random((CAPPED_SIZE, NUM_TRAINING_EXAMPLES)) - 1
	weights_level1 = 2*np.random.random((NUM_TRAINING_EXAMPLES, 21)) -1
	weights_level2 = 2*np.random.random((21,15)) - 1
	weights_level3 = 2*np.random.random((15,1)) -1

	#this is due to a weird issue with numpy.  All this does is put the training input into a 2D numpy matrix
	truth = np.array(true_output)
	my_array = np.empty((len(training_input), CAPPED_SIZE))
	for i, x in enumerate(training_input):
	    my_array[i] = x
	

	#learning rate: an alterable parameter that says how fast the NN moves down the gradient descent
	learning_rate = 0.4
	for iterator in xrange(2000):
		layer0 = my_array
		
		#feed the inputs through the network
		prediction_layer1 = sigmoid(np.dot(layer0, weights_level0))
		prediction_layer2 = sigmoid(np.dot(prediction_layer1, weights_level1))
		prediction_layer3 = sigmoid(np.dot(prediction_layer2, weights_level2))	
		prediction_layer4 = sigmoid(np.dot(prediction_layer3, weights_level3))
		print prediction_layer4
		print iterator
		print dictname
		#get the error for each layer
		prediction_layer4_error = truth - prediction_layer4 
	
		layer4_delta = prediction_layer4_error * sigmoid(prediction_layer4, deriv=True)
		prediction_layer3_error = np.dot(layer4_delta, weights_level3.T)
		layer3_delta = prediction_layer3_error * sigmoid(prediction_layer3, deriv=True)

		#Simple Backpropogation of weights to previous layers
		prediction_layer2_error = np.dot(layer3_delta, weights_level2.T)	
		layer2_delta = prediction_layer2_error * sigmoid(prediction_layer2, deriv=True)
		prediction_layer1_error = np.dot(layer2_delta, weights_level1.T)
		layer1_delta = prediction_layer1_error * sigmoid(prediction_layer1, deriv=True)

		#update the weights
		weights_level0 += np.dot(layer0.T, layer1_delta)
		weights_level1 += np.dot(prediction_layer1.T, layer2_delta) * learning_rate
		weights_level2 += np.dot(prediction_layer2.T, layer3_delta) * learning_rate
		weights_level3 += np.dot(prediction_layer3.T, layer4_delta) * learning_rate
		
		#time.sleep(.00001)
	
	weights_level0_all[dictname] = weights_level0
	weights_level1_all[dictname] = weights_level1
	weights_level2_all[dictname] = weights_level2
	weights_level3_all[dictname] = weights_level3

def predict(interval_size, capped_size, dictname, filename):
	
	with open(filename) as input_file:
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
		prediction_layer1 = sigmoid(np.dot(layer0, weights_level0_all[dictname]))
		prediction_layer2 = sigmoid(np.dot(prediction_layer1, weights_level1_all[dictname]))
		prediction_layer3 = sigmoid(np.dot(prediction_layer2, weights_level2_all[dictname]))
		prediction_layer4 = sigmoid(np.dot(prediction_layer3, weights_level3_all[dictname]))
		print "{0} percent chance of belonging to {1}".format(prediction_layer4[0] * 100, dictname)

def predict_openfile(interval_size, capped_size, dictname, openfile):
	
	openfile.readline() #get first line
	sequence = ""
	for line in openfile:
		#get the sequence into the GC placement
		sequence += line.rstrip('\n')
	sample_list = sample_nth(sequence, interval_size)
	sample_list = sample_list[:capped_size]
	sample_list = convert_to_GC_placement(sample_list)
	while len(sample_list) < capped_size:
			sample_list.append(0)

	#push through the network
	layer0 = sample_list
	prediction_layer1 = sigmoid(np.dot(layer0, weights_level0_all[dictname]))
	prediction_layer2 = sigmoid(np.dot(prediction_layer1, weights_level1_all[dictname]))
	prediction_layer3 = sigmoid(np.dot(prediction_layer2, weights_level2_all[dictname]))
	prediction_layer4 = sigmoid(np.dot(prediction_layer3, weights_level3_all[dictname]))
	print "{0} percent chance of belonging to {1}".format(prediction_layer4[0] * 100, dictname)




def predict_batch_list(file_list, interval_size, capped_size):
	for input_file in file_list:

		#input_file = "/Testing/" + input_file
		print "Ground truth region: ", input_file

		predict(interval_size, capped_size, 'S-America', input_file)
		predict(interval_size, capped_size, 'C-America', input_file)
		predict(interval_size, capped_size, 'E-Asia', input_file)
		predict(interval_size, capped_size, 'Sub-Africa', input_file)
		predict(interval_size, capped_size, 'Levant', input_file)
		predict(interval_size, capped_size, 'SSE-Asia', input_file)
		predict(interval_size, capped_size, 'N-America', input_file)
		predict(interval_size, capped_size, 'W-Europe', input_file)
		predict(interval_size, capped_size, 'Australia', input_file)

		print
		print
		print




def predict_batch(tar_filename, interval_size, capped_size):
	tar = tarfile.open(tar_filename)	
	tar_list = tar.getnames()
	counter = 0
	for n_file in tar.getmembers():
		curr_file = tar_list[counter]

		input_file = tar.extractfile(n_file)
		print "Ground truth region: ", curr_file
		#predict_openfile(interval_size, capped_size, 'S-America', input_file)
		#predict_openfile(interval_size, capped_size, 'C-America', input_file)
		#predict_openfile(interval_size, capped_size, 'E-Asia', input_file)
		#predict_openfile(interval_size, capped_size, 'Sub-Africa', input_file)
		#predict_openfile(interval_size, capped_size, 'Levant', input_file)
		#predict_openfile(interval_size, capped_size, 'SSE-Asia', input_file)
		#predict_openfile(interval_size, capped_size, 'N-America', input_file)
		#predict_openfile(interval_size, capped_size, 'W-Europe', input_file)
		#predict_openfile(interval_size, capped_size, 'Australia', input_file)

		predict_openfile(interval_size, capped_size, 'S-America', input_file)
		predict_openfile(interval_size, capped_size, 'C-America', input_file)
		predict_openfile(interval_size, capped_size, 'E-Asia', input_file)
		predict_openfile(interval_size, capped_size, 'Sub-Africa', input_file)
		predict_openfile(interval_size, capped_size, 'Levant', input_file)
		predict_openfile(interval_size, capped_size, 'SSE-Asia', input_file)
		predict_openfile(interval_size, capped_size, 'N-America', input_file)
		predict_openfile(interval_size, capped_size, 'W-Europe', input_file)
		predict_openfile(interval_size, capped_size, 'Australia', input_file)




		print
		print
		print

		counter = counter + 1



train_NN(91, 'Australia', "Australia.tar")
train_NN(27, 'C-America', "C_America.tar")
train_NN(98, 'E-Asia', "East_Asia.tar")
train_NN(19, 'Sub-Africa', "Subsaharan_Africa.tar")
train_NN(31, 'Levant', "Levant.tar")
train_NN(30, 'N-America', "N_America.tar")
train_NN(20, 'SSE-Asia', "SE_Asia.tar")
train_NN(30, 'S-America', "S_America.tar")
train_NN(11, 'W-Europe', "Western_Europe.tar")

test_list = ["Testing_1_S_America.txt", "Testing_2_N_America.txt", "Testing_3_N_America.txt", "Testing_4_Australia.txt",
   			"Testing_5_SSAfrica.txt", "Testing_6_EAsia.txt", "Testing_7_Australia.txt", "Testing_8_EAsia.txt", "Testing_9_EAsia.txt",
   			"Testing_10_Australia.txt", "Testing_11_EAsia_INVASIVE.txt", "Testing_11_Europe.txt", "Testing_12_EAsia.txt", 
   			"Testing_13_N_America.txt", "Testing_14_C_America.txt", "Testing_15_Australia.txt", "Testing_16_SSAfrica.txt", 
   			"Testing_17_C_America.txt"]

#predict(700, 150, 'S-America', "138")
#predict(700, 150, 'C-America', "138")
#predict(700, 150, 'E-Asia', "138")
#predict(700, 150, 'Sub-Africa', "138")
#predict(700, 150, 'Levant', "138")
#predict(700, 150, 'SSE-Asia', "138")
#predict(700, 150, 'N-America', "138")
#predict(700, 150, 'W-Europe', "138")
#predict(700, 150, 'Australia', "138")
#predict_batch(str(sys.argv[1]), 700, 150)
predict_batch_list(test_list, 450, 250)
