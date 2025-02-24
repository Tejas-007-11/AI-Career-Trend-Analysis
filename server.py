from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "career_trend.db")  # Ensure correct DB path

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask API is running!",
        "endpoints": ["/trending-skills", "/recommend-career"]
    })

@app.route("/trending-skills", methods=["GET"])
def trending_skills():
    conn = get_db_connection()
    df = conn.execute("SELECT DISTINCT LanguageHaveWorkedWith FROM job_data").fetchall()
    conn.close()

    skills = list(set([skill for row in df for skill in row["LanguageHaveWorkedWith"].split(';')]))
    return jsonify({"trending_skills": skills})

@app.route("/recommend-career", methods=["POST"])
def recommend_career():
    data = request.json
    user_skills = set(data.get("skills", []))

    conn = get_db_connection()
    job_data = conn.execute("SELECT DevType, LanguageHaveWorkedWith FROM job_data").fetchall()
    conn.close()

    recommendations = {}
    for job in job_data:
        job_skills = set(job["LanguageHaveWorkedWith"].split(';'))
        match_score = len(user_skills & job_skills) / len(job_skills)  # Skill overlap ratio
        if match_score > 0:
            recommendations[job["DevType"]] = round(match_score, 2)  # Round to 2 decimal places

    sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

    return jsonify({"career_recommendations": sorted_recommendations[:5]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)



