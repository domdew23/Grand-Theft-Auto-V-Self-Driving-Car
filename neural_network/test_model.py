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

WIDTH = 160
HEIGHT = 120
LEARNING_RATE  = .001
EPOCHS = 10
MODEL_NAME = 'pygta5-car-{}-{}-{}-epochs.model'.format(LEARNING_RATE, 'alexnetv2', EPOCHS)
TIME = 0.09

model = alexnet(WIDTH, HEIGHT, LEARNING_RATE)
model.load(MODEL_NAME)


def straight():
	PressKey(W)
	ReleaseKey(A)
	ReleaseKey(D)


def left():
	PressKey(A)
	PressKey(W)
	ReleaseKey(D)
	time.sleep(TIME)
	ReleaseKey(A)


def right():
	PressKey(D)
	PressKey(W)
	ReleaseKey(A)
	time.sleep(TIME)
	ReleaseKey(D)


def countdown(seconds):
	for i in list(range(seconds)) [::-1]:
		print(i + 1)
		time.sleep(1)


def main():
	countdown(4)

	PAUSED = False
	
	while True:
		if not PAUSED:
			screen = grab_screen(region=(0, 40, 800, 640))
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			screen = cv2.resize(screen, (WIDTH,HEIGHT))

			# prediction
			prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
			print(prediction)

			turn_treshold = .75
			fwd_threshold = .70

			LEFT = prediction[0]
			STRAIGHT = prediction[1]
			RIGHT = prediction[2]

			if  STRAIGHT > fwd_threshold:
				straight()
			elif LEFT > turn_treshold:
				left()
			elif RIGHT > turn_treshold:
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