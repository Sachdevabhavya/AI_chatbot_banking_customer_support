import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import pickle
import numpy as np

def build_model(input_size, output_size):
    model = Sequential([
        Dense(128, input_shape=(input_size,), activation="relu"),
        Dropout(0.5),
        Dense(64, activation="relu"),
        Dropout(0.5),
        Dense(output_size, activation="softmax")
    ])
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

def train_and_save_model():
    data = pickle.load(open("../model/training_data.pkl", "rb"))
    train_x, train_y = np.array(data["train_x"]), np.array(data["train_y"])

    model = build_model(len(train_x[0]), len(train_y[0]))
    model.fit(train_x, train_y, epochs=200, batch_size=8, verbose=1)
    model.save("../model/chatbot_model.h5")

if __name__ == "__main__":
    train_and_save_model()
