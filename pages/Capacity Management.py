import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Predictions & Utilization", layout="wide")

st.title("📈 Predictions & Utilization")

# Global Time Data for Predictions
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

# Layout for Predictions
col1, col2 = st.columns(2, gap="large")

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
