"""
CareFlow AI - Main Application
A healthcare operations platform for improved patient access and clinic workflows.
"""
import streamlit as st
from utils.database import (
    get_dashboard_metrics, load_demo_data, clear_demo_data
)

# Page configuration
st.set_page_config(
    page_title="CareFlow AI",
    page_icon=":material/health_and_safety:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache metrics for performance
@st.cache_data(ttl=30, show_spinner=False)
def cached_metrics():
    return get_dashboard_metrics()

def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.title("CareFlow AI")
        st.caption("Healthcare Access & Clinic Operations")
        
        st.divider()
        
        page = st.radio(
            "Navigation",
            ["Overview", "Patient Portal", "Patient Requests", "Clinic Operations", 
             "Accessibility Assistant", "AI Intelligence", "Analytics", "About & Responsible AI"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Demo data section
        st.subheader("Demo data")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Load Demo data", width="stretch"):
                result = load_demo_data()
                st.success(result['message'])
                cached_metrics.clear()
                st.rerun()
        with col2:
            if st.button("Clear data", width="stretch"):
                clear_demo_data()
                st.success("All data cleared")
                cached_metrics.clear()
                st.rerun()
        
        st.divider()
        
        # Quick stats
        metrics = cached_metrics()
        st.subheader("Quick Stats")
        st.metric("Total Requests", metrics['total_requests'])
        
    return page

# Import page functions from pages/ module
from pages.overview import render_overview
from pages.patient_portal import render_patient_portal
from pages.patient_requests import render_patient_requests
from pages.clinic_operations import render_clinic_operations
from pages.accessibility import render_accessibility_assistant
from pages.ai_intelligence import render_ai_intelligence
from pages.analytics import render_analytics
from pages.about import render_about

def main():
    """Main application entry point."""
    page = render_sidebar()
    
    # Allow hero buttons to override navigation
    if "selected_page" in st.session_state:
        page = st.session_state.selected_page
        del st.session_state.selected_page
    
    if page == "Overview":
        render_overview()
    elif page == "Patient Portal":
        render_patient_portal()
    elif page == "Patient Requests":
        render_patient_requests()
    elif page == "Clinic Operations":
        render_clinic_operations()
    elif page == "Accessibility Assistant":
        render_accessibility_assistant()
    elif page == "AI Intelligence":
        render_ai_intelligence()
    elif page == "Analytics":
        render_analytics()
    elif page == "About & Responsible AI":
        render_about()

if __name__ == "__main__":
    main()