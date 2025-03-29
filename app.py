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
    return data

mock_data = get_mock_data()

# Combined data when "All" customers and "All" data centers are selected
def get_combined_data():
    combined = {"NW Server": 0, "STG Node": 0, "DD's Count": 0, "SO Count": 0}
    for customer, dcs in mock_data.items():
        for dc, servers in dcs.items():
            for server, stats in servers.items():
                combined["NW Server"] += stats["NW Server"]
                combined["STG Node"] += stats["STG Node"]
                combined["DD's Count"] += stats["DD's Count"]
                combined["SO Count"] += stats["SO Count"]
    return combined

# Dashboard Summary based on the selected filters
if customer == "All" and data_center == "All" and backup_server == "All":
    summary = get_combined_data()
elif customer != "All" and data_center == "All" and backup_server == "All":
    summary = {
        "NW Server": sum([mock_data[customer][dc][server]["NW Server"] for dc in mock_data[customer] for server in mock_data[customer][dc]]),
        "STG Node": sum([mock_data[customer][dc][server]["STG Node"] for dc in mock_data[customer] for server in mock_data[customer][dc]]),
        "DD's Count": sum([mock_data[customer][dc][server]["DD's Count"] for dc in mock_data[customer] for server in mock_data[customer][dc]]),
        "SO Count": sum([mock_data[customer][dc][server]["SO Count"] for dc in mock_data[customer] for server in mock_data[customer][dc]]),
    }
elif customer != "All" and data_center != "All" and backup_server == "All":
    summary = {
        "NW Server": sum([mock_data[customer][data_center][server]["NW Server"] for server in mock_data[customer][data_center]]),
        "STG Node": sum([mock_data[customer][data_center][server]["STG Node"] for server in mock_data[customer][data_center]]),
        "DD's Count": sum([mock_data[customer][data_center][server]["DD's Count"] for server in mock_data[customer][data_center]]),
        "SO Count": sum([mock_data[customer][data_center][server]["SO Count"] for server in mock_data[customer][data_center]]),
    }
elif customer != "All" and data_center != "All" and backup_server != "All":
    summary = mock_data[customer].get(data_center, {}).get(backup_server, {"NW Server": 0, "STG Node": 0, "DD's Count": 0, "SO Count": 0})

# Display Summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("NW Server", summary["NW Server"])
col2.metric("STG Node", summary["STG Node"])
col3.metric("DD's Count", summary["DD's Count"])
col4.metric("SO Count", summary["SO Count"])

# Pie Charts for Backup Job Details using Plotly
col1, col2 = st.columns(2)

def plot_backup_pie_chart():
    labels = ['Successful', 'Failed', 'Running']
    sizes = [60, 25, 15]  # Mock data for jobs
    colors = ['green', 'red', 'blue']

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hoverinfo='label+percent', marker=dict(colors=colors))])
    fig.update_layout(
        title="Backup Job Status",
        template='plotly_dark',
        plot_bgcolor='#0f1117',
        paper_bgcolor='#0f1117',
        font=dict(color='white'),
    )
    return fig

with col1:
    st.markdown("### Backup Job Details")
    st.plotly_chart(plot_backup_pie_chart(), use_container_width=True, key="backup_job_pie_chart")

with col2:
    st.markdown("### NW Server Health")
    st.plotly_chart(plot_backup_pie_chart(), use_container_width=True, key="nw_server_health_pie_chart")

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
