import sys, os, time, cv2
sys.path.append('..\dependencies')
import numpy as np

from settings import FILE_NAME, WIDTH, HEIGHT
from functions import key_check, grab_screen, countdown, prompt_quit

# neural network:
# input is pixel data
# output is the movements
# input data is to manually drive and train data based off that

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]


def keys_to_output(keys):
    # Convert keys to array
    # 0 1 2 3  4  5  6  7   8
    #[W,S,A,D,WA,WD,SA,SD,NOKEY]

    output = [0,0,0,0,0,0,0,0,0]
    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
    	output = sa
    elif 'S' in keys and 'D' in keys:
    	output = sd
    elif 'W' in  keys:
    	output = w
    elif 'S' in keys:
    	output = s
    elif 'A' in keys:
    	output = a
    elif 'D' in keys:
    	output = d
    else:
    	output = nk
    return output


def get_length():
	if os.path.isfile(FILE_NAME):
		with open(FILE_NAME, 'r') as file:
			print("File exists, loading previous data...")
			total_length = len(np.load(FILE_NAME))
	else:
		total_length = 0
	return total_length


def save(length, training_data):
	save_time = time.time()
	print("Saving... || training_data length: {}".format(length))
	if not os.path.isfile(FILE_NAME):
		print("File does not exist, creating file...")
		with open(FILE_NAME, 'wb') as file:
			np.save(file, training_data)
	else:
		print("File exists, appending data...")
		with open(FILE_NAME, 'ab') as file:
			np.save(file, training_data)

	print("Took || {}{:.2f}{} seconds to save".format('{', time.time()- save_time, '}'))
	print("Saved")
	time.sleep(2)



def get_screen():
	screen = grab_screen(region=(0, 40, 1920, 1120))
	screen = cv2.resize(screen, (WIDTH, HEIGHT))
	screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
	return screen


def show_screen(screen):
	cv2.imshow('window', cv2.resize(screen, (640, 360)))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()


def main():
	start_time = time.time() 
	total_length = get_length()
	training_data = []
	print("Took || {}{}{} seconds to load data".format('{', time.time()- start_time, '}'))
	countdown(4)
	PAUSED = False

	while True:
		if not PAUSED:
			start_time = time.time() 
			screen = get_screen()
			# show_screen(screen)
			
			# grab data
			keys = key_check()
			output = keys_to_output(keys)
			training_data.append([screen, output])
			tmp_length = len(training_data)

			if tmp_length % 1000 == 0:
				total_length += tmp_length
				save(total_length, training_data)
				training_data = []
			time = time.time()- start_time
			print("Not Paused Loop took: {}{:.3f}{} seconds || tmp_length: {}".format('{', time, '}', tmp_length))
		
		keys = key_check()

		if 'Q' in keys:
			sys.exit()

		if 'T' in keys:
			if PAUSED:
				print('Unpausing...')
				PAUSED = False
				time.sleep(1)
			else:
				print('Pausing...')
				PAUSED = True
				time.sleep(1)
				print('Paused')
				print("training_data length: {}".format(total_length))
				print('Press (t) to unpause')
				print('Press (q) at any time to quit')


main()