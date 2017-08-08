import sys
sys.path.append('../dependencies')
import time
import os
import cv2
import numpy as np
import constants as const
from functions import key_check, grab_screen, PressKey, ReleaseKey, countdown, prompt_quit

model = alexnet(const.WIDTH, const.HEIGHT, const.LEARNING_RATE)
model.load(MODEL_NAME)

def straight():
	PressKey(const.W)
	ReleaseKey(const.A)
	ReleaseKey(const.D)


def left():
	PressKey(const.A)
	PressKey(const.W)
	ReleaseKey(const.D)
	time.sleep(const.TIME)
	ReleaseKey(const.A)


def right():
	PressKey(const.D)
	PressKey(const.W)
	ReleaseKey(const.A)
	time.sleep(const.TIME)
	ReleaseKey(const.D)


def main():
	countdown(4)

	PAUSED = False
	
	while True:
		if not PAUSED:
			screen = grab_screen(region=(0, 40, 800, 640))
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			screen = cv2.resize(screen, (const.WIDTH, const.HEIGHT))

			# prediction
			prediction = model.predict([screen.reshape(const.WIDTH, const.HEIGHT, 1)])[0]
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

		if 'P' in keys:
			if PAUSED:
				print("Unpausing...")
				PAUSED = False
				time.sleep(1)
			else:
				PAUSED = True
				ReleaseKey(const.A)
				ReleaseKey(const.W)
				ReleaseKey(const.D)
				print("Pausing...")
				time.sleep(1)
				print("Paused")
				prompt_quit()
				print('Press (p) to unpause')


main()