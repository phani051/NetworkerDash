import streamlit as st
import pandas as pd
import time
import os
import urllib.request
import plotly.graph_objects as go
import numpy as np

# Streamlit App Configuration
st.set_page_config(page_title="Networker Dashboard", layout="wide")

# Ensure DXC logo is downloaded
logo_url = "https://dxc.com/content/dam/dxc/projects/dxc-com/us/images/about-us/newsroom/logos-for-media/vertical/DXC%20Logo_Purple+Black%20RGB.png"
logo_path = "dxc_logo.png"
if not os.path.exists(logo_path):
    urllib.request.urlretrieve(logo_url, logo_path)

# Sidebar with Drilldown Filters
st.sidebar.image(logo_path, use_container_width=False, width=100)
st.sidebar.title("Drilldown Filters")
customers = ["All", "Customer 1", "Customer 2", "Customer 3"]
customer = st.sidebar.selectbox("Customer", customers)

# Data Centers per Customer
data_centers = {
    "All": ["DC 1", "DC 2", "DC 3"],
    "Customer 1": ["DC 1", "DC 2"],
    "Customer 2": ["DC 3"],
    "Customer 3": ["DC 2", "DC 3"]
}

# If a specific customer is selected, we provide options for "All DC" or the specific data centers
if customer != "All":
    data_center = st.sidebar.selectbox("Data Centers", ["All"] + data_centers[customer])
else:
    data_center = st.sidebar.selectbox("Data Centers", ["All"] + data_centers["All"])

# Backup Servers per Data Center (Hierarchy Data)
backup_servers = {
    "DC 1": ["Server A", "Server B"],
    "DC 2": ["Server B", "Server C"],
    "DC 3": ["Server A", "Server C"],
}

# If a specific data center is selected, we provide options for "All Backup Servers" or the specific backup servers
if data_center != "All":
    backup_server = st.sidebar.selectbox("Backup Server", ["All"] + backup_servers.get(data_center, []))
else:
    backup_server = st.sidebar.selectbox("Backup Server", ["All"] + [server for servers in backup_servers.values() for server in servers])

refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 60, 30)

# Dashboard Title
col1, col2 = st.columns([1, 5])
col2.title("NETWORKER DASHBOARD")

# Mock Data: Hierarchical Data for NW Server, STG Node, DD's Count, and SO Count
def get_mock_data():
    data = {
        "Customer 1": {
            "DC 1": {"Server A": {"Successful": 60, "Failed": 25, "Running": 15},
                     "Server B": {"Successful": 50, "Failed": 30, "Running": 20}},
            "DC 2": {"Server A": {"Successful": 40, "Failed": 20, "Running": 10},
                     "Server B": {"Successful": 35, "Failed": 25, "Running": 15}},
        },
    }
    return data

mock_data = get_mock_data()

# Line Charts for Backup Job Details using Plotly
col1, col2 = st.columns(2)

def plot_backup_line_chart():
    time_data = pd.date_range(start="2025-03-01", periods=10, freq='D')
    successful = np.random.randint(50, 80, size=10)
    failed = np.random.randint(10, 30, size=10)
    running = np.random.randint(5, 20, size=10)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_data, y=successful, mode='lines+markers', name='Successful', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=time_data, y=failed, mode='lines+markers', name='Failed', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=time_data, y=running, mode='lines+markers', name='Running', line=dict(color='blue')))
    
    fig.update_layout(
        title="Backup Job Status",
        xaxis_title='Time',
        yaxis_title='Count',
        template='plotly_dark',
        plot_bgcolor='#0f1117',
        paper_bgcolor='#0f1117',
        font=dict(color='white')
    )
    return fig

with col1:
    st.markdown("### Backup Job Details")
    st.plotly_chart(plot_backup_line_chart(), use_container_width=True, key="backup_job_line_chart")

with col2:
    st.markdown("### NW Server Health")
    st.plotly_chart(plot_backup_line_chart(), use_container_width=True, key="nw_server_health_line_chart")

# Prediction & Utilization Charts with Plotly (modified)
st.subheader("Predictions & Utilization")
col1, col2 = st.columns(2, gap="large")

# Global Definition for Time Data
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

# Utilization Prediction Chart 1
backup_size = np.random.randint(50, 200, size=10)
with col1:
    st.plotly_chart(plot_prediction_chart("BSR Prediction", time_data, backup_size, 'blue', 'solid'))

# Disk Space Prediction Chart
disk_space = np.random.randint(500, 1000, size=10)
with col1:
    st.plotly_chart(plot_prediction_chart("FETB Prediction", time_data, disk_space, 'red', 'dash'))

# Additional Prediction Chart 1
backup_throughput = np.random.randint(100, 300, size=10)
with col2:
    st.plotly_chart(plot_prediction_chart("SO Utilization Prediction", time_data, backup_throughput, 'green', 'dot'))

# Additional Prediction Chart 2
recovery_time = np.random.randint(10, 50, size=10)
with col2:
    st.plotly_chart(plot_prediction_chart("DD Utilization Prediction", time_data, recovery_time, 'orange', 'dashdot'))

# Auto-refresh
time.sleep(refresh_interval)