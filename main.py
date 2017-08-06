import numpy as np
from numpy import ones,vstack
from numpy.linalg import lstsq
from statistics import mean
from PIL import ImageGrab
from grab_screen import grab_screen
import cv2
import time
import pyautogui

from direct_keys import PressKey, ReleaseKey, W, A, S, D

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
	lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), min_line_length, max_line_gap)  # returns array of arrays that contains lines
	
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


def draw_lanes(image, lines, color=[0,255,255], thickness=3):
	# if this fails go with some default lines
	try:
		# find the max y value for a lane marker
		# since we ecannoot assume horizon will always be at the same point

		ys = []
		for line in lines:
			for i in line:
				ys += [i[1], i[3]]
		min_y = min(ys)
		max_y = 600
		new_lines = []
		line_dict = {}

		for idx, i in enumerate(lines):
			for xyxy in i:
				# These four lines:
				# Used to caluclate definition from a  line
				x_coords = (xyxy[0], xyxy[2])
				y_coords = (xyxy[1], xyxy[3])
				A = vstack([x_coords, ones(len(x_coords))]).T
				m, b = lstsq(A, y_coords)[0]

				# Calculating new nad imporved xs
				x1 = (min_y - b) / m
				x2 = (max_y - b) / m

				line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]
				new_lines.append([int(x1), min_y, int(x2), max_y])

		final_lanes = {}

		# check for the slope, want to  find lines with similar slope
		for idx in line_dict:
			final_lanes_copy = final_lanes.copy()
			m = line_dict[idx][0]
			b = line_dict[idx][1]
			line = line_dict[idx][2]

			if len(final_lanes) == 0:
				final_lanes[m] = [[m, b, line]]
			else:
				found_copy = False

				for other_ms in final_lanes_copy:
					if not found_copy:
						if abs(other_ms * 1.1) > abs(m) > abs(other_ms * 0.9):
							if abs(final_lanes_copy[other_ms][0][1] * 1.1) > abs(b) > abs(final_lanes_copy[other_ms][0][1] * 0.9):
								final_lanes[other_ms].append([m, b, line])
								found_copy = True
								break
						else:
							final_lanes[m] = [[m, b, line]]

		line_counter = {}

		for lanes in final_lanes:
			line_counter[lanes] = len(final_lanes[lanes])

		top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

		lane1_id = top_lanes[0][0]
		lane2_id = top_lanes[1][0]

		def average_lane(lane_data):
			x1s = []
			y1s = []
			x2s = []
			y2s = []
			for data in lane_data:
				x1s.append(data[2][0])
				y1s.append(data[2][1])
				x2s.append(data[2][2])
				y2s.append(data[2][3])
			return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s)) 

		l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
		l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

		return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
	except Exception as e:
		print(str(e))


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
