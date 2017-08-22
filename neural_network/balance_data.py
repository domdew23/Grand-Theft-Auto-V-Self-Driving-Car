import numpy as np 
import pandas as pd 
import cv2

from settings import TYPE, NAME, FINAL_FILE_NAME
from collections import Counter
from random import shuffle
# prevent neural network from being bias for specific movements

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

forwards = []
reverses = []
lefts = []
rights = []
straight_lefts = []
straight_rights = []
reverse_lefts = []
reverse_rights = []
no_keys = []

for i in range(1, 75):
	FILE_NAME = '../data/{}/{}_training_data_{}.npy'.format(TYPE, NAME, i)
	train_data = np.load(FILE_NAME)
	#df = pd.DataFrame(train_data)
	#print(Counter(df[1].apply(str)))
	shuffle(train_data)

	for data in train_data:
		img = data[0]
		choice = data[1]

		if choice == w:
			forwards.append([img, choice])
		elif choice == s:
			reverses.append([img, choice])
		elif choice == a:
			lefts.append([img, choice])
		elif choice == d:
			rights.append([img, choice])
		elif choice == wa:
			straight_lefts.append([img, choice])
		elif choice == wd:
			straight_rights.append([img, choice])
		elif choice == nk:
			no_keys.append([img, choice])
		else:
			print("No match")

	print("File #", i)
	print("Fowards:", len(forwards))
	print("Reverses:", len(reverses))
	print("Lefts:", len(lefts))
	print("Rights:", len(rights))
	print("Straight_lefts:", len(straight_lefts))
	print("Straight_rights:", len(straight_rights))
	print("No_Keys:", len(no_keys))
	print()

forwards = forwards[:len(lefts)][:len(rights)][:len(reverses)][:len(straight_lefts)][:len(straight_rights)][:len(no_keys)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]
reverses = reverses[:len(forwards)]
straight_lefts = straight_lefts[:len(forwards)]
straight_rights = straight_rights[:len(forwards)]
no_keys = no_keys[:len(forwards)]

print("Fowards:", len(forwards))
print("Reverses:", len(reverses))
print("Lefts:", len(lefts))
print("Rights:", len(rights))
print("Straight_lefts:", len(straight_lefts))
print("Straight_rights:", len(straight_rights))
print("No_Keys:", len(no_keys))
print()

final_data = forwards + lefts + rights + reverses + straight_lefts + straight_rights + no_keys
shuffle(final_data)

print("final data: {}".format(len(final_data)))
print("train data: {}".format(2500 * 74))

print("Saving...")
np.save(FINAL_FILE_NAME, final_data)
print("Saved.")
