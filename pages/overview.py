"""Overview Dashboard Page"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import get_dashboard_metrics
from utils.chart_config import get_light_layout, get_pie_colors, COLORS

STATUS_LABELS = {
    'submitted': 'New',
    'pending': 'Pending',
    'waiting_for_info': 'Waiting for Info',
    'processing': 'In Progress',
    'completed': 'Resolved',
    'cancelled': 'Cancelled'
}

STATUS_COLORS_MAP = {
    'New': '#D97706',
    'Pending': '#3B82F6',
    'Waiting for Info': '#7C3AED',
    'In Progress': '#0F766E',
    'Resolved': '#059669',
    'Cancelled': '#DC2626',
}

def render_overview():
    """Render the main overview dashboard with hero section."""
    
    # Hero Section
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #142B4A 0%, #2563EB 50%, #4F46E5 100%); 
                    border-radius: 1rem; padding: 2.5rem 2rem; margin-bottom: 2rem; color: white;">
            <div style="display: inline-block; background: rgba(255,255,255,0.15); padding: 0.35rem 1rem; 
                        border-radius: 9999px; font-size: 0.75rem; font-weight: 600; 
                        letter-spacing: 0.08em; margin-bottom: 1rem;">
                AI-POWERED HEALTHCARE OPERATIONS
            </div>
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; color: white; line-height: 1.2;">
                AI-Powered Healthcare Access &amp; Clinic Workflow Assistant
            </h1>
            <p style="font-size: 1.15rem; opacity: 0.9; margin-bottom: 0.5rem; color: white; font-weight: 500;">
                Better Access. Smarter Clinics. Faster Workflows.
            </p>
            <p style="font-size: 0.95rem; opacity: 0.8; margin-bottom: 1.5rem; color: rgba(255,255,255,0.85);">
                Helping patients navigate healthcare services while empowering clinic teams with intelligent administrative workflows.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Hero action buttons - use st.session_state for navigation
        hero_col1, hero_col2 = st.columns(2)
        with hero_col1:
            if st.button("Submit a Patient Request", type="primary", width="stretch", key="hero_portal_btn"):
                st.session_state.selected_page = "Patient Portal"
                st.rerun()
        with hero_col2:
            if st.button("Open Clinic Operations", width="stretch", key="hero_clinic_btn"):
                st.session_state.selected_page = "Clinic Operations"
                st.rerun()
    
    metrics = get_dashboard_metrics()
    
    if metrics['total_requests'] == 0:
        with st.container(border=True):
            st.info("No patient requests yet. Load demo data to explore the dashboard or submit a request from the Patient Portal.", title="Getting Started")
        return
    
    # Metric Cards Row 1
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Requests", metrics['total_requests'])
    with col2:
        st.metric("New Requests", metrics.get('pending_requests', 0))
    with col3:
        st.metric("In Progress", metrics.get('processing_requests', 0))
    with col4:
        st.metric("Waiting for Info", metrics.get('waiting_for_info', 0))
    with col5:
        st.metric("Resolved", metrics.get('completed_requests', 0))
    
    st.write("")
    
    # Metric Cards Row 2
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_time = metrics.get('avg_processing_time')
        time_display = f"{avg_time} min" if avg_time else "N/A"
        st.metric("Avg. Processing Time", time_display)
    with col2:
        old_unresolved = metrics.get('old_unresolved', 0)
        st.metric("Old Unresolved (>24h)", old_unresolved)
    with col3:
        total = metrics['total_requests']
        completed = metrics.get('completed_requests', 0)
        completion_rate = f"{(completed / total * 100):.1f}%" if total > 0 else "0%"
        st.metric("Completion Rate", completion_rate)
    
    st.write("")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Requests by Status")
        status_data = metrics['by_status']
        if status_data:
            df_status = pd.DataFrame([
                {'Status': STATUS_LABELS.get(k, k.replace('_', ' ').title()), 'Count': v} 
                for k, v in status_data.items()
            ])
            fig = px.pie(df_status, values='Count', names='Status', hole=0.4)
            fig.update_traces(
                marker=dict(colors=[STATUS_COLORS_MAP.get(s, '#6B7280') for s in df_status['Status']]),
                textfont=dict(size=12, color='#172B4D'),
                textposition='inside'
            )
            fig.update_layout(
                **get_light_layout(title=None, height=300, showlegend=True),
                legend=dict(orientation='h', yanchor='bottom', y=-0.2, x=0.5, xanchor='center')
            )
            st.plotly_chart(fig, width="stretch", alt="Pie chart showing requests by status")
    
    with col2:
        st.subheader("Requests by Category")
        category_data = metrics['by_category']
        if category_data:
            df_cat = pd.DataFrame([
                {'Category': k, 'Count': v} 
                for k, v in category_data.items()
            ])
            fig = px.bar(df_cat, x='Count', y='Category',
                        color_discrete_sequence=[COLORS['primary']], orientation='h')
            fig.update_layout(
                **get_light_layout(title=None, height=300, showlegend=False),
                xaxis_title='Count',
                yaxis_title=''
            )
            fig.update_yaxes(tickfont=dict(size=10, color='#526581'))
            st.plotly_chart(fig, width="stretch", alt="Bar chart showing requests by category")
    
    st.write("")
    
    # Recent requests and bottlenecks
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Recent Requests")
        recent = metrics['recent_requests']
        if recent:
            for req in recent[:5]:
                status_label = STATUS_LABELS.get(req['status'], req['status'].replace('_', ' ').title())
                status_color = STATUS_COLORS_MAP.get(status_label, '#6B7280')
                with st.container(border=True):
                    st.write(f"**:{status_color}[{req['patient_name']}]** — {req['category']}")
                    st.caption(f"Status: {status_label} | Urgency: {req['urgency']} | Submitted: {req['created_at'][:10]}")
        else:
            st.info("No recent activity")
    
    with col2:
        st.subheader("Workflow Bottlenecks")
        
        # Show bottleneck alerts
        urgent_count = 0
        for req in metrics['recent_requests']:
            if req['urgency'] == 'Urgent' and req['status'] not in ['completed', 'cancelled']:
                urgent_count += 1
                st.warning(f"**Urgent:** {req['patient_name']} — {req['category']}")
        
        if metrics.get('old_unresolved', 0) > 0:
            st.warning(f"**Backlog:** {metrics['old_unresolved']} request(s) unresolved for over 24 hours")
        
        if metrics.get('processing_requests', 0) > 3:
            st.warning(f"**High Load:** {metrics['processing_requests']} requests currently processing")
        
        if urgent_count == 0 and metrics.get('old_unresolved', 0) == 0 and metrics.get('processing_requests', 0) <= 3:
            st.success("No critical bottlenecks detected")
    
    st.write("")
    
    # AI-Generated Operational Insights
    st.subheader("AI-Generated Operational Insights")
    insights = _generate_operational_insights(metrics)
    for insight in insights:
        with st.container(border=True):
            st.write(f"**{insight['icon']} {insight['title']}**")
            st.caption(insight['description'])

def _generate_operational_insights(metrics):
    """Generate AI-style operational insights from database metrics."""
    insights = []
    
    # Completion rate insight
    total = metrics['total_requests']
    completed = metrics.get('completed_requests', 0)
    if total > 0:
        rate = completed / total * 100
        if rate >= 70:
            insights.append({
                'icon': ":material/check_circle:",
                'title': 'Healthy Completion Rate',
                'description': f'{rate:.1f}% of requests are resolved. The clinic is maintaining good throughput.'
            })
        elif rate >= 40:
            insights.append({
                'icon': ":material/trending_up:",
                'title': 'Moderate Completion Rate',
                'description': f'{rate:.1f}% of requests are resolved. Consider reviewing bottlenecks to improve throughput.'
            })
        else:
            insights.append({
                'icon': ":material/alert:",
                'title': 'Low Completion Rate',
                'description': f'Only {rate:.1f}% of requests are resolved. Immediate attention recommended to clear backlog.'
            })
    
    # Wait time insight
    avg_time = metrics.get('avg_processing_time')
    if avg_time is not None:
        if avg_time < 60:
            insights.append({
                'icon': ":material/speed:",
                'title': 'Fast Processing',
                'description': f'Average processing time is {avg_time} minutes, which is excellent for patient satisfaction.'
            })
        elif avg_time < 120:
            insights.append({
                'icon': ":material/schedule:",
                'title': 'Moderate Processing Time',
                'description': f'Average processing time is {avg_time} minutes. Monitor for improvement opportunities.'
            })
        else:
            insights.append({
                'icon': ":material/timer_off:",
                'title': 'Slow Processing',
                'description': f'Average processing time is {avg_time} minutes. Review workflow for bottlenecks.'
            })
    
    # Waiting for info insight
    waiting = metrics.get('waiting_for_info', 0)
    if waiting > 0:
        insights.append({
            'icon': ":material/question_mark:",
            'title': 'Information Pending',
            'description': f'{waiting} request(s) are waiting for additional information from patients. Follow up to reduce delays.'
        })
    
    # Category insight
    by_category = metrics.get('by_category', {})
    if by_category:
        max_cat = max(by_category, key=by_category.get)
        insights.append({
            'icon': ":material/category:",
            'title': 'Top Category',
            'description': f'"{max_cat}" has the most requests ({by_category[max_cat]}). Consider allocating additional resources.'
        })
    
    if not insights:
        insights.append({
            'icon': ":material/info:",
            'title': 'No Insights Yet',
            'description': 'Submit more requests to generate operational insights.'
        })
    
    return insights[:4]