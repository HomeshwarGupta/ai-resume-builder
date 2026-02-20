from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_full_resume(data):
    try:
        prompt = f"""
You are a professional resume writer.

Generate ONLY inner HTML content.
Do NOT add <html>, <head>, or <body> tags.
Do NOT use markdown.
Do NOT add notes.

Create sections with proper <h2>, <p>, <ul>, <li> formatting.

User Details:
Name: {data['name']}
Email: {data['email']}
Phone: {data['phone']}
Degree: {data['degree']}
University: {data['university']}
Year: {data['year']}
Skills: {data['skills']}
Experience: {data['experience']}

Sections Required:
1. Professional Summary
2. Technical Skills
3. Experience
4. Education
5. Projects (generate if missing)
6. Strengths (generate if missing)
"""

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
        )

        result = chat_completion.choices[0].message.content
        result = result.replace("```", "").replace("html", "")

        return result.strip()

    except Exception as e:
        return f"<h2>AI Error:</h2><p>{str(e)}</p>"


@app.route("/")
def home():
    return render_template("form.html")


@app.route("/generate", methods=["POST"])
def generate():
    form_data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "degree": request.form["degree"],
        "university": request.form["university"],
        "year": request.form["year"],
        "skills": request.form["skills"],
        "experience": request.form["experience"],
    }

    ai_resume = generate_full_resume(form_data)

    return render_template(
        "resume.html",
        name=form_data["name"],
        email=form_data["email"],
        phone=form_data["phone"],
        ai_resume=ai_resume
    )


if __name__ == "__main__":
    app.run(debug=True)