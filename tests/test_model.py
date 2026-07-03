import pickle
from preprocessing import preprocess

model = pickle.load(open("model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

text = "I loved the movie and the director's brilliance oh my god!!!"

processed = preprocess(text)

print("Processed:", processed)

vector = tfidf.transform([processed])

print("Prediction:", model.predict(vector))
print("Probabilities:", model.predict_proba(vector))