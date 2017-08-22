import sys
sys.path.append('../dependencies')
import time
import os
import cv2
import numpy as np
import random
from models import inception_v3 as googlenet
from collections import deque, Counter
from settings import WIDTH, HEIGHT, LEARNING_RATE, MODEL_NAME, W, A, S, D, TIME
from functions import key_check, grab_screen, PressKey, ReleaseKey, countdown, prompt_quit
from motion import motion_detection
from statistics import mode, mean
GAME_WIDTH = 1920
GAME_HEIGHT = 1080

how_far_remove = 800
rs = (20, 15)
log_len = 25

motion_req = 800
motion_log = deque(maxlen=log_len)

choices = deque([], maxlen=5)
hl_hist = 250
choice_hist = deque([], maxlen=hl_hist)

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

def straight():
	PressKey(W)
	ReleaseKey(A)
	ReleaseKey(D)
	ReleaseKey(S)

def left():
	if random.randrange(0,3) == 1:
		PressKey(W)
	else:
		ReleaseKey(W)
	PressKey(A)
	ReleaseKey(S)
	ReleaseKey(D)

def right():
	if random.randrange(0,3) == 1:
		PressKey(W)
	else:
		ReleaseKey(W)
	PressKey(D)
	ReleaseKey(A)
	ReleaseKey(S)


def reverse():
	PressKey(S)
	ReleaseKey(A)
	ReleaseKey(W)
	ReleaseKey(D)


def forward_left():
	PressKey(W)
	PressKey(A)
	ReleaseKey(D)
	ReleaseKey(S)


def forward_right():
	PressKey(W)
	PressKey(D)
	ReleaseKey(A)
	ReleaseKey(S)


def reverse_left():
	PressKey(S)
	PressKey(A)
	ReleaseKey(W)
	ReleaseKey(D)


def reverse_right():
	PressKey(S)
	PressKey(D)
	ReleaseKey(W)
	ReleaseKey(A)


def no_keys():
	if random.randrange(0,3) == 1:
		PressKey(W)
	else:
		ReleaseKey(W)
	ReleaseKey(A)
	ReleaseKey(S)
	ReleaseKey(D)

model = googlenet(WIDTH, HEIGHT, 3, LEARNING_RATE, output=9)
model.load(MODEL_NAME)
print("Loaded model")

def predict(mode_choice):
	if mode_choice == 0:
		straight()
		choice_picked = 'straight'
	elif mode_choice == 1:
		reverse()
		choice_picked = 'reverse'
	elif mode_choice == 2:
		left()
		choice_picked = 'left'
	elif mode_choice == 3:
		right()
		choice_picked = 'right'
	elif mode_choice == 4:
		forward_left()
		choice_picked = 'foward-left'
	elif mode_choice == 5:
		forward_right()
		choice_picked = 'foward-right'
	elif mode_choice == 8:
		no_keys()
		choice_picked = 'no-keys'
	return choice_picked


def predict_2(prediction):
	if np.argmax(prediction) == np.argmax(w):
		straight()
		choice_picked = 'straight'
	elif np.argmax(prediction) == np.argmax(s):
		reverse()
		choice_picked = 'reverse'
	elif np.argmax(prediction) == np.argmax(a):
		left()
		choice_picked = 'left'
	elif np.argmax(prediction) == np.argmax(d):
		right()
		choice_picked = 'right'
	elif np.argmax(prediction) == np.argmax(wa):
		forward_left()
		choice_picked = 'straight_left'
	elif np.argmax(prediction) == np.argmax(wd):
		forward_right()
		choice_picked = 'straight_right'
	elif np.argmax(prediction) == np.argmax(nk):
		no_keys()
		choice_picked = 'no_keys'
	return choice_picked


def main():
	countdown(4)

	PAUSED = False
	mode_choice = 0

	screen = grab_screen(region=(0, 40, GAME_WIDTH, GAME_HEIGHT + 40))
	screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
	prev = cv2.resize(screen, (WIDTH, HEIGHT))

	t_minus = prev
	t_now = prev
	t_plus = prev

	while True:
		if not PAUSED:
			start_time = time.time()
			screen = grab_screen(region=(0, 40, GAME_WIDTH, GAME_HEIGHT + 40))
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
			screen = cv2.resize(screen, (WIDTH, HEIGHT))

			delta_count = motion_detection(t_minus, t_now, t_plus)

			t_minus = t_now
			t_now = t_plus
			t_plus = screen
			t_plus = cv2.blur(t_plus,(4,4))

			# prediction
			prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 3)])[0]
			prediction = np.array(prediction) * np.array([4.5, 0.1, 0.1, 0.1,  1.8, 1.8, 0.5, 0.5, 0.2])

			mode_choice = np.argmax(prediction)
			print("Prediction: {}".format(np.around(prediction, decimals=4)))

			choice_picked = predict(mode_choice)

			motion_log.append(delta_count)
			motion_avg = round(mean(motion_log), 3)
			print("Loop took {} seconds || Motion: {} || Choice: {}".format(
				round(time.time() - start_time, 3), motion_avg, choice_picked))

			if motion_avg < motion_req and len(motion_log) >= log_len:
				print("We are probably stuck, begining evasive maneuvers")

				# 0 = reverse straight, turn left out
				# 1 = reverse straight, turn right out
				# 2 = reverse left, turn right out
				# 3 = reverse right, turn left out

				quick_choice = random.randrange(0, 4)

				if quick_choice == 0:
					reverse()
					time.sleep(random.uniform(1,2))
					forward_left()
					time.sleep(random.uniform(1,2))

				elif quick_choice == 1:
					reverse()
					time.sleep(random.uniform(1,2))
					forward_right()
					time.sleep(random.uniform(1,2))

				elif quick_choice == 2:
					reverse_left()
					time.sleep(random.uniform(1,2))
					forward_right()
					time.sleep(random.uniform(1,2))

				elif quick_choice == 3:
					reverse_right()
					time.sleep(random.uniform(1,2))
					forward_left()
					time.sleep(random.uniform(1,2))

				for i in range(log_len-2):
					del motion_log[0]

		keys = key_check()

		if 'Q' in keys:
			sys.exit()

		if 'T' in keys:
			if PAUSED:
				print("Unpausing...")
				PAUSED = False
				time.sleep(1)
			else:
				PAUSED = True
				ReleaseKey(A)
				ReleaseKey(W)
				ReleaseKey(D)
				ReleaseKey(S)
				print("Pausing...")
				time.sleep(1)
				print("Paused")
				
main()