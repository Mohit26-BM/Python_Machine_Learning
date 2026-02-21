import streamlit as st
from utils.database import fetch_predictions

def render(supabase_client):

    st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="page-title">Prediction <span class="accent">History</span></div>
        <div class="page-subtitle">Full log of every prediction — browse, filter, and export</div>
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
            '<p style="font-family:\'Inter\',sans-serif; font-size:0.75rem; font-weight:700;'
            'letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);'
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
            f'<p style="font-family:\'Inter\',sans-serif; font-size:0.75rem; font-weight:700;'
            f'letter-spacing:0.12em; text-transform:uppercase; color:rgba(255,255,255,0.32);'
            f'margin:16px 0 10px 0;">Showing {len(filtered_df)} of {len(log_df)} records</p>',
            unsafe_allow_html=True,
        )

        st.dataframe(
            filtered_df.style
                .highlight_max(subset=["Predicted_Sales"], color="rgba(124,106,247,0.18)")
                .highlight_min(subset=["Predicted_Sales"], color="rgba(244,114,182,0.14)"),
            use_container_width=True,
            height=480,
        )

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Filtered CSV",
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
