from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load model
model = joblib.load("best_model.pkl")

# Explicit ordered feature list matching training
MODEL_FEATURES = [
    "Item_Weight",
    "Item_Fat_Content",
    "Item_Visibility",
    "Item_Type",
    "Item_MRP",
    "Outlet_Identifier",
    "Outlet_Establishment_Year",
    "Outlet_Size",
    "Outlet_Location_Type",
    "Outlet_Type",
]

# Supabase client — credentials must be set as environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set as environment variables. "
        "Create a .env file locally or set them in your deployment dashboard."
    )

sb = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Label encoding maps (replicated from training) ──
ENCODINGS = {
    "Item_Fat_Content": {
        "Low Fat": 0,
        "Regular": 1,
    },
    "Item_Type": {
        "Baking Goods": 0, "Breads": 1, "Breakfast": 2, "Canned": 3,
        "Dairy": 4, "Frozen Foods": 5, "Fruits and Vegetables": 6,
        "Hard Drinks": 7, "Health and Hygiene": 8, "Household": 9,
        "Meat": 10, "Others": 11, "Seafood": 12, "Snack Foods": 13,
        "Soft Drinks": 14, "Starchy Foods": 15,
    },
    "Outlet_Identifier": {
        "OUT010": 0, "OUT013": 1, "OUT017": 2, "OUT018": 3, "OUT019": 4,
        "OUT027": 5, "OUT035": 6, "OUT045": 7, "OUT046": 8, "OUT049": 9,
    },
    "Outlet_Size": {
        "High": 0, "Medium": 1, "Small": 2,
    },
    "Outlet_Location_Type": {
        "Tier 1": 0, "Tier 2": 1, "Tier 3": 2,
    },
    "Outlet_Type": {
        "Grocery Store": 0, "Supermarket Type1": 1,
        "Supermarket Type2": 2, "Supermarket Type3": 3,
    },
}

# Normalization guards — catch dirty values before encoding lookup
NORMALIZERS = {
    "Item_Fat_Content": {
        "LF": "Low Fat", "low fat": "Low Fat",
        "reg": "Regular", "REG": "Regular",
    },
    "Outlet_Size": {
        "high": "High", "medium": "Medium", "small": "Small",
        "": None,
    },
}


def normalize(field, value):
    """Apply normalization map for a field if one exists, else return as-is."""
    if field in NORMALIZERS:
        return NORMALIZERS[field].get(value, value)
    return value


def encode(scenario):
    """Normalize and label-encode all categorical inputs."""
    def safe_encode(field, raw):
        val = normalize(field, str(raw).strip() if raw is not None else "")
        if val is None:
            raise ValueError(f"Missing value for {field}")
        if val not in ENCODINGS[field]:
            raise ValueError(
                f"Unknown value '{val}' for {field}. "
                f"Valid options: {list(ENCODINGS[field].keys())}"
            )
        return ENCODINGS[field][val]

    return {
        "Item_Weight":               float(scenario["Item_Weight"]),
        "Item_Fat_Content":          safe_encode("Item_Fat_Content", scenario.get("Item_Fat_Content")),
        "Item_Visibility":           float(scenario["Item_Visibility"]),
        "Item_Type":                 safe_encode("Item_Type", scenario.get("Item_Type")),
        "Item_MRP":                  float(scenario["Item_MRP"]),
        "Outlet_Identifier":         safe_encode("Outlet_Identifier", scenario.get("Outlet_Identifier")),
        "Outlet_Establishment_Year": int(scenario["Outlet_Establishment_Year"]),
        "Outlet_Size":               safe_encode("Outlet_Size", scenario.get("Outlet_Size")),
        "Outlet_Location_Type":      safe_encode("Outlet_Location_Type", scenario.get("Outlet_Location_Type")),
        "Outlet_Type":               safe_encode("Outlet_Type", scenario.get("Outlet_Type")),
    }


def make_prediction(scenario):
    """Encode inputs and run model prediction."""
    encoded  = encode(scenario)
    input_df = pd.DataFrame([encoded])[MODEL_FEATURES]
    return round(float(model.predict(input_df)[0]), 2)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict")
def predict_page():
    return render_template("predict.html")


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        supabase_url=SUPABASE_URL,
        supabase_key=SUPABASE_KEY,
    )


@app.route("/simulator")
def simulator():
    return render_template("simulator.html")


@app.route("/compare")
def compare():
    return render_template("compare.html")


@app.route("/insights")
def insights():
    return render_template("insights.html")


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data       = request.get_json()
        prediction = make_prediction(data)

        sb.table("bigmart_predictions").insert({
            "item_weight":      data.get("Item_Weight"),
            "item_fat_content": data.get("Item_Fat_Content"),
            "item_visibility":  data.get("Item_Visibility"),
            "item_type":        data.get("Item_Type"),
            "item_mrp":         data.get("Item_MRP"),
            "outlet_identifier": data.get("Outlet_Identifier"),
            "outlet_year":      data.get("Outlet_Establishment_Year"),
            "outlet_size":      data.get("Outlet_Size"),
            "outlet_location":  data.get("Outlet_Location_Type"),
            "outlet_type":      data.get("Outlet_Type"),
            "predicted_sales":  prediction,
        }).execute()

        return jsonify({"success": True, "prediction": prediction})

    except (ValueError, KeyError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/compare", methods=["POST"])
def compare_predict():
    try:
        data   = request.get_json()
        pred_a = make_prediction(data["a"])
        pred_b = make_prediction(data["b"])
        return jsonify({"success": True, "a": pred_a, "b": pred_b})

    except (ValueError, KeyError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/feature-importance")
def feature_importance():
    try:
        importances  = model.feature_importances_
        categoricals = [
            "Item_Fat_Content", "Item_Type", "Outlet_Size",
            "Outlet_Location_Type", "Outlet_Type", "Outlet_Identifier",
        ]
        groups = {}
        for col, score in zip(MODEL_FEATURES, importances):
            parent = None
            for cat in categoricals:
                if col.startswith(cat):
                    parent = cat.replace("_", " ")
                    break
            if parent is None:
                parent = col.replace("_", " ")
            groups[parent] = groups.get(parent, 0) + float(score)

        sorted_items = sorted(groups.items(), key=lambda x: x[1], reverse=True)
        total        = sum(v for _, v in sorted_items)
        result       = [
            {"feature": label, "score": round(score, 6), "pct": round(score / total * 100, 1)}
            for label, score in sorted_items
        ]
        return jsonify({"success": True, "data": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
