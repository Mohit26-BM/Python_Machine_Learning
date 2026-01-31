from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import sqlite3

app = Flask(__name__)

model_data = pickle.load(open("customer_churn_model.pkl", "rb"))
model = model_data["model"]
feature_names = model_data["feature_names"]
encoders = pickle.load(open("encoders.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        df = pd.DataFrame([data])

        for col, enc in encoders.items():
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: enc.transform([x])[0] if x in enc.classes_ else -1
                )

        df = df[feature_names]

        prob = model.predict_proba(df)[0][1]
        pred = int(prob >= 0.5)
        label = "Churn" if pred else "No Churn"

        prob = round(prob * 100, 2)

        if prob >= 80:
            risk = "Critical"
        elif prob >= 60:
            risk = "High"
        elif prob >= 40:
            risk = "Medium"
        else:
            risk = "Low"

        with get_db() as conn:
            conn.execute(
                "INSERT INTO predictions (churn_probability, prediction, risk_level) VALUES (?, ?, ?)",
                (prob, label, risk)
            )
            conn.commit

        return jsonify({
            "prediction": label,
            "churn_probability": prob,
            "risk_level": risk
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_db():
    return sqlite3.connect("predictions.db", check_same_thread=False)


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
            SELECT risk_level, COUNT(*) as count
            FROM predictions
            GROUP BY risk_level
        """
        ).fetchall()

        distribution = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}

        for risk_level, count in distribution_raw:
            if risk_level in distribution:
                distribution[risk_level] = count

    return render_template(
        "dashboard.html",
        total=today[0] or 0,
        avg_prob=round(today[1], 2) if today[1] else 0,
        high_risk=today[2] or 0,
        distribution=distribution,
    )

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
