import pdf2image
import pytesseract
import requests
import re
# import fitz  # PyMuPDF

# def extract_text_from_pdf(file_path):
#     text = ""
#     with fitz.open(file_path) as doc:
#         for page in doc:
#             text += page.get_text()
#     return text

# Gemini API Key
GEMINI_API_KEY = "AIzaSyDSNKVFGhfCCX6Onx5b8NEyk38qTH-YRXg"

def extract_text_from_pdf(file_path):
    images = pdf2image.convert_from_path(file_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def clean_markdown(text: str) -> str:
    text = text.replace("*", "")
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    return text.strip()

def analyze_resume(file_path):
    resume_text = extract_text_from_pdf(file_path).strip()
    if not resume_text:
        return "No readable text found in the uploaded PDF."

    prompt = f"""
Analyze the following resume text:
{resume_text}

1. Summarize candidate's profile.
2. Recommend suitable job roles.
3. Suggest resume improvements.
4. Generate 5 interview questions.
5. Provide an HR-style overview.
6. Provide HR advice on resume content.
"""

    url = (
      "https://generativelanguage.googleapis.com/v1beta/"
      "models/gemini-1.5-flash:generateContent"
      f"?key={GEMINI_API_KEY}"
    )
    headers = {"Content-Type": "application/json"}
    body = {
      "contents": [{
        "parts": [{"text": prompt}]
      }]
    }

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            raw = data["candidates"][0]["content"]["parts"][0]["text"]
            return clean_markdown(raw)
        else:
            return f"Error {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"Gemini request failed: {str(e)}"

def generate_cover_letter(resume_text):
    prompt = f"""
      You're a professional HR assistant. Based on the following resume content, create a tailored and formal cover letter for a job application.

      Resume Content:
      {resume_text}

      Instructions:
      - Write at least 250 words
      - Start with "Dear Hiring Manager,"
      - End with a formal closing and applicant's name as "Sincerely, [Your Name]"
      - Be specific and professional
      - Use a formal tone
    """


    url = (
      "https://generativelanguage.googleapis.com/v1beta/"
      "models/gemini-1.5-flash:generateContent"
      f"?key={GEMINI_API_KEY}"
    )
    headers = {"Content-Type": "application/json"}
    body = {
      "contents": [{
        "parts": [{"text": prompt}]
      }]
    }

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            raw = data["candidates"][0]["content"]["parts"][0]["text"]
            return clean_markdown(raw)
        else:
            return f"Error {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"Gemini request failed: {str(e)}"
