import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Networker Dashboard", layout="wide")

# Mock Data
data_centers = {
    "All": ["DC 1", "DC 2", "DC 3"],
    "Customer 1": ["DC 1", "DC 2"],
    "Customer 2": ["DC 3"],
    "Customer 3": ["DC 2", "DC 3"]
}

backup_servers = {
    "DC 1": ["Server A", "Server B"],
    "DC 2": ["Server B", "Server C"],
    "DC 3": ["Server A", "Server C"],
}

data = {
    "Customer 1": {
        "DC 1": {"Server A": {"NW Server": 5, "STG Node": 3, "DD's Count": 10, "SO Count": 8},
                 "Server B": {"NW Server": 4, "STG Node": 2, "DD's Count": 12, "SO Count": 6}},
        "DC 2": {"Server A": {"NW Server": 3, "STG Node": 1, "DD's Count": 8, "SO Count": 5},
                 "Server B": {"NW Server": 2, "STG Node": 1, "DD's Count": 6, "SO Count": 4}},
    },
    "Customer 2": {
        "DC 3": {"Server A": {"NW Server": 6, "STG Node": 4, "DD's Count": 14, "SO Count": 7},
                 "Server C": {"NW Server": 5, "STG Node": 3, "DD's Count": 11, "SO Count": 6}},
    },
    "Customer 3": {
        "DC 2": {"Server B": {"NW Server": 3, "STG Node": 2, "DD's Count": 8, "SO Count": 5},
                 "Server C": {"NW Server": 4, "STG Node": 3, "DD's Count": 10, "SO Count": 6}},
        "DC 3": {"Server A": {"NW Server": 4, "STG Node": 3, "DD's Count": 9, "SO Count": 5},
                 "Server C": {"NW Server": 2, "STG Node": 1, "DD's Count": 7, "SO Count": 4}},
    }
}

# Sidebar Filters
st.sidebar.title("🔍 Drill-down Selection")
customers = ["All"] + list(data.keys())
customer = st.sidebar.selectbox("Select Customer", customers)

data_center_options = data_centers["All"] if customer == "All" else data_centers[customer]
data_center = st.sidebar.selectbox("Select Data Center", ["All"] + data_center_options)

backup_server_options = (
    list(set(server for dc in backup_servers.values() for server in dc))
    if data_center == "All" else backup_servers.get(data_center, [])
)
backup_server = st.sidebar.selectbox("Select Backup Server", ["All"] + backup_server_options)

# Sidebar Navigation
selected_page = st.sidebar.radio("Select Page", ["Dashboard", "Predictions"])

