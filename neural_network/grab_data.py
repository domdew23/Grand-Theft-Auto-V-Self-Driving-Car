import sys
sys.path.append('..\dependencies')
import cv2
import time
import constants as const

from functions import key_check, grab_screen, countdown, prompt_quit

# neural network:
# input is pixel data
# output is the movements
# input data is to manually drive and train data based off that

def keys_to_output(keys):
    # [A, W, D] (left, straight, right)
    output = [0, 0, 0]
    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    else:
        output[1] = 1

    return output


def get_file():
    if os.path.isfile(const.FILE_NAME):
        print("File exists, loading previous data")
        training_data = list(np.load(const.FILE_NAME))
    else:
        print("File does not exist, creating file...")
        training_data = []

    return training_data


def save(length, training_data):
    save_time = time.time()
    print("Saving... || training_data length: {}".format(length))
    np.save(const.FILE_NAME, training_data)
    print("Took || {}{:.2f}{} minutes to save".format('{', (time.time()- save_time) / 60, '}'))
    prompt_quit()
    print("Saved")
    time.sleep(1)



def main():
	start_time = time.time() 

	#training_data = get_file()
	training_data = []
	print("Took || {}{}{} seconds to load data".format('{', time.time()- start_time, '}'))

	countdown(4)

	PAUSED = False

	while True:
		if not PAUSED:
			start_time = time.time() 
			screen = grab_screen(region=(0, 40, 800, 640))
			# scale down to grayscale
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			screen = cv2.resize(screen, (160,120))
			
			# grab data
			keys = key_check()
			output = keys_to_output(keys)
			training_data.append([screen, output])
			length = len(training_data)

			if length % 100000 == 0:
				pass
				#save(length, training_data)
			print("Not Paused Loop took: {}{:.3f}{} seconds || training_data length: {}".format('{', time.time()- start_time, '}', length))
		
		keys = key_check()

		if 'P' in keys:
			if PAUSED:
				print('Unpausing...')
				PAUSED = False
				time.sleep(1)
			else:
				print('Pausing...')
				PAUSED = True
				time.sleep(1)
				print('Paused')
				print("training_data length: {}".format(len(training_data)))
				prompt_quit()
				print('Press (p) to unpause')

main()