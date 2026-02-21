import streamlit as st
import pandas as pd
from supabase import create_client

@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def fetch_predictions(supabase_client):
    response = supabase_client.table("bigmart_predictions").select("*").execute()
    df = pd.DataFrame(response.data)
    if df.empty:
        return df
    rename_map = {
        "item_weight":        "Item_Weight",
        "item_fat_content":   "Item_Fat_Content",
        "item_visibility":    "Item_Visibility",
        "item_type":          "Item_Type",
        "item_mrp":           "Item_MRP",
        "outlet_identifier":  "Outlet_Identifier",
        "outlet_year":        "Outlet_Establishment_Year",
        "outlet_size":        "Outlet_Size",
        "outlet_location":    "Outlet_Location_Type",
        "outlet_type":        "Outlet_Type",
        "predicted_sales":    "Predicted_Sales",
    }
    df = df.rename(columns=rename_map)
    df = df[[c for c in rename_map.values() if c in df.columns]]
    return df
