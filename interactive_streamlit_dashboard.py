import pandas as pd
import streamlit as st
from datetime import datetime

# Load Google Sheet data (publicly accessible)
sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=2006560046"
data = pd.read_csv(sheet_url)

# Ensure the Date column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Clean numeric columns (remove commas and convert to numeric types)
for col in data.columns:
    if data[col].dtype == 'object':  # Check for non-numeric columns
        try:
            data[col] = data[col].str.replace(',', '').astype(float)
        except ValueError:
            continue  # Skip columns that cannot be converted

# Streamlit app configuration
st.set_page_config(
    page_title="Interactive Dashboard",
    page_icon="📊",
    layout="wide"
)

# Header Banner
st.markdown(
    """
    <style>
        .header-banner {
            background-color: #1E90FF;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .section-header {
            color: #333333;
            font-size: 22px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .metric-box {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #ddd;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin: 10px 0;
        }
        .metric-title {
            font-size: 18px;
            font-weight: bold;
            color: #555555;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #007BFF;
        }
        .divider {
            height: 2px;
            background-color: #e0e0e0;
            margin: 20px 0;
        }
    </style>
    <div class="header-banner">
        📊 Interactive Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for Filters
st.sidebar.header("Filter Options")
ac_names = ["ALL"] + sorted(data['AC Name'].dropna().unique().tolist())
selected_ac_name = st.sidebar.selectbox("Select AC Name", ac_names)

time_options = ["Today", "WK 1", "WK 2", "WK 3", "WK 4", "WK 5", "MTD"]
selected_time = st.sidebar.selectbox("Select Time Period", time_options)

# Filter data by AC Name
if selected_ac_name != "ALL":
    filtered_data = data[data['AC Name'] == selected_ac_name]
else:
    filtered_data = data

# Define time ranges
time_ranges = {
    "Today": (datetime.now().date(), datetime.now().date()),
    "WK 1": ("2025-01-01", "2025-01-06"),
    "WK 2": ("2025-01-07", "2025-01-13"),
    "WK 3": ("2025-01-14", "2025-01-20"),
    "WK 4": ("2025-01-21", "2025-01-27"),
    "WK 5": ("2025-01-28", "2025-01-31"),
    "MTD": ("2025-01-01", datetime.now().date()),
}

start_date, end_date = time_ranges[selected_time]
filtered_data = filtered_data[
    (filtered_data['Date'] >= pd.to_datetime(start_date)) &
    (filtered_data['Date'] <= pd.to_datetime(end_date))
]

# Calculate metrics
enrl = filtered_data['Enrl'].sum() if 'Enrl' in filtered_data.columns else 0
overall_leads = filtered_data['Overall Leads'].sum() if 'Overall Leads' in filtered_data.columns else 0
sgr_conversion = filtered_data['SGR Conversion'].sum() if 'SGR Conversion' in filtered_data.columns else 0
sgr_leads = filtered_data['SGR Leads'].sum() if 'SGR Leads' in filtered_data.columns else 0

# MLMC% and L2P%
mlmc = (enrl / overall_leads * 100) if overall_leads > 0 else 0
l2p = (
    (enrl - sgr_conversion) / (overall_leads - sgr_leads) * 100
    if (overall_leads - sgr_leads) > 0
    else 0
)

# TS and TD
ts = filtered_data['TS'].sum() if 'TS' in filtered_data.columns else 0
td = filtered_data['TD'].sum() if 'TD' in filtered_data.columns else 0

# Display Target vs. Achievement
st.markdown('<div class="section-header">Target vs. Achievement</div>', unsafe_allow_html=True)
target_columns = {
    "Cash-in Target": "Cash-in",
    "Enrl Target": "Enrl",
    "SGR Conversion Target": "SGR Conversion"
}

col1, col2 = st.columns(2)
for idx, (target_col, achievement_col) in enumerate(target_columns.items()):
    target_value = filtered_data[target_col].sum() if target_col in filtered_data.columns else 0
    achievement_value = filtered_data[achievement_col].sum() if achievement_col in filtered_data.columns else 0
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

# Display Key Metrics
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">Key Performance Metrics</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown(
        f"""
        <div class="metric-box">
            <p class="metric-title">MLMC%</p>
            <p class="metric-value">{int(mlmc)}%</p>
        </div>
        <div class="metric-box">
            <p class="metric-title">TS</p>
            <p class="metric-value">{ts:,.0f}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f"""
        <div class="metric-box">
            <p class="metric-title">L2P%</p>
            <p class="metric-value">{int(l2p)}%</p>
        </div>
        <div class="metric-box">
            <p class="metric-title">TD</p>
            <p class="metric-value">{td:,.0f}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Filtered Data in Expander
with st.expander("🔍 View Filtered Data"):
    st.markdown("### Filtered Data")
    if filtered_data.empty:
        st.info("No data available for the selected filters.")
    else:
        # Apply formatting dynamically to numeric columns
        styled_df = filtered_data.copy()
        for col in styled_df.select_dtypes(include=['float', 'int']).columns:
            styled_df[col] = styled_df[col].apply(lambda x: f"{x:,.0f}")
        
        # Display the dataframe with comma formatting
        st.dataframe(styled_df, use_container_width=True)
