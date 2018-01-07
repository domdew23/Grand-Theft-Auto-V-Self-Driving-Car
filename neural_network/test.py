import numpy as np
import cv2
import pandas as pd 
from collections import Counter
from settings import TYPE, NAME, FINAL_FILE_NAME
import time

def show(train_data):
	for data in train_data:
		img = data[0]
		choice = data[1]
		cv2.imshow('test',img)
		print(choice)
		time.sleep(1)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break


starting_value = 1
FILE_NAME = '../data/{}/{}_training_data_{}.npy'.format(TYPE, NAME, starting_value)
train_data = np.load(FINAL_FILE_NAME)
print(len(train_data))
show(train_data)

#df = pd.DataFrame(train_data)
#print(Counter(df[1].apply(str)))

#show(train_data)


rights = [3, 34, 4, 4 ,4]
lefts = [0,3]
reverses = [1]
forwards = [4,3,2,3,1,1,2,23,3,3,3,33,3]

forwards = forwards[:len(lefts)][:len(rights)][:len(reverses)]

print(len(forwards))



