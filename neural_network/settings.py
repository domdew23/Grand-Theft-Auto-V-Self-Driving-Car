# Constants (keys)
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

WIDTH = 480
HEIGHT = 270
LEARNING_RATE  = .001
EPOCHS = 5

TIME = 0.25

VERSION = 'v1' 
TYPE = 'car'
VIEW = '3rd_person'
NAME = VIEW + '_' + TYPE + '_' + VERSION

FILE_NAME = '../data/{}/{}_training_data.npy'.format(TYPE, NAME)
FINAL_FILE_NAME = '../bal_data/{}/{}_bal_training_data.npy'.format(TYPE, NAME)

MODEL_NAME = 'balanced_pygta5-{}-{}-{}-{}-epochs.model'.format(NAME, LEARNING_RATE, 'googlenet', EPOCHS)
