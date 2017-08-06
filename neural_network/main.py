import sys

sys.path.append('../functions')
from get_keys import key_check
from grab_screen import grab_screen

import time
import os
import cv2
import numpy as np

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


if os.path.isfile(FILE_NAME):
	print("File exists, loading previous data")
	training_data = list(np.load(FILE_NAME))
else:
	print("File does not exist, creating file...")
	training_data = []


def main():
	countdown(4)

	#last_time = time.time()

	while True:
		screen = grab_screen(region=(0, 40, 800, 640))
		# scale down to grayscale
		screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		screen = cv2.resize(screen, (80,60))
		# grab data
		keys = key_check()
		output = keys_to_output(keys)
		training_data.append([screen, output])

		#print('Loop took {' + format(time.time() - last_time) + '} seconds')
		#last_time = time.time()

		if len(training_data) % 1000 == 0:
			print(len(training_data))
			np.save(FILE_NAME, training_data)

main()