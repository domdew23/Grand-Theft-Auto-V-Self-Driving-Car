import numpy as np
from PIL import ImageGrab
import cv2
import time

from direct_keys import PressKey, ReleaseKey, W, A, S, D


def countdown(seconds):
	for i in list(range(seconds)) [::-1]:
		print(i + 1)
		time.sleep(1)

# Use opencv to find lanes in a road, then put those lanes back on original image
def process_img(original_image):
	# Determine wheather or not car is in a lane

	# Convert to gray to have simplier data
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
	return processed_img

def move():
	print('down')
	PressKey(W)
	#countdown(3)
	#print('up')
	#ReleaseKey(W)

# Track the time between frames
last_time = time.time()

countdown(4)
while(True):

	# Grab image off the screen
	#print_screen_pil = ImageGrab.grab(bbox=(0,40, 800, 640))
	screen = np.array(ImageGrab.grab(bbox=(0,40, 800, 640)))
	new_screen = process_img(screen)

	move()

	print('Loop took {' + format(time.time() - last_time) + '} seconds')
	last_time = time.time()

	#cv2.waitKey(1)
	# Display image on the screen
	# cv2.imshow('window', cv2.cvtColor(np.array(print_screen_pil), cv2.COLOR_BGR2RGB))
	cv2.imshow('window', new_screen)
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
