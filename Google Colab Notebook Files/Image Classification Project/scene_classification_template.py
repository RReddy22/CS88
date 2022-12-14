# -*- coding: utf-8 -*-
"""Scene_Classification_Template.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-hgz41b3whWp3fJ6WbmHV1jM5nT_4dyi

##Author: Sidharth Ramanan
###Date: 05/20/22

**First, make a copy of this notebook for you to play around with.** `File -> Save a copy in Drive`

**Second, make sure your Google Drive has been mounted. The option to do so is in the left menu**

This is an image classification project from Kaggle (link [here](https://www.kaggle.com/datasets/puneet6060/intel-image-classification)) The goal is to classify different scenes of images (buildings, glaciers, mountains, etc)

The first step would be to visit the Kaggle project and download the [`archive.zip`](https://www.kaggle.com/datasets/puneet6060/intel-image-classification/download) file containing the dataset of images

Then, upload that file to the root level of your Google Drive and run the cell below to extract the zip file. This will create a folder called `scenes_dataset`
Feel free to change the file paths below if you'd like.

You should use [Tensorflow](https://www.tensorflow.org/api_docs) to complete this project - Tensorflow provides a Python API to create and train neural networks. You can also look at online Tensorflow tutorials for image classification if that would help, but try to understand what the code is doing/how to change it for your specific needs.

Some tips for the project:


1.  There are only a few parts of the Tensorflow API that are worth focusing on - their model API, their layer API, optimizers, loss functions, callbacks, evaluation metrics and maybe some utils
2.  You probably want to leverage Transfer Learning for the project - it would be challenging to construct your own CNN architecture for the project. 
3. Don't hesitate to make mistakes - playing around with the API and causing errors is the best way to understand how things work.
4. Speaking of errors, Stack Overflow is your best friend if you're running into an issue you don't understand. Github Issues might also be helpful. Feel free to reach out to me as well
5. Have fun and do your best! This is a zero stakes, zero pressure project and really just a bonus learning opportunity. Anything you can get out of this project, even if it's a little, is a win.
"""

import zipfile
with zipfile.ZipFile('/content/drive/My Drive/archive.zip', 'r') as zip_ref:
    zip_ref.extractall('/content/drive/My Drive/scenes_dataset')

"""Sometimes, Colab's environment doesn't have all the python packages you need. The easiest way is to `pip install` them like so:"""

!pip install livelossplot

"""In fact, you can run any normal UNIX style commands in Colab with this syntax:"""

!ls -al

"""I've included imports for some commonly used ML/DS python libraries below, along with some Tensorflow modules that you might find useful"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import os
import pathlib
import imageio
import datetime
import cv2
import functools
import math

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow.keras.utils as Utils
import tensorflow.keras.models as Models
from livelossplot import PlotLossesKeras

"""This is how you can check if you're using the GPU. Unless you upgrade your Colab plan, you won't benefit from faster training times with the GPU, but that's fine - the training times should still be manageable"""

if tf.config.list_physical_devices('GPU'):
  print("TensorFlow **IS** using the GPU")
else:
  print("TensorFlow **IS NOT** using the GPU")

"""#Preparation"""

DATASET_FOLDER = f'/content/drive/My Drive/scenes_dataset'
NUM_CLASSES = 6
trainDir = f'{DATASET_FOLDER}/seg_train/seg_train'
testDir = f'{DATASET_FOLDER}/seg_test/seg_test'
bestModelPath = f'{DATASET_FOLDER}/best_model'

def plotRandomSet(N):
  images = []
  labels = []
  for i in range(N * N):
    label = np.random.choice(os.listdir(trainDir))
    image_name = np.random.choice(os.listdir(trainDir + '/' + label))
    image = cv2.imread(trainDir + '/' + label + '/' + image_name)
    image = cv2.resize(image, (150, 150))
    images.append(image)
    labels.append(label)

  fig, ax = plt.subplots(N, N)
  plt.subplots_adjust(left=0.5, bottom=0.5, right=1, top=1, wspace=0.9,hspace=0.9)
  fig.subplots_adjust(0,0,3,3)

  for i in range(0,N,1):
      for j in range(0,N,1):
          ax[i,j].imshow(images[i*N + j])
          ax[i,j].set_title(labels[i*N + j])
          ax[i,j].axis('off')
  
plotRandomSet(5)

"""Here would be a useful place to define Tensorflow callbacks - callbacks are useful functions that run at the end of every epoch during training. Explore the Tensorflow API to find some useful callbacks. An example callback is the liveloss callback which plots the loss and accuracy as training occurs. """

#Define any Tensorflow callbacks here. Remember to include the Tensorboard callback, it will be useful later

"""#Loading in the dataset

Your next step should be figuring out a strategy to load the dataset into Colab for training. I would recommend looking at Tensorflow's `ImageDataGenerator` and its `flow_from_directory` method. Generators are a general Python concept that refers to computation on-demand and in this context that principle applies - image generators allow images to be loaded on-demand and only when they're needed instead of loading the entire dataset into Colab at once.
"""

#Instantiate the image generators for the training and test directories here and call flow_from_directory

"""#Modeling

Next, you should work on building your model. Tensorflow has many available CNN architectures you can use in a transfer learning setting - explore how you can implement a transfer learning model for this data problem

An important thing to remember in building models with Tensorflow layers in managing input and output shapes. As you're passing Tensors (the Tensorflow data structure) between layers, you need to make sure the shapes of those tensors are compatible with what the layer is expecting
"""

#Build, compile, and train your Keras model here

"""#Evaluation

One thing you might want to understand once your model is trained is the pattern of mistakes it's making. Does it frequently confuse some specific classes? The best way to understand this is using confusion matrices. 

This might be helpful in understanding, say, what preprocessing operations you can perform on the images to accentuate/emphasize the differences between the classes the model is confusing, though this is pretty advanced model debugging. Nevertheless, it's insightful to plot confusion matrices.

You may need to change variable names here - I assume that your generator for the test folder is called `test_generator`
"""

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

y_pred = model1.predict(test_generator).argmax(axis=-1) 
y_test = test_generator.classes
labels = test_generator.class_indices.keys()

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

disp.plot(cmap=plt.cm.Blues)
plt.show()

"""Another useful tool to get familiar with is TensorBoard, which is an extension that allows you to really dive into the nitty-gritties of your trained model - understanding the architecture, weights, visualizing graphs, etc

I encourage you to explore using TensorBoard, even if it doesn't directly lead to model improvements. You'll find it handy in the future.

Run the following cells - this should open up Tensorboard with a dashboard to understand your trained model

Remember to also use the tensorboard callback when you build your model
"""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard

# Commented out IPython magic to ensure Python compatibility.
# %tensorboard --logdir logs

"""#Saving your work

Here are some utility functions for Tensorflow models that will alow you to visualize and save your models.
"""

def plotModel(model):
  Utils.plot_model(model,to_file=f'{DATASET_FOLDER}/model.png',show_shapes=True)

def saveModel(model):
  model.save(f'{DATASET_FOLDER}/model.h5')

def loadModel(modelPath):
  model = Models.load_model(modelPath)
  return model

"""For this project, try to get a model that crosses an accuracy of 80% on the test set - that would signify pretty solid work! Reach out to me if you have any questions and need help"""