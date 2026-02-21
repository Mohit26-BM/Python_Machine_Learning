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
    background: #F9FBFD !important;
    font-family: 'Inter', sans-serif;
    color: #1F2937;
}

[data-testid="stAppViewContainer"] > .main { background: #F9FBFD !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #F9FBFD; }
::-webkit-scrollbar-thumb { background: #DBEAFE; border-radius: 2px; }

/* ── Navbar ───────────────────────────────────────────────────────── */
.navbar-wrapper {
    background: #FFFFFF;
    border-bottom: 1px solid #E5E7EB;
    padding: 0 48px;
    position: sticky;
    top: 0;
    z-index: 100;
}

/* ── Page Wrapper ─────────────────────────────────────────────────── */
.page-wrapper {
    padding: 24px 48px 80px;
    max-width: 1280px;
    margin: 0 auto;
}

/* ── Typography ───────────────────────────────────────────────────── */
.page-title {
    font-family: 'Inter', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #1F2937;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin-bottom: 6px;
}

.page-subtitle {
    font-size: 0.93rem;
    color: #6B7280;
    font-weight: 400;
    margin-bottom: 32px;
}

.accent { color: #3B82F6; }

/* ── Cards ────────────────────────────────────────────────────────── */
.card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    transition: border-color 0.2s, box-shadow 0.2s;
}

.card:hover {
    border-color: #DBEAFE;
    box-shadow: 0 4px 16px rgba(59,130,246,0.08);
}

.card-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6B7280;
    margin-bottom: 18px;
}

/* ── Metric Row ───────────────────────────────────────────────────── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

.metric-value {
    font-family: 'Inter', sans-serif;
    font-size: 1.7rem;
    font-weight: 800;
    color: #1F2937;
    line-height: 1;
    margin-bottom: 6px;
}

.metric-label {
    font-size: 0.76rem;
    color: #6B7280;
    font-weight: 500;
}

/* ── Result Banner ────────────────────────────────────────────────── */
.result-banner {
    background: linear-gradient(135deg, #DBEAFE 0%, #EFF6FF 100%);
    border: 1px solid #BFDBFE;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    margin: 24px 0;
}

.result-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3B82F6;
    margin-bottom: 8px;
}

.result-value {
    font-family: 'Inter', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #1F2937;
    letter-spacing: -0.03em;
}

.result-sub {
    font-size: 0.8rem;
    color: #6B7280;
    margin-top: 8px;
}

/* ── Widget Labels ────────────────────────────────────────────────── */
label[data-testid="stWidgetLabel"] p {
    color: #374151 !important;
    font-size: 0.84rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}

/* ── Inputs ───────────────────────────────────────────────────────── */
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #FFFFFF !important;
    border-color: #E5E7EB !important;
    color: #1F2937 !important;
}

/* ── Buttons ──────────────────────────────────────────────────────── */
.stButton > button {
    background: #3B82F6 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 12px 28px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(59,130,246,0.25) !important;
}

.stButton > button:hover {
    background: #2563EB !important;
    box-shadow: 0 4px 16px rgba(59,130,246,0.35) !important;
    transform: translateY(-1px) !important;
}

/* Secondary nav buttons */
.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #374151 !important;
    border: 1px solid #E5E7EB !important;
    box-shadow: none !important;
}

.stButton > button[kind="secondary"]:hover {
    background: #DBEAFE !important;
    color: #2563EB !important;
    border-color: #BFDBFE !important;
    box-shadow: none !important;
    transform: none !important;
}

.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #374151 !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
    box-shadow: none !important;
}

.stDownloadButton > button:hover {
    background: #DBEAFE !important;
    color: #2563EB !important;
    border-color: #BFDBFE !important;
}

/* ── Info / Success boxes ─────────────────────────────────────────── */
[data-testid="stInfo"] {
    background: #EFF6FF !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 10px !important;
    color: #1E40AF !important;
}

[data-testid="stSuccess"] {
    background: #F0FDF4 !important;
    border: 1px solid #BBF7D0 !important;
    border-radius: 10px !important;
}

[data-testid="stCaptionContainer"] p {
    color: #9CA3AF !important;
}

/* ── Dataframe ────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    overflow: hidden;
}

hr {
    border-color: #E5E7EB !important;
    margin: 20px 0 !important;
}
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
st.markdown('<div class="navbar-wrapper">', unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([3, 1, 1, 1])

with nav_col1:
    st.markdown(
        """
        <div style="padding: 16px 0 10px; font-family: 'Inter', sans-serif;
                    font-weight: 800; font-size: 1.5rem; color: #1F2937; letter-spacing:-0.02em;">
            Big<span style="color:#3B82F6;">Mart</span> Predictor
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

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Routing ────────────────────────────────────────────────────────────────────
if st.session_state.page == "Predict":
    render_predict(model, model_columns, supabase_client)
elif st.session_state.page == "Dashboard":
    render_dashboard(supabase_client)
elif st.session_state.page == "History":
    render_history(supabase_client)
