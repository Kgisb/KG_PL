import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

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
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #ddd;
            text-align: center;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
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

# Function to create pie chart
def create_pie_chart(target, achievement, title):
    labels = ["Achieved", "Remaining"]
    values = [achievement, max(0, target - achievement)]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
    fig.update_layout(
        title=title,
        annotations=[dict(text=f"{achievement/target:.0%}", showarrow=False, font_size=20)],
        showlegend=True,
    )
    return fig

# Overall Performance Display
st.markdown("### 📊 Overall Performance")

# Cash-in Performance
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown(
        f"""
        <div class="metric-box">
            <p class="metric-title">Cash-in Target</p>
            <p class="metric-value">{cash_in_target}</p>
            <p class="metric-title">Cash-in Achievement</p>
            <p class="metric-value">{cash_in_achievement}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.plotly_chart(create_pie_chart(cash_in_target, cash_in_achievement, "Cash-in Achievement"), use_container_width=True)

# Enrollment Performance
col3, col4 = st.columns([1, 1])
with col3:
    st.markdown(
        f"""
        <div class="metric-box">
            <p class="metric-title">Enrollment Target</p>
            <p class="metric-value">{enrollment_target}</p>
            <p class="metric-title">Enrollment Achievement</p>
            <p class="metric-value">{enrollment_achievement}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col4:
    st.plotly_chart(create_pie_chart(enrollment_target, enrollment_achievement, "Enrollment Achievement"), use_container_width=True)

# SGR Conversion Performance
col5, col6 = st.columns([1, 1])
with col5:
    st.markdown(
        f"""
        <div class="metric-box">
            <p class="metric-title">SGR Conversion Target</p>
            <p class="metric-value">{sgr_target}</p>
            <p class="metric-title">SGR Conversion Achievement</p>
            <p class="metric-value">{sgr_achievement}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col6:
    st.plotly_chart(create_pie_chart(sgr_target, sgr_achievement, "SGR Conversion Achievement"), use_container_width=True)

# Filtered Data with Expander
with st.expander("🔍 View Filtered Data"):
    st.markdown("### Filtered Data")
    if filtered_data.empty:
        st.info("No data available for the selected filters.")
    else:
        st.dataframe(filtered_data, use_container_width=True)
