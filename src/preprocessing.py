import json
import spacy
import numpy as np
import pickle
import random

# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")

def load_intents(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def preprocess_data(intents):
    words = []
    classes = []
    documents = []
    ignore_words = ["?"]

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            # Tokenize the pattern using SpaCy
            doc = nlp(pattern)
            tokens = [token.text for token in doc]
            words.extend(tokens)
            documents.append((tokens, intent["tag"]))
            if intent["tag"] not in classes:
                classes.append(intent["tag"])

    # Lemmatize and filter out ignored words
    words = sorted(set(token.lemma_.lower() for token in nlp(" ".join(words)) if token.text not in ignore_words))
    classes = sorted(set(classes))

    training = []
    output_empty = [0] * len(classes)

    for doc in documents:
        bag = []
        pattern_words = [token.lemma_.lower() for token in nlp(" ".join(doc[0]))]
        for w in words:
            bag.append(1 if w in pattern_words else 0)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)
    
    return words, classes, list(training[:, 0]), list(training[:, 1])

if __name__ == "__main__":
    intents = load_intents("../data/intents.json")
    words, classes, train_x, train_y = preprocess_data(intents)
    pickle.dump({"words": words, "classes": classes, "train_x": train_x, "train_y": train_y}, open("../data/training_data.pkl", "wb"))