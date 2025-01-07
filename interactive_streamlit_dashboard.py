
import pandas as pd
import streamlit as st

# Load Google Sheet data (publicly accessible)
sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=2006560046"
data = pd.read_csv(sheet_url)

# Ensure the Date column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Streamlit app
st.title("Interactive Dashboard")
st.write("Filter and explore the data interactively.")

# Filter widgets
ac_name = st.selectbox("Select AC Name:", ["All"] + data['AC Name'].unique().tolist())
start_date = st.date_input("Start Date:")
end_date = st.date_input("End Date:")

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

# Filter and display data
filtered_data = filter_and_sort_data(ac_name, start_date, end_date)
st.write("Filtered Data:")
st.dataframe(filtered_data)

# Option to download filtered data
csv = filtered_data.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)
