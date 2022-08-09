import os
from pickletools import optimize
from random import shuffle
import tensorflow as tf
import keras
import numpy as np
from keras import layers
import tensorflow_hub as hub
from keras.preprocessing.image import ImageDataGenerator

BATCH_SIZE = 32
IMAGE_SHAPE = (224, 224)
img_height = 224
img_width = 224

mobilenet_v2 ="https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"

classifier_model = mobilenet_v2

classifier = tf.keras.Sequential([
    hub.KerasLayer(classifier_model, input_shape=IMAGE_SHAPE+(3,))
])

train_ds =tf.keras.preprocessing.image_dataset_from_directory(
    'plants',
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    'plants',
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=BATCH_SIZE
)


def augment(image, label):
    new_height = new_width = 224
    image = tf.image.resize(image, (new_height, new_width))

    if tf.random.uniform((), minval=0, maxval=1) < 0.1:
        image = tf.tile(tf.image.rgb_to_grayscale(image), [1,1,1,3])

    image = tf.image.random_brightness(image, max_delta=0.5)
    image = tf.image.random_contrast(image, lower=0.1, upper=0.4)
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_flip_up_down(image)

    print("applied augmentation")
    return image, label

class_names = np.array(train_ds.class_names)

normalization_layer = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y)) # Where x—images, y—labels.
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y)) # Where x—images, y—labels.

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache()
train_ds = train_ds.map(augment, num_parallel_calls=AUTOTUNE)
train_ds = train_ds.prefetch(AUTOTUNE)


val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y)) # Where x—images, y—labels.
val_ds = val_ds.cache().prefetch(AUTOTUNE)


feature_extractor_model = mobilenet_v2

feature_extractor_layer = hub.KerasLayer(
    feature_extractor_model,
    input_shape=(224,224,3),
    trainable=False
)

resize_and_rescale = tf.keras.Sequential([
  layers.Resizing(img_width, img_height),
  layers.Rescaling(1./255)
])

data_augmentation = tf.keras.Sequential([
  layers.RandomFlip("horizontal_and_vertical"),
  layers.RandomRotation(0.2),
  layers.RandomZoom(.5, .2),
  layers.RandomContrast(0.2),
])

num_classes = len(class_names)

model = keras.Sequential([
  feature_extractor_layer,
  layers.Dense(num_classes),
])

# model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

# model.summary()


NUM_EPOCHS = 20

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=NUM_EPOCHS,
)

model.save('complete_saved_model/')

