import os
import pickle
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Dynamically locate the pickle file
PICKLE_PATH = os.path.join(os.path.dirname(__file__), "career_trends.pkl")

# ✅ Check if the pickle file exists before loading
if os.path.exists(PICKLE_PATH):
    with open(PICKLE_PATH, "rb") as f:
        job_data = pickle.load(f)  # Ensure job_data is a DataFrame
else:
    job_data = None  # Handle missing file

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask API is running!",
        "endpoints": ["/trending-skills", "/recommend-career"]
    })

@app.route("/trending-skills", methods=["GET"])
def trending_skills():
    if job_data is None or not isinstance(job_data, pd.DataFrame):
        return jsonify({"error": "Pickle data not found!"}), 500

    if "LanguageHaveWorkedWith" not in job_data.columns:
        return jsonify({"error": "Invalid data format!"}), 500

    # ✅ Extract skills while handling None values
    skills = list(set(
        skill for row in job_data["LanguageHaveWorkedWith"].dropna()
        for skill in row.split(';')
    ))

    return jsonify({"trending_skills": skills})

@app.route("/recommend-career", methods=["POST"])
def recommend_career():
    if job_data is None or not isinstance(job_data, pd.DataFrame):
        return jsonify({"error": "Pickle data not found!"}), 500

    data = request.json
    user_skills = set(data.get("skills", []))  # ✅ Ensure it's a list

    if not user_skills:
        return jsonify({"error": "No skills provided!"}), 400

    recommendations = {}

    for _, row in job_data.iterrows():
        job_skills = row.get("LanguageHaveWorkedWith", "")
        if not job_skills:
            continue  # Skip if no skills listed

        job_skills_set = set(job_skills.split(';'))
        match_score = len(user_skills & job_skills_set) / len(job_skills_set)

        if match_score > 0:
            recommendations[row["DevType"]] = round(match_score, 2)

    sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

    return jsonify({"career_recommendations": sorted_recommendations[:5]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)





