"""Analytics Page"""
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import get_dashboard_metrics, get_category_trends
from utils.chart_config import get_light_layout, get_pie_colors, COLORS

STATUS_LABELS = {
    'submitted': 'Submitted',
    'pending': 'Pending',
    'waiting_for_info': 'Waiting for Info',
    'processing': 'Processing',
    'completed': 'Completed',
    'cancelled': 'Cancelled'
}

def render_analytics():
    """Render the analytics dashboard."""
    st.header("Analytics & Insights")
    
    metrics = get_dashboard_metrics()
    
    if metrics['total_requests'] == 0:
        st.info("No data to analyze. Load demo data or submit requests to see analytics.")
        return
    
    # Key performance indicators
    st.subheader("Key Performance Indicators")
    
    total = metrics['total_requests']
    completed = metrics['completed_requests']
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Requests", total)
    
    with col2:
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    with col3:
        avg_time = metrics['avg_processing_time']
        time_display = f"{avg_time} min" if avg_time else "N/A"
        st.metric("Avg. Processing Time", time_display)
    
    with col4:
        pending = metrics['pending_requests']
        st.metric("Pending Requests", pending)
    
    st.write("")
    
    # Detailed charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Category breakdown
        st.subheader("Requests by Category")
        
        category_data = metrics['by_category']
        if category_data:
            df_cat = pd.DataFrame([
                {'Category': k, 'Count': v} 
                for k, v in sorted(category_data.items(), key=lambda x: x[1], reverse=True)
            ])
            fig = px.bar(df_cat, x='Count', y='Category',
                        color_discrete_sequence=[COLORS['primary']], orientation='h')
            fig.update_layout(
                **get_light_layout(title=None, height=350, showlegend=False),
                xaxis_title='Count',
                yaxis_title=''
            )
            fig.update_yaxes(tickfont=dict(size=10, color='#526581'))
            st.plotly_chart(fig, width="stretch", alt="Horizontal bar chart showing requests by category")
    
    with col2:
        # Status distribution
        st.subheader("Status Distribution")
        
        status_data = metrics['by_status']
        if status_data:
            df_status = pd.DataFrame([
                {'Status': STATUS_LABELS.get(k, k.replace('_', ' ').title()), 'Count': v} 
                for k, v in status_data.items()
            ])
            fig = px.pie(df_status, values='Count', names='Status')
            fig.update_traces(
                marker=dict(colors=get_pie_colors(df_status['Status'].tolist())),
                textfont=dict(size=12, color='#172B4D')
            )
            fig.update_layout(
                **get_light_layout(title=None, height=350),
                legend=dict(orientation='h', yanchor='bottom', y=-0.2, x=0.5, xanchor='center')
            )
            st.plotly_chart(fig, width="stretch", alt="Pie chart showing status distribution")
    
    st.write("")
    
    # Trends section
    st.subheader("Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Daily Request Volume (Last 30 Days)**")
        
        trends = get_category_trends(days=30)
        if trends:
            df_trends = pd.DataFrame(trends)
            df_trends['date'] = pd.to_datetime(df_trends['date'])
            
            # Group by date for total daily volume
            daily = df_trends.groupby('date')['count'].sum().reset_index()
            daily = daily.sort_values('date')
            
            fig = px.line(daily, x='date', y='count',
                         labels={'date': 'Date', 'count': 'Requests'})
            fig.update_traces(line_color=COLORS['primary'], line_width=2)
            fig.update_layout(
                **get_light_layout(title=None, height=300, showlegend=False),
                xaxis_title='Date',
                yaxis_title='Requests'
            )
            st.plotly_chart(fig, width="stretch", alt="Line chart showing daily request volume over last 30 days")
        else:
            st.info("No trend data available for the last 30 days.")
    
    with col2:
        st.write("**Category Trends Over Time**")
        
        if trends:
            df_trends = pd.DataFrame(trends)
            df_trends['date'] = pd.to_datetime(df_trends['date'])
            
            fig = px.line(df_trends, x='date', y='count', color='category',
                         labels={'date': 'Date', 'count': 'Requests', 'category': 'Category'},
                         color_discrete_sequence=[COLORS['primary'], COLORS['teal'], COLORS['purple'], COLORS['amber'], COLORS['green']])
            fig.update_traces(line_width=2)
            fig.update_layout(
                **get_light_layout(title=None, height=300),
                xaxis_title='Date',
                yaxis_title='Requests'
            )
            st.plotly_chart(fig, width="stretch", alt="Line chart showing category trends over time")
        else:
            st.info("No trend data available.")