import numpy as np 

from settings import WIDTH, HEIGHT, LEARNING_RATE, EPOCHS, FINAL_FILE_NAME, MODEL_NAME
from models import inception_v3 as googlenet

model = googlenet(WIDTH, HEIGHT, LEARNING_RATE)

hm_data = 22

for i in range(EPOCHS):
	for i in range(1, hm_data + 1):
		train_data = np.load(FINAL_FILE_NAME)

		train = train_data[:-100]
		test = train_data[-100:]

		X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
		y = [i[1] for i in train]

		X_test = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
		y_test = [i[1] for i in test]

		model.fit(X, y, n_epoch=EPOCHS, validation_set=(X_test, y_test), 
			snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

		# tensorboard --logdir=foo:D:/Coding Projects/Python/gtav_self_driving_car

		model.save(MODEL_NAME)
