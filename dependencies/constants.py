# Constants (keys)
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

WIDTH = 160
HEIGHT = 120
LEARNING_RATE  = .001
EPOCHS = 10
MODEL_NAME = 'pygta5-car-{}-{}-{}-epochs.model'.format(LEARNING_RATE, 'alexnetv2', EPOCHS)

TIME = 0.09

FILE_NAME = '../data/training_data.npy'
FINAL_FILE_NAME = '../data/final_training_data.npy'