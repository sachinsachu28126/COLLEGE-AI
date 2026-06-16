from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

app = Flask(__name__)

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_faqs():
    with open("faqs.json", "r") as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/chat", methods=["POST"])
def chat():

    faqs = load_faqs()
    questions = [f["question"] for f in faqs]

    embeddings = model.encode(questions)

    user_question = request.json["message"]
    user_embedding = model.encode([user_question])

    similarity = cosine_similarity(
        user_embedding,
        embeddings
    )[0]

    index = similarity.argmax()
    score = similarity[index]

    if score > 0.55:
        answer = faqs[index]["answer"]
    else:
        answer = (
            "Sorry, I couldn't find an answer."
        )

    return jsonify({
        "answer": answer,
        "confidence": round(float(score), 2)
    })

@app.route("/add", methods=["POST"])
def add():

    faqs = load_faqs()

    faqs.append({
        "category": request.json["category"],
        "question": request.json["question"],
        "answer": request.json["answer"]
    })

    with open("faqs.json", "w") as f:
        json.dump(faqs, f, indent=4)

    return jsonify({"message": "Added"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)