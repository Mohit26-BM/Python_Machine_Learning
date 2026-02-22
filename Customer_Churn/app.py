from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from supabase import create_client
import os

app = Flask(__name__)

# -------------------------------
# Load Model + Encoders
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_data = pickle.load(open(os.path.join(BASE_DIR, "customer_churn_model.pkl"), "rb"))

model = model_data["model"]
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
    "TotalCharges",
]
encoders = pickle.load(open(os.path.join(BASE_DIR, "encoders.pkl"), "rb"))

# -------------------------------
# Supabase Client
# -------------------------------

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
)

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

        # Save to Supabase
        try:
            supabase.table("churn_predictions").insert({
                "gender":             data.get("gender"),
                "senior_citizen":     data.get("SeniorCitizen"),
                "partner":            data.get("Partner"),
                "dependents":         data.get("Dependents"),
                "tenure":             data.get("tenure"),
                "phone_service":      data.get("PhoneService"),
                "multiple_lines":     data.get("MultipleLines"),
                "internet_service":   data.get("InternetService"),
                "online_security":    data.get("OnlineSecurity"),
                "online_backup":      data.get("OnlineBackup"),
                "device_protection":  data.get("DeviceProtection"),
                "tech_support":       data.get("TechSupport"),
                "streaming_tv":       data.get("StreamingTV"),
                "streaming_movies":   data.get("StreamingMovies"),
                "contract":           data.get("Contract"),
                "paperless_billing":  data.get("PaperlessBilling"),
                "payment_method":     data.get("PaymentMethod"),
                "monthly_charges":    data.get("MonthlyCharges"),
                "total_charges":      data.get("TotalCharges"),
                "churn_probability":  prob_percent,
                "prediction":         label,
                "risk_level":         risk,
            }).execute()
        except Exception as db_error:
            print(f"Database save error: {db_error}")

        return jsonify(
            {"prediction": label, "churn_probability": prob_percent, "risk_level": risk}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history")
def history():
    try:
        response = (
            supabase.table("churn_predictions")
            .select("churn_probability, prediction, risk_level, created_at")
            .order("created_at", desc=True)
            .limit(20)
            .execute()
        )
        # Convert to tuples to match template's row[0], row[1], row[2], row[3] indexing
        rows = [
            (
                row["churn_probability"],
                row["prediction"],
                row["risk_level"],
                row["created_at"],
            )
            for row in response.data
        ]
    except Exception as e:
        print(f"History fetch error: {e}")
        rows = []

    return render_template("history.html", rows=rows)


@app.route("/dashboard")
def dashboard():
    try:
        # Fetch today's predictions
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        response = (
            supabase.table("churn_predictions")
            .select("churn_probability, risk_level")
            .execute()
        )
        records = response.data

        # Aggregate in Python (replaces SQL aggregation)
        total = len(records)
        avg_prob = round(sum(r["churn_probability"] for r in records) / total, 2) if total else 0
        high_risk = sum(1 for r in records if r["churn_probability"] >= 60)

        distribution = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}
        for r in records:
            level = r["risk_level"]
            if level in distribution:
                distribution[level] += 1

    except Exception as e:
        print(f"Dashboard fetch error: {e}")
        total, avg_prob, high_risk = 0, 0, 0
        distribution = {"Low": 0, "Medium": 0, "High": 0, "Critical": 0}

    return render_template(
        "dashboard.html",
        total=total,
        avg_prob=avg_prob,
        high_risk=high_risk,
        distribution=distribution,
    )


# -------------------------------
# Run App
# -------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

