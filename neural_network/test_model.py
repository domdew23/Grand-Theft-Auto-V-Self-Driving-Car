import sys

sys.path.append('../functions')
from get_keys import key_check
from grab_screen import grab_screen
from alexnet import alexnet
from direct_keys import PressKey, ReleaseKey, W, A, S, D

import time
import os
import cv2
import numpy as np

WIDTH = 80
HEIGHT = 60
LEARNING_RATE  = .001
EPOCHS = 8
MODEL_NAME = 'pygta5-car-{}-{}-{}-epochs.model'.format(LEARNING_RATE, 'alexnetv2', EPOCHS)

def straight():
	PressKey(W)
	ReleaseKey(A)
	ReleaseKey(D)

def left():
	PressKey(A)
	PressKey(W)
	ReleaseKey(D)

def right():
	PressKey(D)
	PressKey(W)
	ReleaseKey(D)

def slow_down():
	ReleaseKey(W)
	ReleaseKey(A)
	ReleaseKey(D)


def countdown(seconds):
	for i in list(range(seconds)) [::-1]:
		print(i + 1)
		time.sleep(1)


model = alexnet(WIDTH, HEIGHT, LEARNING_RATE)
model.load(MODEL_NAME)

STRAIGHT = [0, 1, 0]
LEFT = [1, 0, 0]
RIGHT = [0, 0, 1]


def main():
	countdown(4)

	PAUSED = False
	
	while True:
		if not PAUSED:
			screen = grab_screen(region=(0, 40, 800, 640))
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			screen = cv2.resize(screen, (80,60))
			# prediction
			prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
			moves = list(np.around(prediction))
			print(moves, prediction)

			if moves == LEFT:
				left()
			elif moves == STRAIGHT:
				straight()
			elif moves == RIGHT:
				right()

		keys = key_check()

		if 'T' in keys:
			if PAUSED:
				PAUSED = False
				time.sleep(1)
			else:
				PAUSED = True
				ReleaseKey(A)
				ReleaseKey(W)
				ReleaseKey(D)
				time.sleep(1)


main()