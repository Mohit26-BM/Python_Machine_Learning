from flask import Flask, render_template, request
import joblib
import pandas as pd
from supabase import create_client
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Load trained model
model = joblib.load("rainfall_model.pkl")

# Init Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict")
def predict_page():
    return render_template("predict.html")


@app.route("/result", methods=["POST"])
def result():
    try:
        input_data = [
            float(request.form["pressure"]),
            float(request.form["dewpoint"]),
            float(request.form["humidity"]),
            float(request.form["cloud"]),
            float(request.form["sunshine"]),
            float(request.form["winddirection"]),
            float(request.form["windspeed"]),
        ]

        input_df = pd.DataFrame(
            [input_data],
            columns=[
                "pressure",
                "dewpoint",
                "humidity",
                "cloud",
                "sunshine",
                "winddirection",
                "windspeed",
            ],
        )

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        result_text = "Rainfall Expected" if prediction == 1 else "No Rainfall Expected"

        # Store in Supabase
        supabase.table("rain_predictions").insert(
            {
                "pressure": input_data[0],
                "dewpoint": input_data[1],
                "humidity": input_data[2],
                "cloud": input_data[3],
                "sunshine": input_data[4],
                "winddirection": input_data[5],
                "windspeed": input_data[6],
                "prediction": result_text,
                "probability": round(probability * 100, 2),
            }
        ).execute()

        return render_template(
            "result.html",
            prediction=result_text,
            probability=round(probability * 100, 2),
        )

    except Exception as e:
        print(f"Error: {e}")
        return "Error processing input."


@app.route("/whatif")
def whatif_page():
    return render_template("whatif.html")


@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame(
            [
                {
                    "pressure": float(data["pressure"]),
                    "dewpoint": float(data["dewpoint"]),
                    "humidity": float(data["humidity"]),
                    "cloud": float(data["cloud"]),
                    "sunshine": float(data["sunshine"]),
                    "winddirection": float(data["winddirection"]),
                    "windspeed": float(data["windspeed"]),
                }
            ]
        )

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        return jsonify(
            {
                "prediction": (
                    "Rainfall Expected" if prediction == 1 else "No Rainfall Expected"
                ),
                "probability": round(probability * 100, 2),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
