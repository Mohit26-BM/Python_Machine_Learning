import streamlit as st
import pandas as pd
import numpy as np
import joblib
from supabase import create_client
import os

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BigMart Sales Predictor",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    font-family: 'Inter', sans-serif;
    color: #e8e6f0;
}

[data-testid="stAppViewContainer"] > .main { background: #0a0a0f !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #3d3a5c; border-radius: 2px; }

.page-wrapper {
    padding: 24px 48px 80px;
    max-width: 1280px;
    margin: 0 auto;
}

.page-title {
    font-family: 'Inter', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 6px;
}

.page-subtitle {
    font-size: 0.93rem;
    color: rgba(255,255,255,0.38);
    font-weight: 300;
    margin-bottom: 36px;
}

.accent { color: #7c6af7; }

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
    transition: border-color 0.2s;
}

.card:hover { border-color: rgba(124,106,247,0.22); }

.card-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.32);
    margin-bottom: 20px;
}

.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}

.metric-card {
    background: rgba(124,106,247,0.07);
    border: 1px solid rgba(124,106,247,0.16);
    border-radius: 14px;
    padding: 22px;
    text-align: center;
}

.metric-value {
    font-family: 'Inter', sans-serif;
    font-size: 1.7rem;
    font-weight: 800;
    color: #fff;
    line-height: 1;
    margin-bottom: 6px;
}

.metric-label {
    font-size: 0.76rem;
    color: rgba(255,255,255,0.38);
}

.result-banner {
    background: linear-gradient(135deg, rgba(124,106,247,0.14) 0%, rgba(99,179,237,0.07) 100%);
    border: 1px solid rgba(124,106,247,0.28);
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    margin: 24px 0;
}

.result-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(124,106,247,0.8);
    margin-bottom: 8px;
}

.result-value {
    font-family: 'Inter', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.03em;
}

.result-sub {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.32);
    margin-top: 8px;
}

label[data-testid="stWidgetLabel"] p {
    color: rgba(255,255,255,0.55) !important;
    font-size: 0.82rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: #7c6af7 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 14px 32px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(124,106,247,0.3) !important;
}

.stButton > button:hover {
    background: #6a58e8 !important;
    box-shadow: 0 6px 28px rgba(124,106,247,0.48) !important;
    transform: translateY(-1px) !important;
}

.stDownloadButton > button {
    background: rgba(255,255,255,0.04) !important;
    color: rgba(255,255,255,0.65) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
}

[data-testid="stInfo"] {
    background: rgba(124,106,247,0.07) !important;
    border: 1px solid rgba(124,106,247,0.18) !important;
    border-radius: 10px !important;
}

[data-testid="stSuccess"] {
    background: rgba(72,199,142,0.08) !important;
    border: 1px solid rgba(72,199,142,0.22) !important;
    border-radius: 10px !important;
}

[data-testid="stCaptionContainer"] p { color: rgba(255,255,255,0.28) !important; }

