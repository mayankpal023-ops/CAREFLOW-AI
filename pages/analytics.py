"""Analytics Page"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import get_dashboard_metrics, get_category_trends, get_status_distribution

def render_analytics():
    """Render the analytics dashboard."""
    st.markdown('<p class="section-title">Analytics & Insights</p>', unsafe_allow_html=True)
    
    metrics = get_dashboard_metrics()
    
    if metrics['total_requests'] == 0:
        st.markdown("""
        <div class="empty-state">
            <h3>No data to analyze</h3>
            <p>Load demo data or submit requests to see analytics.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Key performance indicators
    st.markdown("### Key Performance Indicators")
    
    total = metrics['total_requests']
    completed = metrics['completed_requests']
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Requests</h3>
            <div class="value">{total}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Completion Rate</h3>
            <div class="value">{completion_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_time = metrics['avg_processing_time']
        time_display = f"{avg_time} min" if avg_time else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Avg. Processing Time</h3>
            <div class="value" style="font-size: 1.5rem;">{time_display}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        pending = metrics['pending_requests']
        st.markdown(f"""
        <div class="metric-card">
            <h3>Pending Requests</h3>
            <div class="value" style="color: #f59e0b;">{pending}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Category breakdown
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3>Requests by Category</h3>', unsafe_allow_html=True)
        
        category_data = metrics['by_category']
        if category_data:
            df_cat = pd.DataFrame([
                {'Category': k, 'Count': v} 
                for k, v in sorted(category_data.items(), key=lambda x: x[1], reverse=True)
            ])
            fig = px.bar(df_cat, x='Category', y='Count',
                        color_discrete_sequence=['#2563eb'])
            fig.update_layout(xaxis_tickangle=-45, height=350)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Status distribution
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3>Status Distribution</h3>', unsafe_allow_html=True)
        
        status_data = metrics['by_status']
        if status_data:
            df_status = pd.DataFrame([
                {'Status': k.replace('_', ' ').title(), 'Count': v} 
                for k, v in status_data.items()
            ])
            colors = {'Submitted': '#f59e0b', 'Pending': '#3b82f6', 
                     'Processing': '#8b5cf6', 'Completed': '#10b981', 'Cancelled': '#ef4444'}
            fig = px.pie(df_status, values='Count', names='Status',
                        color='Status', color_discrete_map=colors)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Trends section
    st.markdown("### Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3>Daily Request Volume (Last 30 Days)</h3>', unsafe_allow_html=True)
        
        trends = get_category_trends(days=30)
        if trends:
            df_trends = pd.DataFrame(trends)
            df_trends['date'] = pd.to_datetime(df_trends['date'])
            
            # Group by date for total daily volume
            daily = df_trends.groupby('date')['count'].sum().reset_index()
            daily = daily.sort_values('date')
            
            fig = px.line(daily, x='date', y='count',
                         labels={'date': 'Date', 'count': 'Requests'})
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trend data available for the last 30 days.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3>Category Trends Over Time</h3>', unsafe_allow_html=True)
        
        if trends:
            df_trends = pd.DataFrame(trends)
            df_trends['date'] = pd.to_datetime(df_trends['date'])
            
            fig = px.line(df_trends, x='date', y='count', color='category',
                         labels={'date': 'Date', 'count': 'Requests', 'category': 'Category'})
            fig.update_layout(height=300, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trend data available.")
        st.markdown('</div>', unsafe_allow_html=True)