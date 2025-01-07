import pandas as pd
import streamlit as st

# Load Google Sheet data (publicly accessible)
sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=2006560046"
data = pd.read_csv(sheet_url)

# Ensure the Date column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Streamlit app
st.set_page_config(
    page_title="Interactive Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Interactive Data Dashboard")
st.markdown(
    """
    Use this dashboard to filter, explore, and analyze data interactively. 
    You can filter by AC Name, date range, and download the filtered results.
    """
)

# Sidebar for filters
st.sidebar.header("Filter Options")
ac_name = st.sidebar.selectbox("Select AC Name:", ["All"] + data['AC Name'].unique().tolist())
start_date = st.sidebar.date_input("Start Date:")
end_date = st.sidebar.date_input("End Date:")

# Filter and sort data
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

# Display summary statistics
st.subheader("Data Summary")
st.metric("Total Entries", len(filtered_data))
st.metric("Unique AC Names", filtered_data['AC Name'].nunique())

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_data, use_container_width=True)

# Option to download filtered data
csv = filtered_data.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)

# Footer with feedback option
st.sidebar.markdown("### Feedback")
st.sidebar.text_area("What do you think about this dashboard?", placeholder="Write your feedback here...")
st.sidebar.button("Submit Feedback")
