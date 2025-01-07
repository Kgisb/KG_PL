import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

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
    """
    Explore the data with Month-to-Date (MTD) and weekly breakdowns.
    Use filters to refine results and download the filtered data.
    """
)

# Sidebar filters
st.sidebar.header("Filter Options")
ac_name = st.sidebar.selectbox("Select AC Name:", ["All"] + data['AC Name'].unique().tolist())
start_date = st.sidebar.date_input("Start Date:")
end_date = st.sidebar.date_input("End Date:")

# Filter data function
def filter_and_sort_data(ac_name="All", start_date=None, end_date=None):
    filtered_data = data.copy()

    # Filter by AC Name if not "All"
    if ac_name != "All":
        filtered_data = filtered_data[filtered_data['AC Name'] == ac_name]

    # Filter by date range if specified
    if start_date and end_date:
        filtered_data = filtered_data[
            (filtered_data['Date'] >= pd.to_datetime(start_date)) &
            (filtered_data['Date'] <= pd.to_datetime(end_date))
        ]
    
    # Sort by Date
    filtered_data = filtered_data.sort_values(by="Date")
    
    return filtered_data

# Filter data
filtered_data = filter_and_sort_data(ac_name, start_date, end_date)

# Function to split data into MTD and weekly buckets
def split_into_weeks(data):
    current_month = datetime.now().month
    mtd_data = data[data['Date'].dt.month == current_month]

    # Define week ranges
    start_of_month = mtd_data['Date'].min()
    week_ranges = [
        (start_of_month, start_of_month + timedelta(days=5)),
        (start_of_month + timedelta(days=6), start_of_month + timedelta(days=12)),
        (start_of_month + timedelta(days=13), start_of_month + timedelta(days=19)),
        (start_of_month + timedelta(days=20), start_of_month + timedelta(days=26)),
        (start_of_month + timedelta(days=27), mtd_data['Date'].max())
    ]

    weeks = []
    for start, end in week_ranges:
        week_data = mtd_data[(mtd_data['Date'] >= start) & (mtd_data['Date'] <= end)]
        weeks.append((start, end, week_data))
    return mtd_data, weeks

mtd_data, weekly_data = split_into_weeks(filtered_data)

# Display tabs for MTD and weekly data
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["MTD", "Week 1", "Week 2", "Week 3", "Week 4", "Week 5"])

# MTD tab
with tab1:
    st.subheader("Month-to-Date (MTD) Data")
    st.dataframe(mtd_data, use_container_width=True)

# Weekly tabs
for i, (start, end, week_data) in enumerate(weekly_data):
    with [tab2, tab3, tab4, tab5, tab6][i]:
        st.subheader(f"Week {i + 1}: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
        st.dataframe(week_data, use_container_width=True)

# Download filtered data
st.sidebar.markdown("### Download Filtered Data")
csv = filtered_data.to_csv(index=False)
st.sidebar.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)
