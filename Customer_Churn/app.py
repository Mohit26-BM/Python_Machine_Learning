from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

# -------------------------------
# Load Model + Encoders
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "customer_churn_model.pkl"), "rb"))
#model_data = pickle.load(open(os.path.join(BASE_DIR, "customer_churn_model.pkl"), "rb"))
#feature_names = model_data["feature_names"]
feature_names = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges"
]
encoders = pickle.load(open(os.path.join(BASE_DIR, "encoders.pkl"), "rb"))


# -------------------------------
# Database Functions
# -------------------------------


def get_db():
    return sqlite3.connect(os.path.join(BASE_DIR, "predictions.db"))


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                churn_probability REAL,
                prediction TEXT,
                risk_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


# -------------------------------
# Routes
# -------------------------------


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])

        # Encode categorical features safely
        for col, enc in encoders.items():
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: enc.transform([x])[0] if x in enc.classes_ else -1
                )

        df = df[feature_names]

        # Prediction
        prob = model.predict_proba(df)[0][1]
        label = "Churn" if prob >= 0.5 else "No Churn"
        prob_percent = round(prob * 100, 2)

        # Risk Classification
        if prob_percent >= 80:
            risk = "Critical"
        elif prob_percent >= 60:
            risk = "High"
        elif prob_percent >= 40:
            risk = "Medium"
        else:
            risk = "Low"

        # Save to DB
        with get_db() as conn:
            conn.execute(
                "INSERT INTO predictions (churn_probability, prediction, risk_level) VALUES (?, ?, ?)",
                (prob_percent, label, risk),
            )
            conn.commit()

        return jsonify(
            {"prediction": label, "churn_probability": prob_percent, "risk_level": risk}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history")
def history():
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT churn_probability, prediction, risk_level, created_at
            FROM predictions
            ORDER BY created_at DESC
            LIMIT 20
        """
        ).fetchall()

    return render_template("history.html", rows=rows)


@app.route("/dashboard")
def dashboard():
    with get_db() as conn:
        today = conn.execute(
            """
            SELECT
                COUNT(*) AS total,
                AVG(churn_probability) AS avg_prob,
                SUM(CASE WHEN churn_probability >= 60 THEN 1 ELSE 0 END) AS high_risk
            FROM predictions
            WHERE DATE(created_at) = DATE('now')
        """
        ).fetchone()

        distribution_raw = conn.execute(
            """
            SELECT risk_level, COUNT(*)
            FROM predictions
            GROUP BY risk_level
        """
        ).fetchall()

    distribution = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}

    for level, count in distribution_raw:
        if level in distribution:
            distribution[level] = count

    return render_template(
        "dashboard.html",
        total=today[0] or 0,
        avg_prob=round(today[1], 2) if today[1] else 0,
        high_risk=today[2] or 0,
        distribution=distribution,
    )


# -------------------------------
# Run App
# -------------------------------
init_db()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

