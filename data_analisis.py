from os.path import join, dirname, abspath
from os import error, listdir, path
from datetime import datetime
from cv2 import data, imread, resize
from keras import models
from numpy.lib.histograms import histogram
from tqdm import tqdm, utils
from random import shuffle
from numpy import array, log
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import callbacks, utils
import keras    # TODO replace redundant imports with smaller and more optimized ones

class ImageRecgonition:
    def __init__(self, path: str, size: tuple, logDir: str = "logs\\fit\\"):
        self.path = path
        self.size = size
        self.logDir = f"{logDir}log_{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        

    def define_dataset(self) -> list:

        self.dataset: list = []
        self.categories = [ d for d in listdir(join(dirname(abspath(__file__)), self.path)) ]   # look for all subdirectories and name categories from them 
        # what the fuck? vvv
        for cat in self.categories:
            imgPath: str = join(join(dirname(abspath(__file__)), self.path), cat)
            categoryIndex: int = self.categories.index(cat)
            for img in tqdm(listdir(path)):
                try:
                    imgArray: list = imread(join(path, img))
                    actualImg = resize(imgArray, self.size)
                    self.dataset.append([actualImg, categoryIndex])
                except Exception as e:
                    exit(f"Error in 'ImageRecoginiton.define_dataset' occured - stopped working: {e}")
        # end of what the fuck? ^^^

    def modeling(
        self, 
        batchSize: int,
        epochs: int,
        validationSplit: float):

        shuffle(self.dataset)
        trainingX, labelsY = [], []

        for features, label in self.dataset:    # preparing dataset and its labels for further modeling
            trainingX.append(features)
            labelsY.append(label)
        
        trainingX: array = array(trainingX).reshape(-1, self.size[0], self.size[1], 3)  # reshape data as a numpy array
        trainingX = trainingX/255.0

        # actual modelingg, adding layers and creating models
        self.modelSequential = Sequential()
        
        self.modelSequential.add(Conv2D(256, (3, 3), input_shape=trainingX.shape[1:]))
        self.modelSequential.add(Activation('relu'))
        self.modelSequential.add(MaxPooling2D(pool_size=(2, 2)))

        self.modelSequential.add(Conv2D(256, (3, 3)))
        self.modelSequential.add(Activation('relu'))
        self.modelSequential.add(MaxPooling2D(pool_size=(2, 2)))

        self.modelSequential.add(Flatten()).add(Dense(64)).add(Dense(7))
        self.modelSequential.add(Activation('sigmoid'))
        # TODO modeling in beta version
        # TODO create several models to choose from as methods

        self.modelSequential.compile(
            loss="categorical_crossentropy", 
            optimizer="adam", 
            metrics=["accutracy"])      # compiling model defined above
        labelsYCategorical = utils.to_categorical(labelsY, num_classes=7)     # converting labelsY as a categories

        tensorboard = callbacks.TensorBoard(log_dir = self.logDir, histogram_freq = 1)      # creating tensorboard

        try:
            self.modelSequential.fit(
                trainingX, 
                labelsYCategorical, 
                batch_size = batchSize, 
                epochs = epochs, 
                validation_split = validationSplit,
                callbacks = [tensorboard])
        except Exception as e:
            print(f"Error unhandled: {e} while trying to fit model in 'ImageRecgonition.modeling")
            self.modelSequential.fit(
                trainingX, 
                labelsYCategorical, 
                batch_size = batchSize, 
                epochs = epochs, 
                validation_split = validationSplit)
    
    def calling_predictions(self, model, testImg):          # predicting tests
        # preparing models and dimensions
        imgArray = imread(testImg)
        actualImg = resize(imgArray, self.size).reshape(-1, self.size[0], self.size[1], 3)
        prediction = model.predict([actualImg])      # pick a test sample
        return self.categories[int(prediction[0][0])]

        
                    
    def size(self) -> int:
        try:
            return len(self.dataset)
        except UnboundLocalError as e:
            return f"Error in 'ImageRecognition.size' - dataset not created yet: {e}. Use 'ImageRecognition.define_dataset'"
        except error as e:
            return f"Error in 'ImageRecognition.size' - unhandled error: {e}"
        

if __name__ == "__main__":
    pass
    # TODO WARNING code untested yet