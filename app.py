"""
CareFlow AI - Main Application
A healthcare operations platform for improved patient access and clinic workflows.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.database import (
    get_dashboard_metrics, load_demo_data, clear_demo_data,
    get_all_patient_requests, create_patient_request, update_request_status,
    get_all_staff, get_staff_workload, get_category_trends, get_status_distribution,
    get_patient_request, get_request_history, assign_staff_to_request, DB_PATH
)
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="CareFlow AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
        color: white;
        padding: 2rem 2rem 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 1rem 1rem;
    }
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 0.75rem;
        padding: 1.25rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .status-submitted { background: #fef3c7; color: #92400e; }
    .status-pending { background: #dbeafe; color: #1e40af; }
    .status-processing { background: #e0e7ff; color: #3730a3; }
    .status-completed { background: #d1fae5; color: #065f46; }
    .status-cancelled { background: #fee2e2; color: #991b1b; }
    
    .urgency-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 0.375rem;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .urgency-urgent { background: #fee2e2; color: #991b1b; }
    .urgency-soon { background: #fed7aa; color: #9a3412; }
    .urgency-routine { background: #d1fae5; color: #065f46; }
    
    .stButton button {
        border-radius: 0.5rem;
        font-weight: 500;
        padding: 0.5rem 1rem;
    }
    
    .stSidebar {
        background-color: #f1f5f9;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #64748b;
    }
    
    .empty-state h3 {
        font-size: 1.25rem;
        color: #475569;
        margin-bottom: 0.5rem;
    }
    
    .success-message {
        background: #d1fae5;
        color: #065f46;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #2563eb;
        padding: 1rem;
        border-radius: 0 0.5rem 0.5rem 0;
        margin-bottom: 1rem;
    }
    
    .warning-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0 0.5rem 0.5rem 0;
        margin-bottom: 1rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .request-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: box-shadow 0.2s;
    }
    
    .request-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    
    .request-card .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .request-card .patient-name {
        font-weight: 600;
        color: #1e293b;
    }
    
    .request-card .category {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 0.25rem;
    }
    
    .request-card .description {
        font-size: 0.85rem;
        color: #475569;
        margin-top: 0.5rem;
        line-height: 1.4;
    }
    
    .request-card .meta {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.5rem;
    }
    
    .tabs-container {
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: #eff6ff;
        color: #1e40af;
    }
    
    .staff-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .chart-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .chart-container h3 {
        font-size: 1.1rem;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #94a3b8;
        font-size: 0.85rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    .demo-banner {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

def status_badge(status):
    """Render a status badge."""
    css_class = f"status-{status}"
    label = status.replace('_', ' ').title()
    return f'<span class="status-badge {css_class}">{label}</span>'

def urgency_badge(urgency):
    """Render an urgency badge."""
    css_class = f"urgency-{urgency.lower()}"
    return f'<span class="urgency-badge {css_class}">{urgency}</span>'

def get_status_display(status):
    """Convert status to display format."""
    mapping = {
        'submitted': 'Submitted',
        'pending': 'Pending',
        'processing': 'Processing',
        'completed': 'Completed',
        'cancelled': 'Cancelled'
    }
    return mapping.get(status, status.title())

def get_status_color(status):
    """Get color for status."""
    colors = {
        'submitted': '#f59e0b',
        'pending': '#3b82f6',
        'processing': '#8b5cf6',
        'completed': '#10b981',
        'cancelled': '#ef4444'
    }
    return colors.get(status, '#6b7280')

def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0 1.5rem 0;">
            <h1 style="font-size: 1.5rem; color: #1e3a5f; margin-bottom: 0.25rem;">CareFlow AI</h1>
            <p style="font-size: 0.85rem; color: #64748b; margin-bottom: 0;">Healthcare Access & Clinic Operations</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["Overview", "Patient Portal", "Patient Requests", "Clinic Operations", 
             "Accessibility Assistant", "Analytics", "About & Responsible AI"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Demo data section
        st.markdown("### Demo Data")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Load Demo Data", use_container_width=True):
                result = load_demo_data()
                st.success(result['message'])
                st.rerun()
        with col2:
            if st.button("Clear Data", use_container_width=True):
                clear_demo_data()
                st.success("All data cleared")
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        metrics = get_dashboard_metrics()
        st.markdown("### Quick Stats")
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 0.5rem; border: 1px solid #e2e8f0;">
            <div style="font-size: 0.8rem; color: #64748b;">Total Requests</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #1e293b;">{metrics['total_requests']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    return page

def render_header():
    """Render the main header."""
    st.markdown("""
    <div class="main-header">
        <h1>CareFlow AI</h1>
        <p>Better Access. Smarter Clinics. Faster Workflows.</p>
    </div>
    """, unsafe_allow_html=True)

# Page functions will be imported from pages/ module
from pages.overview import render_overview
from pages.patient_portal import render_patient_portal
from pages.patient_requests import render_patient_requests
from pages.clinic_operations import render_clinic_operations
from pages.accessibility import render_accessibility_assistant
from pages.analytics import render_analytics
from pages.about import render_about

def main():
    """Main application entry point."""
    page = render_sidebar()
    render_header()
    
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
    elif page == "Analytics":
        render_analytics()
    elif page == "About & Responsible AI":
        render_about()

if __name__ == "__main__":
    main()