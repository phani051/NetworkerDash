import streamlit as st

def add_header():
    st.markdown(
        """
        <h1 style='text-align: center; color: #0078D4;'>Networker Dashboard</h1>
        <hr style="border:1px solid #0078D4">
        """,
        unsafe_allow_html=True,
    )

def show_page_links():
    """Displays a list of available pages as navigation links."""
    st.markdown("### Pages")
    pages = {
        "Home": "Home.py",
        "Predictions": "pages/Predictions.py",
        "Analytics": "pages/Analytics.py",
        # Add more pages as needed
    }
    for name, path in pages.items():
        st.markdown(f"- [{name}](/{path})")  # Streamlit reruns when clicked
