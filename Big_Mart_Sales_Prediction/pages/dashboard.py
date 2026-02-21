import streamlit as st
from utils.database import fetch_predictions

def render(supabase_client):

    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="page-title">Prediction <span class="accent">Dashboard</span></div>
        <div class="page-subtitle">Visual analytics of all recorded predictions</div>
        """,
        unsafe_allow_html=True,
    )

    try:
        log_df = fetch_predictions(supabase_client)

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
                '<p style="font-family:\'Inter\',sans-serif; font-size:0.75rem; font-weight:700;'
                'letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);'
                'margin:0 0 10px 0;">Predicted Sales Over Time</p>',
                unsafe_allow_html=True,
            )
            ts = log_df[["Predicted_Sales"]].reset_index()
            ts.columns = ["Prediction #", "Predicted Sales (₹)"]
            st.line_chart(ts.set_index("Prediction #"), color="#7c6af7")

        with r1c2:
            st.markdown(
                '<p style="font-family:\'Inter\',sans-serif; font-size:0.75rem; font-weight:700;'
                'letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);'
                'margin:0 0 10px 0;">Avg Sales by Outlet Type</p>',
                unsafe_allow_html=True,
            )
            ot = log_df.groupby("Outlet_Type")["Predicted_Sales"].mean().reset_index()
            ot.columns = ["Outlet Type", "Avg Sales (₹)"]
            st.bar_chart(ot.set_index("Outlet Type"), color="#7c6af7")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.markdown(
                '<p style="font-family:\'Inter\',sans-serif; font-size:0.75rem; font-weight:700;'
                'letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);'
                'margin:0 0 10px 0;">Avg Sales by Item Type</p>',
                unsafe_allow_html=True,
            )
            it = log_df.groupby("Item_Type")["Predicted_Sales"].mean().reset_index()
            it.columns = ["Item Type", "Avg Sales (₹)"]
            st.bar_chart(it.set_index("Item Type"), color="#a78bfa")

        with r2c2:
            st.markdown(
                '<p style="font-family:\'Inter\',sans-serif; font-size:0.75rem; font-weight:700;'
                'letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);'
                'margin:0 0 10px 0;">Avg Sales by Location Tier</p>',
                unsafe_allow_html=True,
            )
            lt = log_df.groupby("Outlet_Location_Type")["Predicted_Sales"].mean().reset_index()
            lt.columns = ["Location Tier", "Avg Sales (₹)"]
            st.bar_chart(lt.set_index("Location Tier"), color="#6ee7b7")

        r3c1, r3c2 = st.columns(2)
        with r3c1:
            if len(log_df) >= 3:
                st.markdown(
                    '<p style="font-family:\'Inter\',sans-serif; font-size:0.75rem; font-weight:700;'
                    'letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);'
                    'margin:0 0 10px 0;">Item MRP vs Predicted Sales</p>',
                    unsafe_allow_html=True,
                )
                sc = log_df[["Item_MRP", "Predicted_Sales"]].copy()
                sc.columns = ["Item MRP (₹)", "Predicted Sales (₹)"]
                st.scatter_chart(sc, x="Item MRP (₹)", y="Predicted Sales (₹)", color="#7c6af7")

        with r3c2:
            st.markdown(
                '<p style="font-family:\'Inter\',sans-serif; font-size:0.75rem; font-weight:700;'
                'letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);'
                'margin:0 0 10px 0;">Avg Sales by Fat Content</p>',
                unsafe_allow_html=True,
            )
            fc = log_df.groupby("Item_Fat_Content")["Predicted_Sales"].mean().reset_index()
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