hr { border-color: rgba(255,255,255,0.05) !important; margin: 28px 0 !important; }
</style>
""",
    unsafe_allow_html=True,
)


# ── Load Model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(__file__)
    model = joblib.load(os.path.join(base_dir, "best_model.pkl"))
    columns = joblib.load(os.path.join(base_dir, "model_columns.pkl"))
    return model, columns


@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


model, model_columns = load_model()
supabase_client = init_supabase()


# ── Helper — fetch from Supabase and normalise column names ────────────────────
def fetch_predictions():
    response = supabase_client.table("bigmart_predictions").select("*").execute()
    df = pd.DataFrame(response.data)
    if df.empty:
        return df
    # Rename Supabase snake_case columns back to display names
    rename_map = {
        "item_weight": "Item_Weight",
        "item_fat_content": "Item_Fat_Content",
        "item_visibility": "Item_Visibility",
        "item_type": "Item_Type",
        "item_mrp": "Item_MRP",
        "outlet_identifier": "Outlet_Identifier",
        "outlet_year": "Outlet_Establishment_Year",
        "outlet_size": "Outlet_Size",
        "outlet_location": "Outlet_Location_Type",
        "outlet_type": "Outlet_Type",
        "predicted_sales": "Predicted_Sales",
    }
    df = df.rename(columns=rename_map)
    # Drop internal Supabase columns if present
    df = df[[c for c in rename_map.values() if c in df.columns]]
    return df


# ── Mappings ───────────────────────────────────────────────────────────────────
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
    "OUT010": 0,
    "OUT013": 1,
    "OUT017": 2,
    "OUT018": 3,
    "OUT019": 4,
    "OUT027": 5,
    "OUT035": 6,
    "OUT045": 7,
    "OUT046": 8,
    "OUT049": 9,
}
item_type_map = {
    "Baking Goods": 0,
    "Breads": 1,
    "Breakfast": 2,
    "Canned": 3,
    "Dairy": 4,
    "Frozen Foods": 5,
    "Fruits and Vegetables": 6,
    "Hard Drinks": 7,
    "Health and Hygiene": 8,
    "Household": 9,
    "Meat": 10,
    "Others": 11,
    "Sea Food": 12,
    "Snack Foods": 13,
    "Soft Drinks": 14,
    "Starchy Foods": 15,
}

# ── Session State ──────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Predict"

# ── Navbar ─────────────────────────────────────────────────────────────────────
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([4, 1, 1, 1])

with nav_col1:
    st.markdown(
        """
        <div style="padding: 18px 0 10px; font-family: 'Inter', sans-serif;
                    font-weight: 800; font-size: 3.5rem; color: #fff; letter-spacing:-0.02em;">
            Big<span style="color:#7c6af7;">Mart</span> Predictor
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col2:
    st.markdown("<div style='padding-top:12px'>", unsafe_allow_html=True)
    if st.button(
        "Predict",
        key="nav_predict",
        type="primary" if st.session_state.page == "Predict" else "secondary",
    ):
        st.session_state.page = "Predict"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with nav_col3:
    st.markdown("<div style='padding-top:12px'>", unsafe_allow_html=True)
    if st.button(
        "Dashboard",
        key="nav_dash",
        type="primary" if st.session_state.page == "Dashboard" else "secondary",
    ):
        st.session_state.page = "Dashboard"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with nav_col4:
    st.markdown("<div style='padding-top:12px'>", unsafe_allow_html=True)
    if st.button(
        "History",
        key="nav_history",
        type="primary" if st.session_state.page == "History" else "secondary",
    ):
        st.session_state.page = "History"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — PREDICT
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "Predict":

    st.markdown(
        """
        <div style="padding: 20px 0 0 0;">
            <p style="font-size: 1.2rem; font-weight: 500;
                      color: rgba(255,255,255,0.65);
                      font-family: 'Inter', sans-serif;
                      margin: 0 0 24px 0;">
                Enter product and outlet details to get an instant sales forecast
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-wrapper" style="padding-top: 0;">', unsafe_allow_html=True
    )

    col_item, col_outlet = st.columns(2)

    with col_item:
        st.markdown(
            "<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
            "letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
            'margin:0 0 10px 0;">Item Details</p>',
            unsafe_allow_html=True,
        )
        item_weight = st.number_input(
            "Item Weight (kg)", min_value=1.0, max_value=25.0, value=12.0, step=0.1
        )
        item_fat_content = st.selectbox("Fat Content", list(fat_content_map.keys()))
        item_visibility = st.slider(
            "Item Visibility", 0.0, 0.35, 0.066, 0.001, format="%.3f"
        )
        item_type = st.selectbox("Item Type", list(item_type_map.keys()))
        item_mrp = st.number_input(
            "Item MRP (₹)", min_value=30.0, max_value=270.0, value=140.0, step=0.5
        )

    with col_outlet:
        st.markdown(
            "<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
            "letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
            'margin:0 0 10px 0;">Outlet Details</p>',
            unsafe_allow_html=True,
        )
        outlet_id = st.selectbox("Outlet ID", list(outlet_id_map.keys()))
        outlet_est_year = st.selectbox(
            "Establishment Year",
            sorted([1985, 1987, 1988, 1992, 1994, 1999, 2002, 2004, 2007, 2009]),
        )
        outlet_size = st.selectbox("Outlet Size", list(outlet_size_map.keys()))
        outlet_location = st.selectbox(
            "Location Type", list(outlet_location_map.keys())
        )
        outlet_type = st.selectbox("Outlet Type", list(outlet_type_map.keys()))

    st.markdown("<br>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        predict_clicked = st.button("Predict Sales", key="predict_btn")

    if predict_clicked:
        input_dict = {
            "Item_Weight": item_weight,
            "Item_Fat_Content": fat_content_map[item_fat_content],
            "Item_Visibility": item_visibility,
            "Item_Type": item_type_map[item_type],
            "Item_MRP": item_mrp,
            "Outlet_Identifier": outlet_id_map[outlet_id],
            "Outlet_Establishment_Year": outlet_est_year,
            "Outlet_Size": outlet_size_map[outlet_size],
            "Outlet_Location_Type": outlet_location_map[outlet_location],
            "Outlet_Type": outlet_type_map[outlet_type],
        }
        input_df = pd.DataFrame([input_dict])[model_columns]
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
        diff = prediction - avg_sales
        direction = "above" if diff > 0 else "below"
        st.info(
            f"This is **₹ {abs(diff):,.0f} {direction}** the dataset average of ₹ {avg_sales:,.0f}"
        )

        # Save to Supabase
        try:
            supabase_client.table("bigmart_predictions").insert(
                {
                    "item_weight": item_weight,
                    "item_fat_content": item_fat_content,
                    "item_visibility": round(item_visibility, 4),
                    "item_type": item_type,
                    "item_mrp": item_mrp,
                    "outlet_identifier": outlet_id,
                    "outlet_year": outlet_est_year,
                    "outlet_size": outlet_size,
                    "outlet_location": outlet_location,
                    "outlet_type": outlet_type,
                    "predicted_sales": round(float(prediction), 2),
                }
            ).execute()
            st.caption("Saved to predictions log — view in History")
        except Exception as e:
            st.warning(f"Prediction made but could not save to database: {e}")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Dashboard":

    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="page-title">Prediction <span class="accent">Dashboard</span></div>
        <div class="page-subtitle">Visual analytics of all recorded predictions</div>
        """,
        unsafe_allow_html=True,
    )

    try:
        log_df = fetch_predictions()

        if log_df.empty:
            raise ValueError("empty")

        st.markdown(
            f"""
            <div class="metric-row">
                <div class="metric-card">
                    <div class="metric-value">{len(log_df)}</div>
                    <div class="metric-label">Total Predictions</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">₹ {log_df['Predicted_Sales'].mean():,.0f}</div>
                    <div class="metric-label">Average Predicted Sales</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">₹ {log_df['Predicted_Sales'].max():,.0f}</div>
                    <div class="metric-label">Highest Prediction</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            st.markdown(
                "<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
                "letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
                'margin:0 0 10px 0;">Predicted Sales Over Time</p>',
                unsafe_allow_html=True,
            )
            ts = log_df[["Predicted_Sales"]].reset_index()
            ts.columns = ["Prediction #", "Predicted Sales (₹)"]
            st.line_chart(ts.set_index("Prediction #"), color="#7c6af7")

        with r1c2:
            st.markdown(
                "<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
                "letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
                'margin:0 0 10px 0;">Avg Sales by Outlet Type</p>',
                unsafe_allow_html=True,
            )
            ot = log_df.groupby("Outlet_Type")["Predicted_Sales"].mean().reset_index()
            ot.columns = ["Outlet Type", "Avg Sales (₹)"]
            st.bar_chart(ot.set_index("Outlet Type"), color="#7c6af7")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.markdown(
                "<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
                "letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
                'margin:0 0 10px 0;">Avg Sales by Item Type</p>',
                unsafe_allow_html=True,
            )
            it = log_df.groupby("Item_Type")["Predicted_Sales"].mean().reset_index()
            it.columns = ["Item Type", "Avg Sales (₹)"]
            st.bar_chart(it.set_index("Item Type"), color="#a78bfa")

        with r2c2:
            st.markdown(
                "<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
                "letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
                'margin:0 0 10px 0;">Avg Sales by Location Tier</p>',
                unsafe_allow_html=True,
            )
            lt = (
                log_df.groupby("Outlet_Location_Type")["Predicted_Sales"]
                .mean()
                .reset_index()
            )
            lt.columns = ["Location Tier", "Avg Sales (₹)"]
            st.bar_chart(lt.set_index("Location Tier"), color="#6ee7b7")

        r3c1, r3c2 = st.columns(2)
        with r3c1:
            if len(log_df) >= 3:
                st.markdown(
                    "<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
                    "letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
                    'margin:0 0 10px 0;">Item MRP vs Predicted Sales</p>',
                    unsafe_allow_html=True,
                )
                sc = log_df[["Item_MRP", "Predicted_Sales"]].copy()
                sc.columns = ["Item MRP (₹)", "Predicted Sales (₹)"]
                st.scatter_chart(
                    sc, x="Item MRP (₹)", y="Predicted Sales (₹)", color="#7c6af7"
                )

        with r3c2:
            st.markdown(
                "<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
                "letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
                'margin:0 0 10px 0;">Avg Sales by Fat Content</p>',
                unsafe_allow_html=True,
            )
            fc = (
                log_df.groupby("Item_Fat_Content")["Predicted_Sales"]
                .mean()
                .reset_index()
            )
            fc.columns = ["Fat Content", "Avg Sales (₹)"]
            st.bar_chart(fc.set_index("Fat Content"), color="#f472b6")

    except Exception:
        st.markdown(
            """
            <div class="card" style="text-align:center; padding:64px 32px;">
                <div class="page-title" style="font-size:1.5rem;">No predictions yet</div>
                <div class="page-subtitle" style="margin-bottom:0">
                    Head over to the Predict tab and make your first prediction.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "History":

    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="page-title">Prediction <span class="accent">History</span></div>
        <div class="page-subtitle">Full log of every prediction — browse, filter, and export</div>
        """,
        unsafe_allow_html=True,
    )

    try:
        log_df = fetch_predictions()

        if log_df.empty:
            raise ValueError("empty")

        st.markdown(
            f"""
            <div class="metric-row">
                <div class="metric-card">
                    <div class="metric-value">{len(log_df)}</div>
                    <div class="metric-label">Total Records</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">₹ {log_df['Predicted_Sales'].min():,.0f}</div>
                    <div class="metric-label">Lowest Prediction</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">₹ {log_df['Predicted_Sales'].max():,.0f}</div>
                    <div class="metric-label">Highest Prediction</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
            "letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
            'margin:0 0 10px 0;">Filter Records</p>',
            unsafe_allow_html=True,
        )

        f1, f2, f3 = st.columns(3)
        with f1:
            outlet_filter = st.multiselect(
                "Outlet ID",
                options=sorted(log_df["Outlet_Identifier"].unique()),
                default=sorted(log_df["Outlet_Identifier"].unique()),
            )
        with f2:
            type_filter = st.multiselect(
                "Outlet Type",
                options=sorted(log_df["Outlet_Type"].unique()),
                default=sorted(log_df["Outlet_Type"].unique()),
            )
        with f3:
            min_s = float(log_df["Predicted_Sales"].min())
            max_s = float(log_df["Predicted_Sales"].max())
            sales_range = st.slider(
                "Predicted Sales Range (₹)", min_s, max_s, (min_s, max_s), step=10.0
            )

        filtered_df = log_df[
            (log_df["Outlet_Identifier"].isin(outlet_filter))
            & (log_df["Outlet_Type"].isin(type_filter))
            & (log_df["Predicted_Sales"] >= sales_range[0])
            & (log_df["Predicted_Sales"] <= sales_range[1])
        ].reset_index(drop=True)

        st.markdown(
            f"<p style=\"font-family:'Inter',sans-serif; font-size:0.75rem; font-weight:700;"
            f"letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);"
            f'margin:16px 0 10px 0;">Showing {len(filtered_df)} of {len(log_df)} records</p>',
            unsafe_allow_html=True,
        )
        st.dataframe(
            filtered_df.style.highlight_max(
                subset=["Predicted_Sales"], color="rgba(124,106,247,0.18)"
            ).highlight_min(subset=["Predicted_Sales"], color="rgba(244,114,182,0.14)"),
            use_container_width=True,
            height=480,
        )
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Filtered CSV",
            csv,
            file_name="bigmart_predictions_filtered.csv",
            mime="text/csv",
            use_container_width=True,
        )

    except Exception:
        st.markdown(
            """
            <div class="card" style="text-align:center; padding:64px 32px;">
                <div class="page-title" style="font-size:1.5rem;">No history yet</div>
                <div class="page-subtitle" style="margin-bottom:0">
                    Head over to the Predict tab and make your first prediction.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
