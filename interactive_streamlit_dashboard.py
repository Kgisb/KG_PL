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

# Global Styling
st.markdown(
    """
    <style>
        /* Responsive design for mobile screens */
        @media (max-width: 768px) {
            .metric-box {
                font-size: 12px;
                padding: 15px;
            }
            .metric-title {
                font-size: 16px;
            }
            .metric-value {
                font-size: 20px;
            }
            .section-header {
                font-size: 18px;
            }
        }
        .header-banner {
            background-color: #1E90FF;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
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
            padding: 15px;
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
        .table-container {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Tabs for navigation
tabs = st.tabs(["Dashboard", "Compare"])
dashboard_tab, compare_tab = tabs

# Dashboard Tab
with dashboard_tab:
    # Header Banner
    st.markdown('<div class="header-banner">📊 Interactive Dashboard</div>', unsafe_allow_html=True)

    # Sidebar for Filters
    st.sidebar.header("Filter Options")
    ac_names = ["ALL"] + sorted(data['AC Name'].dropna().unique().tolist())
    selected_ac_name = st.sidebar.selectbox("Select AC Name", ac_names)

    time_options = ["Today", "WK 1", "WK 2", "WK 3", "WK 4", "WK 5", "MTD"]
    selected_time = st.sidebar.selectbox("Select Time Period", time_options)

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
    filtered_data = data[
        (data['Date'] >= pd.to_datetime(start_date)) & 
        (data['Date'] <= pd.to_datetime(end_date))
    ]

    # Filter data by AC Name
    if selected_ac_name != "ALL":
        filtered_data = filtered_data[filtered_data['AC Name'] == selected_ac_name]

    # Metrics
    enrl = filtered_data['Enrl'].sum() if 'Enrl' in filtered_data.columns else 0
    cash_in = filtered_data['Cash-in'].sum() if 'Cash-in' in filtered_data.columns else 0
    sgr_conversion = filtered_data['SGR Conversion'].sum() if 'SGR Conversion' in filtered_data.columns else 0

    # Display Target vs Achievement Metrics
    st.markdown('<div class="section-header">Target vs. Achievement</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="metric-box">
                <p class="metric-title">Total Enrollments</p>
                <p class="metric-value">{enrl:,.0f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-box">
                <p class="metric-title">Total SGR Conversion</p>
                <p class="metric-value">{sgr_conversion:,.0f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Display Key Performance Metrics
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Key Performance Metrics</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(
            f"""
            <div class="metric-box">
                <p class="metric-title">Total Cash-in</p>
                <p class="metric-value">{cash_in:,.0f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Compare Tab
with compare_tab:
    st.markdown('<div class="section-header">Comparison Metrics</div>', unsafe_allow_html=True)

    # Prepare data for comparison
    compare_data = filtered_data.groupby("AC Name")[["Cash-in", "SGR Conversion"]].sum().reset_index()
    compare_data = compare_data.sort_values(by="Cash-in", ascending=False).reset_index(drop=True)

    # Table with scrollable view for mobile
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    st.dataframe(compare_data, use_container_width=True)  # Enables horizontal scrolling for mobile
    st.markdown('</div>', unsafe_allow_html=True)
