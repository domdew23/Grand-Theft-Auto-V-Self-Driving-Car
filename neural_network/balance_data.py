import numpy as np 
import pandas as pd 
import cv2

from settings import FILE_NAME, FINAL_FILE_NAME
from collections import Counter
from random import shuffle

train_data = np.load(FILE_NAME)

df = pd.DataFrame(train_data)
print(df.head)
print(Counter(df[1].apply(str)))

lefts = []
rights = []
forwards = []

# prevent neural network from being bias for specific movements

shuffle(train_data)

for data in train_data:
	img = data[0]
	choice = data[1]

	if choice == [1, 0, 0]:
		lefts.append([img, choice])
	elif choice == [0, 1, 0]:
		forwards.append([img, choice])
	elif choice == [0, 0, 1]:
		rights.append([img, choice])
	else:
		print("No mathces")

print(len(forwards))
print(len(lefts))
print(len(rights))
print()

forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]

print(len(forwards))
print(len(lefts))
print(len(rights))

final_data = forwards + lefts + rights
shuffle(final_data)

print("final data: {}".format(len(final_data)))
print("train data: {}".format(len(train_data)))

np.save(FINAL_FILE_NAME, final_data)

