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

# Navigation
st.sidebar.subheader("📌 Navigation")
page = st.sidebar.radio("Select a Page", ["Dashboard", "Predictions"])

# Dashboard Page
if page == "Dashboard":
    st.title("📊 NETWORKER DASHBOARD")
    st.subheader(f"Overview for {customer} - {data_center} - {backup_server}")

    # Initialize counts
    server_count = 0
    storage_node_count = 0
    so_count = 0
    dd_count = 0

    # Retrieve counts based on drilldown selection
    if customer == "All":
        # Aggregate all customer data
        for cust_data in data.values():
            for dc_data in cust_data.values():
                for server_data in dc_data.values():
                    server_count += 1
                    storage_node_count += server_data.get("STG Node", 0)
                    so_count += server_data.get("SO Count", 0)
                    dd_count += server_data.get("DD's Count", 0)
    else:
        selected_data = data.get(customer, {})

        if data_center == "All":
            # Aggregate data for the selected customer
            for dc_data in selected_data.values():
                for server_data in dc_data.values():
                    server_count += 1
                    storage_node_count += server_data.get("STG Node", 0)
                    so_count += server_data.get("SO Count", 0)
                    dd_count += server_data.get("DD's Count", 0)
        else:
            selected_dc_data = selected_data.get(data_center, {})

            if backup_server == "All":
                # Aggregate data for the selected customer & data center
                for server_data in selected_dc_data.values():
                    server_count += 1
                    storage_node_count += server_data.get("STG Node", 0)
                    so_count += server_data.get("SO Count", 0)
                    dd_count += server_data.get("DD's Count", 0)
            else:
                # Direct selection
                selected_server_data = selected_dc_data.get(backup_server, {})
                server_count = 1 if selected_server_data else 0
                storage_node_count = selected_server_data.get("STG Node", 0)
                so_count = selected_server_data.get("SO Count", 0)
                dd_count = selected_server_data.get("DD's Count", 0)

    # Mock data if counts are zero
    if server_count == 0:
        server_count = np.random.randint(1, 5)
    if storage_node_count == 0:
        storage_node_count = np.random.randint(1, 5)
    if so_count == 0:
        so_count = np.random.randint(1, 10)
    if dd_count == 0:
        dd_count = np.random.randint(5, 15)

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Server Count", value=server_count)
    col2.metric(label="Storage Node Count", value=storage_node_count)
    col3.metric(label="SO Count", value=so_count)
    col4.metric(label="DD Count", value=dd_count)

    # Add Line Graphs for Dashboard (Only Backup Success Rate)
    time_data = pd.date_range(start="2025-03-01", periods=10, freq='D')
    success_rate = np.random.uniform(95, 100, size=10)

    def plot_line_chart(title, x_data, y_data, color):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', line=dict(color=color), name=title))
        fig.update_layout(title=title, xaxis_title='Time', yaxis_title='%', plot_bgcolor='#0f1117', paper_bgcolor='#0f1117', font=dict(color='white'))
        return fig
    
    # Only one graph now (Backup Success Rate)
    st.plotly_chart(plot_line_chart("Backup Success Rate", time_data, success_rate, 'green'))

# Predictions Page
elif page == "Predictions":
    st.title("📈 Predictions & Utilization")
    time_data = pd.date_range(start="2025-03-01", periods=10, freq='D')

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

    col1, col2 = st.columns(2, gap="large")
    backup_size = np.random.randint(50, 200, size=10)
    with col1:
        st.plotly_chart(plot_prediction_chart("BSR Prediction", time_data, backup_size, 'blue', 'solid'))

    disk_space = np.random.randint(500, 1000, size=10)
    with col1:
        st.plotly_chart(plot_prediction_chart("FETB Prediction", time_data, disk_space, 'red', 'dash'))

    backup_throughput = np.random.randint(100, 300, size=10)
    with col2:
        st.plotly_chart(plot_prediction_chart("SO Utilization Prediction", time_data, backup_throughput, 'green', 'dot'))

    recovery_time = np.random.randint(10, 50, size=10)
    with col2:
        st.plotly_chart(plot_prediction_chart("DD Utilization Prediction", time_data, recovery_time, 'orange', 'dashdot'))