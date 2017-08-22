import numpy as np 
from random import shuffle
from settings import WIDTH, HEIGHT, LEARNING_RATE, EPOCHS, MODEL_NAME, TYPE, NAME, FINAL_FILE_NAME
from models import inception_v3 as googlenet

START_FILE = 1
END_FILE = 74

model = googlenet(WIDTH, HEIGHT, 3, LEARNING_RATE, output=9, model_name=MODEL_NAME)

train_data = np.load(FINAL_FILE_NAME)

train = train_data[:-1500]  # all up to the last 1500
test = train_data[-1500:]   # the last 1500

X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 3)
y = [i[1] for i in train]

X_test = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 3)
y_test = [i[1] for i in test]

model.fit(X, y, n_epoch=EPOCHS, validation_set=(X_test, y_test), 
	snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

model.save(MODEL_NAME)

'''
try:
	model.load(MODEL_NAME)
	print("Loaded a previous model")
except Exception as e:
	print(str(e))
	print("No previous models")
'''


'''
for _ in range(EPOCHS):
	data_order = [i for i in range(START_FILE, END_FILE + 1)]
	shuffle(data_order)
	for count, i in enumerate(data_order):
		try:
			FILE_NAME = '../data/{}/{}_training_data_{}.npy'.format(TYPE, NAME, i)

			train_data = np.load(FILE_NAME)

			train = train_data[:-250]  # all up to the last 250
			test = train_data[-250:]   # the last 250

			X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 3)
			y = [i[1] for i in train]

			X_test = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 3)
			y_test = [i[1] for i in test]

			model.fit(X, y, n_epoch=1, validation_set=(X_test, y_test), 
				snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)

			# tensorboard --logdir=D:/Coding Projects/Python/gtav_self_driving_car/neural_network/log

			if count % 10 == 0:
				print("Saving model...")
				model.save(MODEL_NAME)
				print("Model saved.")

		except Exception as e:
			print("Got an exception:")
			print(str(e))
			'''