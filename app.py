from flask import Flask, request, render_template
import json
from scoring import calculate_scores
from roadmap import analyze_and_generate
from config import get_db
from visual import generate_chart

app = Flask(__name__)

# Load questions — now a dictionary with keys: product, service, core
with open("questions.json") as f:
    all_questions = json.load(f)


# -----------------------------------------------
# HOME PAGE
# -----------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -----------------------------------------------
# QUIZ PAGE — loads target-specific questions
# -----------------------------------------------
@app.route("/quiz")
def quiz():
    target = request.args.get("target")

    if not target or target not in ["product", "service", "core"]:
        return render_template("home.html")

    questions = all_questions.get(target, [])

    return render_template("quiz.html", questions=questions, target=target)


# -----------------------------------------------
# RESULT PAGE
# -----------------------------------------------
@app.route("/result", methods=["POST"])
def result():
    answers = request.form.to_dict()
    target = answers.get("target")

    if not target:
        return "Invalid submission", 400

    # Get questions for this target
    questions = all_questions.get(target, [])

    # Calculate scores
    scores, total = calculate_scores(answers, questions, target)

    # Generate roadmap and gap analysis
    gaps, roadmap, weakest, strongest = analyze_and_generate(scores, target)

    # Percentile — capped at 99
    percentile = min(int(total * 100), 99)

    # Generate bar chart
    generate_chart(scores)

    # Labels and values for Chart.js radar
    labels = list(scores.keys())
    values = list(scores.values())

    # Save to MySQL
    try:
        db = get_db()
        if db:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO results
                (target, total_score, dsa, os, dbms, cn, aptitude, communication)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                target,
                round(total, 4),
                scores.get("DSA", 0),
                scores.get("OS", 0),
                scores.get("DBMS", 0),
                scores.get("CN", 0),
                scores.get("Aptitude", 0),
                scores.get("Communication", 0)
            ))
            db.commit()
            cursor.close()
            db.close()
    except Exception as e:
        print("DB Error:", e)

    return render_template(
        "result.html",
        scores=scores,
        total=round(total * 100, 2),
        roadmap=roadmap,
        percentile=percentile,
        weakest=weakest,
        strongest=strongest,
        labels=labels,
        values=values
    )


# -----------------------------------------------
# HISTORY PAGE
# -----------------------------------------------
@app.route("/history")
def history():
    return """
    <h1 style='font-family: Arial; text-align:center; margin-top:60px;'>Past Test History</h1>
    <p style='text-align:center;'>This feature is available in the full local version of the application.</p>
    <p style='text-align:center;'>History storage has been disabled in the live demo.</p>
    <div style='text-align:center; margin-top:20px;'>
        <a href="/" style="text-decoration:none; font-size:18px;">Go Back Home</a>
    </div>
    """
# -----------------------------------------------
# RUN
# -----------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
