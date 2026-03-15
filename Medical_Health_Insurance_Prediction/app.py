from flask import Flask, request, jsonify, render_template, redirect, make_response
import pickle
import pandas as pd
from supabase import create_client
import os
from datetime import datetime, timezone

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)

# ── Load Model ─────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
model_data = pickle.load(open(os.path.join(BASE_DIR, "insurance_model.pkl"), "rb"))
model      = model_data["model"]
feature_names = model_data["feature_names"]

# ── Supabase ───────────────────────────────────────────────────────────────────
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
)

# ── Encoding Maps ──────────────────────────────────────────────────────────────
sex_map    = {"male": 0, "female": 1}
smoker_map = {"yes": 1, "no": 0}
region_map = {"southwest": 1, "southeast": 0, "northwest": 3, "northeast": 2}

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET"])
def predict_page():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        age      = int(data["age"])
        bmi      = float(data["bmi"])
        children = int(data["children"])

        if not (1 <= age <= 100):
            return jsonify({"error": "Age must be between 1 and 100"}), 400
        if not (10 <= bmi <= 60):
            return jsonify({"error": "BMI must be between 10 and 60"}), 400
        if not (0 <= children <= 10):
            return jsonify({"error": "Children must be between 0 and 10"}), 400

        input_df = pd.DataFrame([{
            "age":      age,
            "sex":      sex_map[data["sex"].lower()],
            "bmi":      bmi,
            "children": children,
            "smoker":   smoker_map[data["smoker"].lower()],
            "region":   region_map[data["region"].lower()],
        }])[feature_names]

        predicted_charges = round(float(model.predict(input_df)[0]), 2)

        if predicted_charges >= 40000:
            risk = "Very High"
        elif predicted_charges >= 25000:
            risk = "High"
        elif predicted_charges >= 12000:
            risk = "Medium"
        else:
            risk = "Low"

        try:
            supabase.table("insurance_predictions").insert({
                "age":               age,
                "sex":               data["sex"].lower(),
                "bmi":               bmi,
                "children":          children,
                "smoker":            data["smoker"].lower(),
                "region":            data["region"].lower(),
                "predicted_charges": predicted_charges,
                "risk_level":        risk,
            }).execute()
        except Exception as db_error:
            print(f"Database save error: {db_error}")

        return jsonify({"predicted_charges": predicted_charges, "risk_level": risk})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/simulate", methods=["GET"])
def simulate_page():
    return render_template("simulate.html")


@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        data = request.json

        age      = int(data.get("age", 30))
        bmi      = float(data.get("bmi", 25))
        children = int(data.get("children", 0))
        sex      = data.get("sex", "male").lower()
        smoker   = data.get("smoker", "no").lower()
        region   = data.get("region", "southeast").lower()

        input_df = pd.DataFrame([{
            "age":      age,
            "sex":      sex_map.get(sex, 0),
            "bmi":      bmi,
            "children": children,
            "smoker":   smoker_map.get(smoker, 0),
            "region":   region_map.get(region, 0),
        }])[feature_names]

        predicted = round(float(model.predict(input_df)[0]), 2)

        if predicted >= 40000:   risk = "Very High"
        elif predicted >= 25000: risk = "High"
        elif predicted >= 12000: risk = "Medium"
        else:                    risk = "Low"

        return jsonify({"predicted_charges": predicted, "risk_level": risk})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/risk")
def risk_page():
    return render_template("risk.html")

@app.route("/history")
def history():
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    try:
        response = (
            supabase.table("insurance_predictions")
            .select(
                "age, sex, bmi, children, smoker, region, predicted_charges, risk_level, created_at"
            )
            .order("created_at", desc=False)
            .execute()
        )
        records = response.data

        total = len(records)
        avg_charges = (
            round(sum(r["predicted_charges"] for r in records) / total, 2)
            if total
            else 0
        )
        high_cost = sum(1 for r in records if r["predicted_charges"] >= 25000)
        smokers = sum(1 for r in records if r["smoker"] == "yes")

        distribution = {"Low": 0, "Medium": 0, "High": 0, "Very High": 0}
        for r in records:
            level = r["risk_level"]
            if level in distribution:
                distribution[level] += 1

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

        charges_over_time = [r["predicted_charges"] for r in records]

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

        history_response = (
            supabase.table("insurance_predictions")
            .select(
                "age, sex, bmi, children, smoker, region, predicted_charges, risk_level, created_at"
            )
            .order("created_at", desc=True)
            .limit(10)
            .execute()
        )
        history_rows = history_response.data

    except Exception as e:
        print(f"Dashboard fetch error: {e}")
        total = avg_charges = high_cost = smokers = smoker_avg = nonsmoker_avg = 0
        distribution = {"Low": 0, "Medium": 0, "High": 0, "Very High": 0}
        charges_over_time = []
        age_buckets = {"18-30": 0, "31-45": 0, "46-60": 0, "60+": 0}
        history_rows = []

    resp = make_response(
        render_template(
            "dashboard.html",
            total=total,
            avg_charges=avg_charges,
            high_cost=high_cost,
            smokers=smokers,
            distribution=distribution,
            smoker_avg=smoker_avg,
            nonsmoker_avg=nonsmoker_avg,
            history_rows=history_rows,
            charges_over_time=charges_over_time,
            age_buckets=age_buckets,
        )
    )
    resp.headers["Cache-Control"] = "no-store"
    return resp

# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
