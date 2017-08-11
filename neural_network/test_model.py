import sys
sys.path.append('../dependencies')
import time
import os
import cv2
import numpy as np

from settings import WIDTH, HEIGHT, LEARNING_RATE, MODEL_NAME, W, A, S, D, TIME
from functions import key_check, grab_screen, PressKey, ReleaseKey, countdown, prompt_quit
from alexnet import alexnet

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


def main():
	countdown(4)

	PAUSED = False
	
	while True:
		if not PAUSED:
			screen = grab_screen(region=(0, 40, 800, 640))
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			screen = cv2.resize(screen, (WIDTH, HEIGHT))

			# prediction
			prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]

			turn_treshold = .75
			fwd_threshold = .70

			LEFT = prediction[0]
			STRAIGHT = prediction[1]
			RIGHT = prediction[2]

			if  STRAIGHT > fwd_threshold:
				straight()
				print(" {} || Straight".format(prediction))
			elif LEFT > turn_treshold:
				left()
				print("{} || Left".format(prediction))
			elif RIGHT > turn_treshold:
				right()
				print("{} || Right".format(prediction))
		keys = key_check()

		if 'P' in keys:
			if PAUSED:
				print("Unpausing...")
				PAUSED = False
				time.sleep(1)
			else:
				PAUSED = True
				ReleaseKey(A)
				ReleaseKey(W)
				ReleaseKey(D)
				print("Pausing...")
				time.sleep(1)
				print("Paused")
				
main()