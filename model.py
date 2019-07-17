import os

import tensorflow as tf
from keras import layers, models


def build_model():
    model = models.Sequential()
    model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=(3000, 1500, 4)))
    model.add(layers.Conv2D(16, (3, 3), activation='relu'))
    model.add(layers.Conv2D(32, (3, 3), activation='relu'))
    model.add(layers.Conv2D(16, (3, 3), activation='relu'))
    model.add(layers.Conv2D(8, (3, 3), activation='relu'))
    model.add(layers.Conv2D(4, (3, 3), activation='relu'))
    model.add(layers.Conv2D(3, (3, 3), activation='relu'))
    model.compile(optimizer='adam', loss='mse')
    model.summary()
    return model

def load_data(directories):
    train = []
    label = []
    for d in directories:
        for file in os.listdir(d):
            if file.endswith('png') :
                if file.endswith('_whiped.png') and file.startswith('cropped_'):
                    input_file = tf.constant(d + os.path.sep + file.strip('_whiped.png') + '.png')
                    label_file = tf.constant(d + os.path.sep + file)
                    train.append(tf.io.decode_png(tf.read_file(input_file)))
                    label.append(tf.io.decode_png(tf.read_file(label_file)))
    return tf.stack(train), tf.stack(label)

if __name__ == "__main__":
    session = tf.Session()
    model = build_model()
    X, Y = load_data(['./data/'])
    model.fit(X, Y , epochs=1, steps_per_epoch= 200 )
    print(session.run(tf.shape(Y)))





