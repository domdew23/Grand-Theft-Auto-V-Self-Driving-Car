import time
import os
import cv2
import numpy as np
import sys

sys.path.append('../functions')
from get_keys import key_check
from grab_screen import grab_screen

# neural network:
# input is pixel data
# output is the movements
# input data is to manually drive and train data based off that

FILE_NAME = '../data/training_data.npy'

def keys_to_output(keys):
	# [A, W, D] (left, straight, right)
	output = [0, 0, 0]
	if 'A' in keys:
		output[0] = 1
	elif 'D' in keys:
		output[2] = 1
	else:
		output[1] = 1

	return output


def countdown(seconds):
	for i in list(range(seconds)) [::-1]:
		print(i + 1)
		time.sleep(1)


def get_file():
	if os.path.isfile(FILE_NAME):
		print("File exists, loading previous data")
		training_data = list(np.load(FILE_NAME))
	else:
		print("File does not exist, creating file...")
		training_data = []

	return training_data

def main():
	start_time = time.time() 

	training_data = get_file()

	print("Took || {}{}{} seconds to load data".format('{', time.time()- start_time, '}'))

	countdown(4)

	PAUSED = False

	while True:
		if not PAUSED:
			start_time = time.time() 
			screen = grab_screen(region=(0, 40, 800, 640))
			# scale down to grayscale
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			screen = cv2.resize(screen, (160,120))
			
			# grab data
			keys = key_check()
			output = keys_to_output(keys)
			training_data.append([screen, output])

			length = len(training_data)

			if length % 100000 == 0:
				save_time = time.time()
				print("Saving... || training_data length: {}".format(length))
				np.save(FILE_NAME, training_data)
				print("Took || {}{:.2f}{} minutes to save".format('{', (time.time()- save_time) / 60, '}'))
				cont = input("Would you like to cointue training or exit? \nPress y to continue or n to exit.")
					if cont == 'n':
						sys.exit()


			print("Not Paused Loop took: {}{:.3f}{} seconds || training_data length: {}".format('{', time.time()- start_time, '}', length))
		
		keys = key_check()

		if 'T' in keys:
			if PAUSED:
				print('Unpausing...')
				PAUSED = False
				time.sleep(1)
			else:
				print('Pausing...')
				PAUSED = True
				time.sleep(1)
				print('Paused')
				print("training_data length: {}".format(len(training_data)))



main()