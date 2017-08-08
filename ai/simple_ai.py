import sys
sys.path.append('../dependencies')
import cv2
import time
import pyautogui
import numpy as np

from functions import direct_keys, grab_screen, draw_lanes
from constants import W, A, S, D


def roi(image, vertices):
	# Get the region of interest (where lanes will be on screen)

	# create array of zeros in the shape of image
	mask = np.zeros_like(image)
	# filling pixels inside polygon defined by 'vertices' with fill color
	cv2.fillPoly(mask, vertices, 255)
	# return the image only where mask pixels are nonzero
	masked = cv2.bitwise_and(image, mask)
	return masked


def countdown(seconds):
	for i in list(range(seconds)) [::-1]:
		print(i + 1)
		time.sleep(1)


# Use opencv to find lanes in a road, then put those lanes back on original image
def process_img(image):
	# Determine wheather or not car is in a lane
	original_image = image
	# Convert to gray to have simplier data
	processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# edge detection
	processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
	processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)
	 
	# Get region of interest from image
	vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500],], np.int32)
	processed_img = roi(processed_img, [vertices])

	min_line_length, max_line_gap = 100, 5
	lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), min_line_length, max_line_gap)  
	# returns array of arrays that contains lines
	
	# slope of the lines
	m1 = 0
	m2 = 0

	try:
		l1, l2, m1,m2 = draw_lanes(original_image,lines)
		cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
		cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
	except Exception as e:
		print(str(e))
		pass
	try:
	    for coords in lines:
	        coords = coords[0]
	        try:
	            cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
	        except Exception as e:
	            print(str(e))
	except Exception as e:
	    pass

	return processed_img, original_image, m1, m2


def move(m1, m2):
	if m1 < 0 and m2 < 0:
		right()
	elif m1 > 0 and m2 > 0:
		left()
	else:
		straight()


def straight():
	PressKey(W)
	ReleaseKey(A)
	ReleaseKey(D)

def left():
	PressKey(A)
	ReleaseKey(W)
	ReleaseKey(D)

def right():
	PressKey(D)
	ReleaseKey(W)
	ReleaseKey(D)

def slow_down():
	ReleaseKey(W)
	ReleaseKey(A)
	ReleaseKey(D)

# Track the time between frames
last_time = time.time()

countdown(4)

while(True):
	# Grab image off the screen
	#print_screen_pil = ImageGrab.grab(bbox=(0,40, 800, 640))
	screen = grab_screen(region=(0,40, 800, 640))
	new_screen, original_image, m1, m2 = process_img(screen)

	print('Loop took {' + format(time.time() - last_time) + '} seconds')
	last_time = time.time()

	# Display image on the screen
	# cv2.imshow('window', cv2.cvtColor(np.array(print_screen_pil), cv2.COLOR_BGR2RGB))
	# cv2.imshow('window', new_screen)
	cv2.imshow('window2', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))

	move(m1, m2)

	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
