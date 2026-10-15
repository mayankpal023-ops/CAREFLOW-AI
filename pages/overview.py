"""Overview Dashboard Page"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import get_dashboard_metrics

def render_overview():
    """Render the main overview dashboard."""
    st.markdown('<p class="section-title">Operational Overview</p>', unsafe_allow_html=True)
    
    metrics = get_dashboard_metrics()
    
    if metrics['total_requests'] == 0:
        st.markdown("""
        <div class="empty-state">
            <h3>Welcome to CareFlow AI</h3>
            <p>No patient requests yet. Load demo data or submit requests from the Patient Portal.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Metric cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Requests</h3>
            <div class="value">{metrics['total_requests']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Pending</h3>
            <div class="value" style="color: #3b82f6;">{metrics['pending_requests']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Processing</h3>
            <div class="value" style="color: #8b5cf6;">{metrics['processing_requests']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Completed</h3>
            <div class="value" style="color: #10b981;">{metrics['completed_requests']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        avg_time = metrics['avg_processing_time']
        time_display = f"{avg_time} min" if avg_time else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Avg. Processing Time</h3>
            <div class="value" style="font-size: 1.5rem;">{time_display}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        # Status distribution pie chart
        status_data = metrics['by_status']
        if status_data:
            df_status = pd.DataFrame([
                {'Status': k.replace('_', ' ').title(), 'Count': v} 
                for k, v in status_data.items()
            ])
            fig = px.pie(df_status, values='Count', names='Status', 
                        title='Requests by Status',
                        color_discrete_sequence=['#f59e0b', '#3b82f6', '#8b5cf6', '#10b981', '#ef4444'])
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Category bar chart
        category_data = metrics['by_category']
        if category_data:
            df_cat = pd.DataFrame([
                {'Category': k, 'Count': v} 
                for k, v in category_data.items()
            ])
            fig = px.bar(df_cat, x='Category', y='Count',
                        title='Requests by Category',
                        color_discrete_sequence=['#2563eb'])
            fig.update_layout(height=300, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent requests and bottlenecks
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">Recent Activity</p>', unsafe_allow_html=True)
        recent = metrics['recent_requests']
        if recent:
            for req in recent[:5]:
                status_colors = {
                    'submitted': '#f59e0b', 'pending': '#3b82f6', 
                    'processing': '#8b5cf6', 'completed': '#10b981'
                }
                color = status_colors.get(req['status'], '#6b7280')
                st.markdown(f"""
                <div class="request-card">
                    <div class="header">
                        <span class="patient-name">{req['patient_name']}</span>
                        <span style="color: {color}; font-weight: 600; font-size: 0.85rem;">
                            {req['status'].replace('_', ' ').title()}
                        </span>
                    </div>
                    <div class="category">{req['category']}</div>
                    <div class="meta">Submitted: {req['created_at'][:10]}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent activity")
    
    with col2:
        st.markdown('<p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem;">Bottleneck Alerts</p>', unsafe_allow_html=True)
        
        # Show bottleneck alerts
        urgent_count = 0
        for req in metrics['recent_requests']:
            if req['urgency'] == 'Urgent' and req['status'] not in ['completed', 'cancelled']:
                urgent_count += 1
                st.markdown(f"""
                <div class="warning-box" style="padding: 0.75rem;">
                    <strong>Urgent:</strong> {req['patient_name']} - {req['category']}
                </div>
                """, unsafe_allow_html=True)
        
        if metrics['processing_requests'] > 3:
            st.markdown(f"""
            <div class="warning-box" style="padding: 0.75rem;">
                <strong>High Load:</strong> {metrics['processing_requests']} requests currently processing
            </div>
            """, unsafe_allow_html=True)
        
        if urgent_count == 0 and metrics['processing_requests'] <= 3:
            st.markdown("""
            <div class="success-message">
                No critical bottlenecks detected
            </div>
            """, unsafe_allow_html=True)