from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from supabase import create_client
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# -------------------------------
# Load Model
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_data = pickle.load(open(os.path.join(BASE_DIR, "insurance_model.pkl"), "rb"))
model = model_data["model"]
feature_names = model_data["feature_names"]

# -------------------------------
# Supabase Client
# -------------------------------

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
)

# -------------------------------
# Encoding Maps
# -------------------------------

sex_map     = {"male": 0, "female": 1}
smoker_map  = {"yes": 1, "no": 0}
region_map  = {"southwest": 1, "southeast": 0, "northwest": 3, "northeast": 2}

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

        # Encode categorical inputs
        sex     = sex_map.get(data["sex"].lower(), 0)
        smoker  = smoker_map.get(data["smoker"].lower(), 0)
        region  = region_map.get(data["region"].lower(), 0)

        # Build input dataframe in correct feature order
        input_df = pd.DataFrame([{
            "age":      int(data["age"]),
            "sex":      sex,
            "bmi":      float(data["bmi"]),
            "children": int(data["children"]),
            "smoker":   smoker,
            "region":   region,
        }])[feature_names]

        # Predict
        predicted_charges = round(float(model.predict(input_df)[0]), 2)

        # Risk classification based on predicted charge
        if predicted_charges >= 40000:
            risk = "Very High"
        elif predicted_charges >= 25000:
            risk = "High"
        elif predicted_charges >= 12000:
            risk = "Medium"
        else:
            risk = "Low"

        # Save to Supabase
        try:
            supabase.table("insurance_predictions").insert({
                "age":               int(data["age"]),
                "sex":               data["sex"].lower(),
                "bmi":               float(data["bmi"]),
                "children":          int(data["children"]),
                "smoker":            data["smoker"].lower(),
                "region":            data["region"].lower(),
                "predicted_charges": predicted_charges,
                "risk_level":        risk,
            }).execute()
        except Exception as db_error:
            print(f"Database save error: {db_error}")

        return jsonify({
            "predicted_charges": predicted_charges,
            "risk_level": risk,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/history")
def history():
    try:
        response = (
            supabase.table("insurance_predictions")
            .select("age, sex, bmi, children, smoker, region, predicted_charges, risk_level, created_at")
            .order("created_at", desc=True)
            .limit(20)
            .execute()
        )
        rows = [
            (
                row["age"],
                row["sex"],
                row["bmi"],
                row["children"],
                row["smoker"],
                row["region"],
                row["predicted_charges"],
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
        response = (
            supabase.table("insurance_predictions")
            .select("age, predicted_charges, risk_level, smoker")
            .order("created_at", desc=True)
            .limit(100)
            .execute()
        )

        records = response.data or []

        total = len(records)
        avg_charges = (
            round(sum(r["predicted_charges"] for r in records) / total, 2)
            if total
            else 0
        )

        high_cost = sum(1 for r in records if r["predicted_charges"] >= 25000)

        smokers = sum(1 for r in records if r["smoker"] == "yes")

        # ── Charges Over Time (Line Chart)
        charges_over_time = [r["predicted_charges"] for r in records]

        # ── Risk Distribution (Donut)
        distribution = {"Low": 0, "Medium": 0, "High": 0, "Very High": 0}
        for r in records:
            level = r["risk_level"]
            if level in distribution:
                distribution[level] += 1

        # ── Age Buckets (Bar Chart)
        age_buckets = {"18-30": 0, "31-45": 0, "46-60": 0, "60+": 0}
        for r in records:
            age = r["age"]
            if age <= 30:
                age_buckets["18-30"] += 1
            elif age <= 45:
                age_buckets["31-45"] += 1
            elif age <= 60:
                age_buckets["46-60"] += 1
            else:
                age_buckets["60+"] += 1

        # ── Smoker vs Non-Smoker Avg
        smoker_charges = [
            r["predicted_charges"] for r in records if r["smoker"] == "yes"
        ]
        nonsmoker_charges = [
            r["predicted_charges"] for r in records if r["smoker"] == "no"
        ]

        smoker_avg = (
            round(sum(smoker_charges) / len(smoker_charges), 2) if smoker_charges else 0
        )

        nonsmoker_avg = (
            round(sum(nonsmoker_charges) / len(nonsmoker_charges), 2)
            if nonsmoker_charges
            else 0
        )

    except Exception as e:
        print(f"Dashboard fetch error: {e}")

        total = avg_charges = high_cost = smokers = 0
        charges_over_time = []
        distribution = {"Low": 0, "Medium": 0, "High": 0, "Very High": 0}
        age_buckets = {}
        smoker_avg = nonsmoker_avg = 0

    return render_template(
        "dashboard.html",
        total=total,
        avg_charges=avg_charges,
        high_cost=high_cost,
        smokers=smokers,
        distribution=distribution,
        charges_over_time=charges_over_time,
        age_buckets=age_buckets,
        smoker_avg=smoker_avg,
        nonsmoker_avg=nonsmoker_avg,
    )


# -------------------------------
# Run App
# -------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
