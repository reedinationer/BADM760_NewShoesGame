import tensorflow as tf
import numpy as np
import pandas as pd

from tensorflow import keras
from tensorflow.keras import layers, model

training_data = pd.read_excel("/Users/reed/PycharmProjects/760_Marketing/New Shoes.xlsx", sheet_name=None, index_col=0, header=[0, 1])

features = training_data["2"].copy()
# marketing_labels = features.pop('Age')

features_array = np.array(features)

tf_model = tf.keras.Sequential([
  layers.Dense(64),
  layers.Dense(1)
])

tf_model.compile(loss = tf.losses.MeanSquaredError(), optimizer = tf.optimizers.Adam())

tf_model.fit(features_array, features.columns, epochs=10)

