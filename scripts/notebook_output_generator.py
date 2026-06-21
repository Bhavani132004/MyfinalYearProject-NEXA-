import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def run_step(title, code_fn):
    with open('notebook_results.txt', 'a') as f:
        f.write(f"\n{'='*20} {title} {'='*20}\n")
    return code_fn()

def step_2_loading():
    dataset_path = 'data/dataset.json'
    with open(dataset_path, 'r') as f:
        data = json.load(f)
    texts = [item['text'] for item in data]
    labels = [item['intent'] for item in data]
    with open('notebook_results.txt', 'a') as f:
        f.write(f"Loaded {len(texts)} examples.\n")
    return texts, labels

def step_3_4_dataframe(texts, labels):
    df = pd.DataFrame({'text': texts, 'intent': labels})
    with open('notebook_results.txt', 'a') as f:
        f.write("\n[DataFrame Head]\n")
        f.write(str(df.head()) + "\n")
    return df

def step_5_distribution(df):
    dist = df['intent'].value_counts()
    with open('notebook_results.txt', 'a') as f:
        f.write("\n[Intent Distribution]\n")
        f.write(str(dist) + "\n")

def step_6_split(texts, labels):
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
    with open('notebook_results.txt', 'a') as f:
        f.write(f"Training set size: {len(X_train)}\n")
        f.write(f"Test set size: {len(X_test)}\n")
    return X_train, X_test, y_train, y_test

def step_7_8_train(X_train, y_train):
    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
        ('clf', SVC(kernel='linear', probability=True))
    ])
    with open('notebook_results.txt', 'a') as f:
        f.write("Training model...\n")
    model.fit(X_train, y_train)
    with open('notebook_results.txt', 'a') as f:
        f.write("Training complete.\n")
    return model

def step_9_evaluate(model, X_test, y_test):
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions)
    with open('notebook_results.txt', 'a') as f:
        f.write(f"\nClassification Report:\n{report}\n")

def step_12_test(model):
    test_queries = [
        "open chrome",
        "search for python on google",
        "what is the weather like today",
        "play some music",
        "create a new folder called work"
    ]
    with open('notebook_results.txt', 'a') as f:
        f.write("\n[Sample Predictions]\n")
        for query in test_queries:
            probas = model.predict_proba([query])[0]
            max_index = np.argmax(probas)
            confidence = probas[max_index]
            intent = model.classes_[max_index]
            f.write(f"Query: '{query}' -> Intent: {intent} ({confidence:.2f})\n")

if __name__ == "__main__":
    if os.path.exists('notebook_results.txt'):
        os.remove('notebook_results.txt')
    texts, labels = run_step("2. Loading Data", step_2_loading)
    df = run_step("3 & 4. DataFrame & Sample", lambda: step_3_4_dataframe(texts, labels))
    run_step("5. Distribution", lambda: step_5_distribution(df))
    X_train, X_test, y_train, y_test = run_step("6. Split", lambda: step_6_split(texts, labels))
    model = run_step("7 & 8. Model & Training", lambda: step_7_8_train(X_train, y_train))
    run_step("9. Evaluation", lambda: step_9_evaluate(model, X_test, y_test))
    run_step("12. Testing Queries", lambda: step_12_test(model))
