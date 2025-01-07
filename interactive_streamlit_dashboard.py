import pandas as pd
import streamlit as st
from datetime import datetime

# Load Google Sheet data (publicly accessible)
sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=2006560046"
data = pd.read_csv(sheet_url)

# Ensure the Date column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

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
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        .metric-box {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #ddd;
            text-align: center;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            margin: 10px 0;
        }
        .metric-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        .metric-value {
            font-size: 22px;
            font-weight: bold;
            color: #007BFF;
        }
    </style>
    <div class="header-banner">
        📊 Interactive Dashboard - January Weekly Breakdown and MTD
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")  # Adds spacing

# Sidebar for Filters
st.sidebar.header("Filter Options")
ac_names = ["ALL"] + sorted(data['AC Name'].dropna().unique().tolist())
selected_ac_name = st.sidebar.selectbox("Select AC Name", ac_names)

# Week and MTD filter options
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

# Define Target and Achievements
cash_in_target = 100000  # Example target
cash_in_achievement = filtered_data['Cash-in'].sum() if 'Cash-in' in filtered_data.columns else 0

enrollment_target = 50  # Example target
enrollment_achievement = filtered_data['Enrollment'].sum() if 'Enrollment' in filtered_data.columns else 0

sgr_target = 4  # Example target
sgr_achievement = filtered_data['SGR Conversion'].sum() if 'SGR Conversion' in filtered_data.columns else 0

# Overall Performance Display
st.markdown("### 📊 Overall Performance")

# Cash-in Performance
st.markdown(
    f"""
    <div class="metric-box">
        <p class="metric-title">Cash-in Target</p>
        <p class="metric-value">{cash_in_target}</p>
        <p class="metric-title">Cash-in Achievement</p>
        <p class="metric-value">{cash_in_achievement}</p>
        <p class="metric-title">Achievement (%)</p>
        <p class="metric-value">{(cash_in_achievement / cash_in_target) * 100 if cash_in_target > 0 else 0:.2f}%</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Enrollment Performance
st.markdown(
    f"""
    <div class="metric-box">
        <p class="metric-title">Enrollment Target</p>
        <p class="metric-value">{enrollment_target}</p>
        <p class="metric-title">Enrollment Achievement</p>
        <p class="metric-value">{enrollment_achievement}</p>
        <p class="metric-title">Achievement (%)</p>
        <p class="metric-value">{(enrollment_achievement / enrollment_target) * 100 if enrollment_target > 0 else 0:.2f}%</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# SGR Conversion Performance
st.markdown(
    f"""
    <div class="metric-box">
        <p class="metric-title">SGR Conversion Target</p>
        <p class="metric-value">{sgr_target}</p>
        <p class="metric-title">SGR Conversion Achievement</p>
        <p class="metric-value">{sgr_achievement}</p>
        <p class="metric-title">Achievement (%)</p>
        <p class="metric-value">{(sgr_achievement / sgr_target) * 100 if sgr_target > 0 else 0:.2f}%</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Filtered Data with Expander
with st.expander("🔍 View Filtered Data"):
    st.markdown("### Filtered Data")
    if filtered_data.empty:
        st.info("No data available for the selected filters.")
    else:
        st.dataframe(filtered_data, use_container_width=True)