# Dashboard Page
if selected_page == "Dashboard":
    st.title("📊 NETWORKER DASHBOARD")
    st.subheader(f"Overview for {customer} - {data_center} - {backup_server}")

    # Initialize counts
    server_count, storage_node_count, so_count, dd_count = 0, 0, 0, 0

    # Retrieve counts based on drilldown selection
    if customer == "All":
        for cust_data in data.values():
            for dc_data in cust_data.values():
                for server_data in dc_data.values():
                    server_count += 1
                    storage_node_count += server_data.get("STG Node", 0)
                    so_count += server_data.get("SO Count", 0)
                    dd_count += server_data.get("DD's Count", 0)
    else:
        selected_data = data.get(customer, {})
        for dc, dc_data in selected_data.items():
            if data_center in ["All", dc]:
                for server, server_data in dc_data.items():
                    if backup_server in ["All", server]:
                        server_count += 1
                        storage_node_count += server_data.get("STG Node", 0)
                        so_count += server_data.get("SO Count", 0)
                        dd_count += server_data.get("DD's Count", 0)

    # Styled metric cards
    def styled_metric_card(title, value, description, color1, color2):
        st.markdown(
            f"""
            <div style="border-radius: 10px; padding: 20px; text-align: center; 
                        background: linear-gradient(to left, rgba{color1}, rgba{color2}); 
                        opacity: 1;">  <!-- Ensure text remains fully opaque -->
                <h4 style="margin: 0; color: white;">{title}</h4>
                <h2 style="margin: 5px 0; color: white;">{value}</h2>
                <p style="margin: 0; color: #ddd;">{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: styled_metric_card("Server Count", server_count, "Total servers available", "(31, 41, 55, 0.3)", "(75, 85, 99, 0.3)")
    with col2: styled_metric_card("Storage Node Count", storage_node_count, "Total storage nodes", "(20, 83, 45, 0.3)", "(34, 139, 34, 0.3)")
    with col3: styled_metric_card("SO Count", so_count, "Total service objects", "(59, 7, 100, 0.3)", "(106, 13, 173, 0.3)")
    with col4: styled_metric_card("DD Count", dd_count, "Total data domains", "(127, 29, 29, 0.3)", "(255, 69, 0, 0.3)")


    # Add spacing
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)


    # Time selection slider
    time_data = pd.date_range(start="2025-03-01", periods=10, freq='D')
    success_rate = np.random.uniform(95, 100, size=10)
    
    start_date, end_date = st.slider(
        "Select Date Range:", 
        min_value=time_data.min().to_pydatetime(), 
        max_value=time_data.max().to_pydatetime(), 
        value=(time_data.min().to_pydatetime(), time_data.max().to_pydatetime()), 
        format="YYYY-MM-DD"
    )
    
    # Filter data based on selected range
    mask = (time_data >= start_date) & (time_data <= end_date)
    filtered_time_data = time_data[mask]
    filtered_success_rate = success_rate[mask]
    
    def plot_line_chart(title, x_data, y_data, color):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', line=dict(color=color), name=title))
        fig.update_layout(title=title, xaxis_title='Time', yaxis_title='%', plot_bgcolor='#0f1117', paper_bgcolor='#0f1117', font=dict(color='white'))
        return fig
    
    # Display graph based on selected range
    st.plotly_chart(plot_line_chart("Backup Success Rate", filtered_time_data, filtered_success_rate, 'green'))

# Predictions Page
elif selected_page == "Predictions":
    st.title("📈 Predictions & Utilization")
    time_data = pd.date_range(start="2025-03-01", periods=10, freq='D')

    # Generate Time Data and Random Predictions
    time_data = pd.date_range(start="2025-03-01", periods=10, freq='D')
    backup_size = np.random.randint(50, 200, size=10)
    disk_space = np.random.randint(500, 1000, size=10)
    backup_throughput = np.random.randint(100, 300, size=10)
    recovery_time = np.random.randint(10, 50, size=10)

    # Date Selection Slider
    start_date, end_date = st.slider(
        "Select Date Range:", 
        min_value=time_data.min().to_pydatetime(), 
        max_value=time_data.max().to_pydatetime(), 
        value=(time_data.min().to_pydatetime(), time_data.max().to_pydatetime()), 
        format="YYYY-MM-DD"
    )

    # Filter Data Based on Selected Date Range
    mask = (time_data >= start_date) & (time_data <= end_date)
    filtered_time_data = time_data[mask]
    filtered_backup_size = backup_size[mask]
    filtered_disk_space = disk_space[mask]
    filtered_backup_throughput = backup_throughput[mask]
    filtered_recovery_time = recovery_time[mask]

    # Function to Plot Graphs
    def plot_prediction_chart(title, x_data, y_data, color, linestyle):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines+markers',
            line=dict(color=color, dash=linestyle),
            marker=dict(size=8),
            name=title
        ))
        fig.update_layout(
            title=title,
            xaxis_title='Time',
            yaxis_title='Backup Size (GB)',
            plot_bgcolor='#0f1117',
            paper_bgcolor='#0f1117',
            font=dict(color='white')
        )
        return fig

    # Display One Graph Per Line with Filtered Data
    #st.plotly_chart(plot_prediction_chart("BSR Prediction", filtered_time_data, filtered_backup_size, 'blue', 'solid'))
    st.plotly_chart(plot_prediction_chart("FETB Prediction", filtered_time_data, filtered_disk_space, 'red', 'dash'))
    st.plotly_chart(plot_prediction_chart("SO Utilization Prediction", filtered_time_data, filtered_backup_throughput, 'green', 'dot'))
    st.plotly_chart(plot_prediction_chart("DD Utilization Prediction", filtered_time_data, filtered_recovery_time, 'orange', 'dashdot'))