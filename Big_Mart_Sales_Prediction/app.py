import streamlit as st
from utils.model import load_model
from utils.database import init_supabase
from pages.predict import render as render_predict
from pages.dashboard import render as render_dashboard
from pages.history import render as render_history

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

# ── Load Resources ─────────────────────────────────────────────────────────────
model, model_columns = load_model()
supabase_client      = init_supabase()

# ── Session State ──────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Predict"

# ── Navbar ─────────────────────────────────────────────────────────────────────
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([3, 1, 1, 1])

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
    if st.button(
        "Predict", key="nav_predict",
        type="primary" if st.session_state.page == "Predict" else "secondary",
    ):
        st.session_state.page = "Predict"
        st.rerun()

with nav_col3:
    if st.button(
        "Dashboard", key="nav_dash",
        type="primary" if st.session_state.page == "Dashboard" else "secondary",
    ):
        st.session_state.page = "Dashboard"
        st.rerun()

with nav_col4:
    if st.button(
        "History", key="nav_history",
        type="primary" if st.session_state.page == "History" else "secondary",
    ):
        st.session_state.page = "History"
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ── Routing ────────────────────────────────────────────────────────────────────
if st.session_state.page == "Predict":
    render_predict(model, model_columns, supabase_client)
elif st.session_state.page == "Dashboard":
    render_dashboard(supabase_client)
elif st.session_state.page == "History":
    render_history(supabase_client)
