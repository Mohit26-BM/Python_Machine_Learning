import joblib
import os
import streamlit as st

@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    model = joblib.load(os.path.join(base_dir, "best_model.pkl"))
    columns = joblib.load(os.path.join(base_dir, "model_columns.pkl"))
    return model, columns

fat_content_map = {"Low Fat": 0, "Regular": 1}
outlet_size_map = {"High": 0, "Medium": 1, "Small": 2}
outlet_location_map = {"Tier 1": 0, "Tier 2": 1, "Tier 3": 2}
outlet_type_map = {
    "Grocery Store": 0,
    "Supermarket Type1": 1,
    "Supermarket Type2": 2,
    "Supermarket Type3": 3,
}
outlet_id_map = {
    "OUT010": 0, "OUT013": 1, "OUT017": 2, "OUT018": 3, "OUT019": 4,
    "OUT027": 5, "OUT035": 6, "OUT045": 7, "OUT046": 8, "OUT049": 9,
}
item_type_map = {
    "Baking Goods": 0, "Breads": 1, "Breakfast": 2, "Canned": 3,
    "Dairy": 4, "Frozen Foods": 5, "Fruits and Vegetables": 6,
    "Hard Drinks": 7, "Health and Hygiene": 8, "Household": 9,
    "Meat": 10, "Others": 11, "Sea Food": 12, "Snack Foods": 13,
    "Soft Drinks": 14, "Starchy Foods": 15,
}
