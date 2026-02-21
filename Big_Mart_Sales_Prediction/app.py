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
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    color: #1F2937;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 2px; }

/* ── Brand Header ─────────────────────────────────────────────────── */
.brand-bar {
    background: #1E293B;
    padding: 14px 48px;
    display: flex;
    align-items: center;
}

.brand-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.02em;
}

.brand-accent { color: #60A5FA; }

/* ── Tabs ─────────────────────────────────────────────────────────── */
[data-testid="stTabs"] {
    background: #1E293B !important;
    padding: 0 48px !important;
}

button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.6) !important;
    padding: 14px 20px !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}

button[data-baseweb="tab"]:hover {
    color: #fff !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #60A5FA !important;
    border-bottom: 2px solid #60A5FA !important;
    font-weight: 600 !important;
}

[data-testid="stTabPanel"] {
    padding: 0 !important;
}

/* ── Shared Page Wrapper ──────────────────────────────────────────── */
.page-wrapper {
    padding: 28px 48px 80px;
    max-width: 1280px;
    margin: 0 auto;
}

/* ── Shared Typography ────────────────────────────────────────────── */
.page-title {
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin-bottom: 4px;
}

.page-subtitle {
    font-size: 0.9rem;
    font-weight: 400;
    margin-bottom: 28px;
}

/* ══════════════════════════════════════════════════════════════════
   PREDICT PAGE COLORS
══════════════════════════════════════════════════════════════════ */
.predict-bg { background: #F8FAFC; }

.predict-bg .page-title { color: #1E293B; }
.predict-bg .page-subtitle { color: #64748B; }

.predict-bg label[data-testid="stWidgetLabel"] p {
    color: #374151 !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
}

.predict-bg .section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 10px;
}

.result-banner {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
    border: 1px solid #86EFAC;
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
    color: #16A34A;
    margin-bottom: 8px;
}

.result-value {
    font-size: 3rem;
    font-weight: 800;
    color: #15803D;
    letter-spacing: -0.03em;
}

.result-sub {
    font-size: 0.8rem;
    color: #6B7280;
    margin-top: 8px;
}

/* Predict Button — teal */
.predict-bg .stButton > button {
    background: #0D9488 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 12px 28px !important;
    width: 100% !important;
    box-shadow: 0 2px 8px rgba(13,148,136,0.3) !important;
    transition: all 0.2s ease !important;
}

.predict-bg .stButton > button:hover {
    background: #0F766E !important;
    box-shadow: 0 4px 16px rgba(13,148,136,0.4) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stInfo"] {
    background: #F0FDF4 !important;
    border: 1px solid #86EFAC !important;
    border-radius: 10px !important;
}

/* ══════════════════════════════════════════════════════════════════
   DASHBOARD PAGE COLORS
══════════════════════════════════════════════════════════════════ */
.dashboard-bg { background: #F1F5F9; }

.dashboard-bg .page-title { color: #1E293B; }
.dashboard-bg .page-subtitle { color: #64748B; }

.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.metric-value {
    font-size: 1.7rem;
    font-weight: 800;
    color: #1E293B;
    line-height: 1;
    margin-bottom: 6px;
}

.metric-label {
    font-size: 0.76rem;
    color: #64748B;
    font-weight: 500;
}

.dashboard-bg .section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 10px;
}

/* ══════════════════════════════════════════════════════════════════
   HISTORY PAGE COLORS
══════════════════════════════════════════════════════════════════ */
.history-bg { background: #F9FAFB; }

.history-bg .page-title { color: #1E293B; }
.history-bg .page-subtitle { color: #64748B; }

.history-bg .section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 10px;
}

/* ── Download Button ──────────────────────────────────────────────── */
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #374151 !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    width: 100% !important;
    font-weight: 500 !important;
}

.stDownloadButton > button:hover {
    background: #DBEAFE !important;
    color: #1E40AF !important;
    border-color: #BFDBFE !important;
}

/* ── Caption ──────────────────────────────────────────────────────── */
[data-testid="stCaptionContainer"] p { color: #9CA3AF !important; }

hr { border-color: #E2E8F0 !important; margin: 16px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Load Resources ─────────────────────────────────────────────────────────────
model, model_columns = load_model()
supabase_client      = init_supabase()

# ── Brand Header ───────────────────────────────────────────────────────────────
st.markdown("""
    <div class="brand-bar">
        <span class="brand-title">Big<span class="brand-accent">Mart</span> Predictor 🛒</span>
    </div>
""", unsafe_allow_html=True)

# ── Tabs Navigation ────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔮  Predict", "📊  Dashboard", "📋  History"])

with tab1:
    render_predict(model, model_columns, supabase_client)

with tab2:
    render_dashboard(supabase_client)

with tab3:
    render_history(supabase_client)
