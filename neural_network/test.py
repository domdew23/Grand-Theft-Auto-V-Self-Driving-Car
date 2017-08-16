import numpy as np
import cv2
import pandas as pd 
from collections import Counter
from settings import TYPE, NAME


def show(train_data):
	for data in train_data:
		img = data[0]
		choice = data[1]
		cv2.imshow('test',img)
		print(choice)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break


starting_value = 4
FILE_NAME = '../data/{}/{}_training_data_{}.npy'.format(TYPE, NAME, starting_value)
train_data = np.load(FILE_NAME)

df = pd.DataFrame(train_data)
print(Counter(df[1].apply(str)))

#show(train_data)



