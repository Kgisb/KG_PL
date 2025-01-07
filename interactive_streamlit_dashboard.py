# Display Target vs. Achievement
st.markdown('<div class="section-header">Target vs. Achievement</div>', unsafe_allow_html=True)
target_columns = {
    "Cash-in Target": "Cash-in",
    "Enrl Target": "Enrl",
    "SGR Conversion Target": "SGR Conversion"
}

col1, col2 = st.columns(2)
for idx, (target_col, achievement_col) in enumerate(target_columns.items()):
    target_value = filtered_data[target_col].sum() if target_col in numeric_columns else 0
    achievement_value = filtered_data[achievement_col].sum() if achievement_col in numeric_columns else 0
    achievement_percentage = (achievement_value / target_value * 100) if target_value > 0 else 0

    with col1 if idx % 2 == 0 else col2:
        st.markdown(
            f"""
            <div class="metric-box">
                <p class="metric-title">{target_col.split(' Target')[0]}</p>
                <p class="metric-value">{achievement_value:,.0f} / {target_value:,.0f}</p>
                <p class="metric-title">Achievement</p>
                <p class="metric-value">{achievement_percentage:.0f}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
