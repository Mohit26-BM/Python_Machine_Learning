import streamlit as st
import pandas as pd
from utils.model import (
    fat_content_map, outlet_size_map, outlet_location_map,
    outlet_type_map, outlet_id_map, item_type_map
)

def render(model, model_columns, supabase_client):

    st.markdown('<div class="predict-bg">', unsafe_allow_html=True)
    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

    st.markdown("""
        <div class="page-title">Sales <span style="color:#0D9488;">Predictor</span></div>
        <div class="page-subtitle" style="color:#64748B;">
            Enter product and outlet details to get an instant sales forecast
        </div>
    """, unsafe_allow_html=True)

    col_item, col_outlet = st.columns(2)

    with col_item:
        st.markdown(
            '<p class="section-label">Item Details</p>',
            unsafe_allow_html=True,
        )
        item_weight      = st.number_input("Item Weight (kg)", min_value=1.0, max_value=25.0, value=12.0, step=0.1)
        item_fat_content = st.selectbox("Fat Content", list(fat_content_map.keys()))
        item_visibility  = st.slider("Item Visibility", 0.0, 0.35, 0.066, 0.001, format="%.3f")
        item_type        = st.selectbox("Item Type", list(item_type_map.keys()))
        item_mrp         = st.number_input("Item MRP (₹)", min_value=30.0, max_value=270.0, value=140.0, step=0.5)

    with col_outlet:
        st.markdown(
            '<p class="section-label">Outlet Details</p>',
            unsafe_allow_html=True,
        )
        outlet_id       = st.selectbox("Outlet ID", list(outlet_id_map.keys()))
        outlet_est_year = st.selectbox("Establishment Year", sorted([1985,1987,1988,1992,1994,1999,2002,2004,2007,2009]))
        outlet_size     = st.selectbox("Outlet Size", list(outlet_size_map.keys()))
        outlet_location = st.selectbox("Location Type", list(outlet_location_map.keys()))
        outlet_type     = st.selectbox("Outlet Type", list(outlet_type_map.keys()))

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        predict_clicked = st.button("Predict Sales", key="predict_btn")

    if predict_clicked:
        input_dict = {
            "Item_Weight":               item_weight,
            "Item_Fat_Content":          fat_content_map[item_fat_content],
            "Item_Visibility":           item_visibility,
            "Item_Type":                 item_type_map[item_type],
            "Item_MRP":                  item_mrp,
            "Outlet_Identifier":         outlet_id_map[outlet_id],
            "Outlet_Establishment_Year": outlet_est_year,
            "Outlet_Size":               outlet_size_map[outlet_size],
            "Outlet_Location_Type":      outlet_location_map[outlet_location],
            "Outlet_Type":               outlet_type_map[outlet_type],
        }
        input_df   = pd.DataFrame([input_dict])[model_columns]
        prediction = model.predict(input_df)[0]

        st.markdown(
            f"""
            <div class="result-banner">
                <div class="result-label">Predicted Outlet Sales</div>
                <div class="result-value">₹ {prediction:,.0f}</div>
                <div class="result-sub">XGBoost · R² = 0.589 · MAE ≈ ₹788</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        avg_sales = 2181.29
        diff      = prediction - avg_sales
        direction = "above" if diff > 0 else "below"
        st.info(f"This is **₹ {abs(diff):,.0f} {direction}** the dataset average of ₹ {avg_sales:,.0f}")

        try:
            supabase_client.table("bigmart_predictions").insert({
                "item_weight":       item_weight,
                "item_fat_content":  item_fat_content,
                "item_visibility":   round(item_visibility, 4),
                "item_type":         item_type,
                "item_mrp":          item_mrp,
                "outlet_identifier": outlet_id,
                "outlet_year":       outlet_est_year,
                "outlet_size":       outlet_size,
                "outlet_location":   outlet_location,
                "outlet_type":       outlet_type,
                "predicted_sales":   round(float(prediction), 2),
            }).execute()
            st.caption("Saved to predictions log — view in History")
        except Exception as e:
            st.warning(f"Prediction made but could not save to database: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
