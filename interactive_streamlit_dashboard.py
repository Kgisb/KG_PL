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

# Calculate Overall Performance
def calculate_overall_performance(data):
    if data.empty:
        return {"Total Entries": 0, "Sum of Values": 0}
    summary = {
        "Total Entries": len(data),
        "Sum of Values": data.select_dtypes(include=['number']).sum(numeric_only=True).to_dict()
    }
    return summary

overall_performance = calculate_overall_performance(filtered_data)

# Display Overall Performance
st.markdown("### 📊 Overall Performance")
st.write(f"**Selected AC Name**: {selected_ac_name}")
st.write(f"**Selected Time Period**: {selected_time} ({start_date} to {end_date})")
st.write(f"**Total Entries**: {overall_performance['Total Entries']}")

if overall_performance['Total Entries'] > 0:
    st.markdown("#### Sum of Numerical Columns:")
    st.json(overall_performance["Sum of Values"])
else:
    st.info("No data available for the selected filters.")

# Display Filtered Data in a Tab
tab1, tab2 = st.tabs(["Filtered Data", "Detailed View"])

with tab1:
    st.markdown("### Filtered Data")
    if filtered_data.empty:
        st.info("No data available for the selected filters.")
    else:
        st.dataframe(filtered_data, use_container_width=True)

with tab2:
    st.markdown("### Detailed View")
    if filtered_data.empty:
        st.info("No data available for the selected filters.")
    else:
        st.dataframe(filtered_data.describe(include='all'), use_container_width=True)
