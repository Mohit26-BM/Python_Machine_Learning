from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os
from supabase import create_client

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)

# ── Load Model ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "loan_model.pkl"))
model_columns = joblib.load(os.path.join(BASE_DIR, "model_columns.pkl"))

# ── Supabase ───────────────────────────────────────────────────────────────────
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
)

# ── Encoding Maps ──────────────────────────────────────────────────────────────
gender_map = {"Male": 1, "Female": 0}
married_map = {"Yes": 1, "No": 0}
education_map = {"Graduate": 1, "Not Graduate": 0}
self_employed_map = {"Yes": 1, "No": 0}
property_map = {"Urban": 2, "Semiurban": 1, "Rural": 0}

# ── Routes ─────────────────────────────────────────────────────────────────────


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET"])
def predict_page():
    return render_template("predict.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        required = [
            "gender",
            "married",
            "dependents",
            "education",
            "self_employed",
            "applicant_income",
            "coapplicant_income",
            "loan_amount",
            "loan_term",
            "credit_history",
            "property_area",
        ]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        if float(data["applicant_income"]) <= 0:
            return jsonify({"error": "Applicant income must be greater than 0"}), 400
        if float(data["loan_amount"]) <= 0:
            return jsonify({"error": "Loan amount must be greater than 0"}), 400

        input_data = {
            "Gender": gender_map.get(data["gender"], 1),
            "Married": married_map.get(data["married"], 0),
            "Dependents": int(data["dependents"]),
            "Education": education_map.get(data["education"], 1),
            "Self_Employed": self_employed_map.get(data["self_employed"], 0),
            "ApplicantIncome": float(data["applicant_income"]),
            "CoapplicantIncome": float(data["coapplicant_income"]),
            "LoanAmount": float(data["loan_amount"]),
            "Loan_Amount_Term": float(data["loan_term"]),
            "Credit_History": float(data["credit_history"]),
            "Property_Area": property_map.get(data["property_area"], 1),
        }

        input_array = np.array([[input_data[col] for col in model_columns]])
        prediction = model.predict(input_array)[0]
        proba = model.predict_proba(input_array)[0]
        confidence = round(float(max(proba)) * 100, 1)
        result_label = "Approved" if prediction == 1 else "Rejected"

        try:
            supabase.table("loan_predictions").insert(
                {
                    "gender": data["gender"],
                    "married": data["married"],
                    "dependents": int(data["dependents"]),
                    "education": data["education"],
                    "self_employed": data["self_employed"],
                    "applicant_income": float(data["applicant_income"]),
                    "coapplicant_income": float(data["coapplicant_income"]),
                    "loan_amount": float(data["loan_amount"]),
                    "loan_term": float(data["loan_term"]),
                    "credit_history": float(data["credit_history"]),
                    "property_area": data["property_area"],
                    "prediction": result_label,
                    "confidence": confidence,
                }
            ).execute()
        except Exception as db_err:
            print(f"DB save error: {db_err}")

        return jsonify({"prediction": result_label, "confidence": confidence})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/dashboard")
def dashboard():
    try:
        response = (
            supabase.table("loan_predictions")
            .select(
                "prediction, confidence, property_area, education, gender, applicant_income, credit_history"
            )
            .order("created_at", desc=False)
            .execute()
        )
        records = response.data

        total = len(records)
        approved = sum(1 for r in records if r["prediction"] == "Approved")
        rejected = total - approved
        avg_conf = (
            round(sum(r["confidence"] for r in records) / total, 1) if total else 0
        )
        avg_income = (
            round(sum(r["applicant_income"] for r in records) / total, 0)
            if total
            else 0
        )

        # Property area breakdown
        area_counts = {"Urban": 0, "Semiurban": 0, "Rural": 0}
        for r in records:
            a = r["property_area"]
            if a in area_counts:
                area_counts[a] += 1

        # Education breakdown
        edu_counts = {"Graduate": 0, "Not Graduate": 0}
        for r in records:
            e = r["education"]
            if e in edu_counts:
                edu_counts[e] += 1

        # Approval by credit history
        good_credit_approved = sum(
            1
            for r in records
            if r["credit_history"] == 1.0 and r["prediction"] == "Approved"
        )
        good_credit_rejected = sum(
            1
            for r in records
            if r["credit_history"] == 1.0 and r["prediction"] == "Rejected"
        )
        bad_credit_approved = sum(
            1
            for r in records
            if r["credit_history"] == 0.0 and r["prediction"] == "Approved"
        )
        bad_credit_rejected = sum(
            1
            for r in records
            if r["credit_history"] == 0.0 and r["prediction"] == "Rejected"
        )

        # Predictions over time (for line chart)
        predictions_timeline = [r["prediction"] for r in records]

    except Exception as e:
        print(f"Dashboard error: {e}")
        total = approved = rejected = avg_conf = avg_income = 0
        area_counts = {"Urban": 0, "Semiurban": 0, "Rural": 0}
        edu_counts = {"Graduate": 0, "Not Graduate": 0}
        good_credit_approved = good_credit_rejected = bad_credit_approved = (
            bad_credit_rejected
        ) = 0
        predictions_timeline = []

    return render_template(
        "dashboard.html",
        total=total,
        approved=approved,
        rejected=rejected,
        avg_conf=avg_conf,
        avg_income=int(avg_income),
        area_counts=area_counts,
        edu_counts=edu_counts,
        good_credit_approved=good_credit_approved,
        good_credit_rejected=good_credit_rejected,
        bad_credit_approved=bad_credit_approved,
        bad_credit_rejected=bad_credit_rejected,
        predictions_timeline=predictions_timeline,
    )


@app.route("/history")
def history():
    try:
        response = (
            supabase.table("loan_predictions")
            .select("*")
            .order("created_at", desc=True)
            .limit(30)
            .execute()
        )
        rows = response.data
    except Exception as e:
        print(f"History error: {e}")
        rows = []

    return render_template("history.html", rows=rows)


# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
