import sys
sys.path.append('../dependencies')
import numpy as np 
import constants as const

from alexnet import alexnet

model = alexnet(const.WIDTH, const.HEIGHT, const.LEARNING_RATE)

train_data = np.load(const.FINAL_FILE_NAME)

train = train_data[:-500]
test = train_data[-500:]

X = np.array([i[0] for i in train]).reshape(-1, const.WIDTH, const.HEIGHT, 1)
y = [i[1] for i in train]

X_test = np.array([i[0] for i in test]).reshape(-1, const.WIDTH, const.HEIGHT, 1)
y_test = [i[1] for i in test]

model.fit(X, y, n_epoch=const.EPOCHS, validation_set=(X_test, y_test), 
	snapshot_step=500, show_metric=True, run_id=const.MODEL_NAME)

# tensorboard --logdir=foo:D:/Coding Projects/Python/gtav_self_driving_car

model.save(const.MODEL_NAME)
