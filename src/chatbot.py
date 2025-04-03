import json
import numpy as np
import tensorflow as tf
import pickle
import random
import spacy

# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")

# Load required data
intents = json.load(open("../data/intents.json"))
data = pickle.load(open("../model/training_data.pkl", "rb"))
words, classes = data["words"], data["classes"]

# Load trained model
model = tf.keras.models.load_model("../model/chatbot_model.h5")

def clean_up_sentence(sentence):
    # Tokenize and lemmatize the sentence using SpaCy
    doc = nlp(sentence)
    sentence_words = [token.lemma_.lower() for token in doc]
    return sentence_words

def bow(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def classify(sentence):
    ERROR_THRESHOLD = 0.25
    results = model.predict(np.array([bow(sentence)]))[0]
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [(classes[r[0]], r[1]) for r in results]

def get_response(sentence):
    results = classify(sentence)
    if results:
        for intent in intents["intents"]:
            if intent["tag"] == results[0][0]:
                return random.choice(intent["responses"])
    return "I'm sorry, I don't understand."

if __name__ == "__main__":
    print("Chatbot is ready! Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("Bot:", get_response(user_input))