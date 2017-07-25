import numpy as np
from PIL import ImageGrab
import cv2
import time

last_time = time.time()

while(True):

	print_screen_pil = ImageGrab.grab(bbox=(0,40, 1270, 1000))
	#printscreen_numpy = np.array(print_screen_pil.getdata(), dtype ='uint8')

	print('Loop took {' + format(time.time() - last_time) + '} seconds')
	last_time = time.time()
	cv2.waitKey(1)
	cv2.imshow('window', np.array(print_screen_pil))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break


