import numpy as np 
from alexnet import alexnet
from sklearn.model_selection import train_test_split

WIDTH = 80
HEIGHT = 60
LEARNING_RATE  = .001
EPOCHS = 8
MODEL_NAME = 'pygta5-car-{}-{}-{}-epochs.model'.format(LEARNING_RATE, 'alexnetv2', EPOCHS)

model = alexnet(WIDTH, HEIGHT, LEARNING_RATE)

train_data = np.load('../data/training_data_v2.npy')

train = train_data[:-500]
test = train_data[-500:]

X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
y = [i[1] for i in train]

X_test = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
y_test = [i[1] for i in test]

model.fit(X, y, n_epoch=EPOCHS, validation_set=(X_test, y_test), 
	snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

# tensorboard --logdir=foo:D:/Coding Projects/Python/gtav_self_driving_car

model.save(MODEL_NAME)
