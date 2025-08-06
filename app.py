from flask import Flask, render_template, request
import pandas as pd
import re
import nltk
import pymongo
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# ========== PREPARACIÓN INICIAL ==========
nltk.download("stopwords")
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)

# ========== CARGA Y ENTRENAMIENTO ==========
df = pd.read_csv("spam.csv", encoding="latin-1")[["v1", "v2"]].rename(columns={"v1": "label", "v2": "text"})
df["cleaned_text"] = df["text"].apply(clean_text)
df["label_num"] = df["label"].map({"ham": 0, "spam": 1})

# Vectorización
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["cleaned_text"])
y = df["label_num"]

# Modelo
model = MultinomialNB()
model.fit(X, y)

# ========== CONEXIÓN A MONGODB ==========
client = pymongo.MongoClient("mongodb://localhost:27017/Spam_Detector")  # o URI de MongoDB Atlas
db = client["Spam_Detector"]
collection = db["mensajes"]

# ========== FLASK APP ==========
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        texto_usuario = request.form["texto"]
        texto_limpio = clean_text(texto_usuario)
        texto_vectorizado = vectorizer.transform([texto_limpio])
        pred = model.predict(texto_vectorizado)[0]
        etiqueta = "Spam" if pred == 1 else "No Spam"

        # Guardar en MongoDB
        collection.insert_one({
            "mensaje": texto_usuario,
            "etiqueta": etiqueta
        })

        resultado = f"Resultado: {etiqueta}"

    return render_template("index.html", result=resultado)

if __name__ == "__main__":
    app.run(debug=True)
