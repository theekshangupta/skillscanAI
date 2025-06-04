from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from gemini_utils import analyze_resume, generate_cover_letter

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return "No file uploaded", 400

    file = request.files["resume"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    result = analyze_resume(filepath)
    return result

@app.route("/cover-letter", methods=["POST"])
def cover_letter():
    data = request.get_json()
    resume_text = data.get("text", "")

    if not resume_text:
        return "Resume content is empty.", 400

    result = generate_cover_letter(resume_text)
    return result

if __name__ == "__main__":
    app.run(debug=True)
