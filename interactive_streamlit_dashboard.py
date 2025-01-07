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
    page_title="Interactive Dashboard with Weekly Tabs",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Interactive Dashboard with Weekly Tabs")
st.markdown(
    '''
    Explore the data with today's data, weekly breakdowns, and Month-to-Date (MTD).
    '''
)

# Define week ranges for January
def get_weekly_data(data):
    january = data[data['Date'].dt.month == 1]  # Filter data for January
    week_ranges = [
        ("WK 1", "2025-01-01", "2025-01-06"),
        ("WK 2", "2025-01-07", "2025-01-13"),
        ("WK 3", "2025-01-14", "2025-01-20"),
        ("WK 4", "2025-01-21", "2025-01-27"),
        ("WK 5", "2025-01-28", "2025-01-31"),
    ]

    weekly_data = []
    for week_name, start_date, end_date in week_ranges:
        week_data = january[
            (january['Date'] >= pd.to_datetime(start_date)) &
            (january['Date'] <= pd.to_datetime(end_date))
        ]
        weekly_data.append((week_name, start_date, end_date, week_data))
    return weekly_data

weekly_data = get_weekly_data(data)

# Get today's data
today = datetime.now().date()
today_data = data[data['Date'] == pd.to_datetime(today)]

# Get MTD (Month-to-Date) data
mtd_data = data[
    (data['Date'].dt.month == 1) &
    (data['Date'] <= pd.to_datetime(today))
]

# Display tabs for Today, Weekly, and MTD
tabs = ["Today"] + [f"Week {i+1}" for i in range(len(weekly_data))] + ["MTD"]
tab_objects = st.tabs(tabs)

# Today tab
with tab_objects[0]:
    st.subheader(f"Today's Data: {today.strftime('%Y-%m-%d')}")
    st.dataframe(today_data, use_container_width=True)

# Weekly tabs
for i, (week_name, start_date, end_date, week_data) in enumerate(weekly_data):
    with tab_objects[i + 1]:
        st.subheader(f"{week_name}: {start_date} to {end_date}")
        st.dataframe(week_data, use_container_width=True)

# MTD tab
with tab_objects[-1]:
    st.subheader("Month-to-Date (MTD) Data")
    st.dataframe(mtd_data, use_container_width=True)

# Download filtered data
st.sidebar.markdown("### Download Filtered Data")
csv = data.to_csv(index=False)
st.sidebar.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)
