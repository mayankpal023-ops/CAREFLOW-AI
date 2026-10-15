"""
CareFlow AI - Shared Plotly Chart Configuration
Ensures consistent light theme across all charts.
"""
import plotly.graph_objects as go

# Color palette
COLORS = {
    'primary': '#2563EB',
    'teal': '#0F766E',
    'purple': '#7C3AED',
    'amber': '#D97706',
    'green': '#059669',
    'red': '#DC2626',
    'blue_light': '#3B82F6',
    'gray': '#6B7280',
    'navy': '#142B4A',
}

STATUS_COLORS = {
    'Submitted': '#D97706',
    'Pending': '#3B82F6',
    'Waiting for Info': '#7C3AED',
    'Processing': '#0F766E',
    'Completed': '#059669',
    'Cancelled': '#DC2626',
    'Waiting_for_Info': '#7C3AED',
}

def get_light_layout(title=None, height=350, showlegend=True):
    """Get a consistent light layout DICT for all charts.
    
    Returns a plain dict that can be unpacked with ** in update_layout().
    This fixes the TypeError: argument after ** must be a mapping, not Layout.
    
    Note: 'legend' is NOT included in this base layout — it is passed separately
    when needed via the fig.update_layout(legend=...) keyword argument.
    """
    return {
        'title': {
            'text': title or '',
            'font': {'size': 16, 'color': '#172B4D', 'family': 'Inter, sans-serif'},
            'x': 0.05,
        },
        'plot_bgcolor': '#FFFFFF',
        'paper_bgcolor': '#FFFFFF',
        'font': {
            'family': 'Inter, sans-serif',
            'color': '#172B4D',
            'size': 12,
        },
        'margin': {'l': 50, 'r': 30, 't': 60, 'b': 50},
        'showlegend': showlegend,
        # 'legend' key intentionally omitted — passed separately when needed
        'xaxis': {
            'gridcolor': '#F1F5F9',
            'linecolor': '#E2E8F0',
            'tickfont': {'size': 11, 'color': '#526581'},
            'title_font': {'size': 13, 'color': '#172B4D'},
        },
        'yaxis': {
            'gridcolor': '#F1F5F9',
            'linecolor': '#E2E8F0',
            'tickfont': {'size': 11, 'color': '#526581'},
            'title_font': {'size': 13, 'color': '#172B4D'},
        },
        'height': height,
    }

def get_pie_colors(statuses):
    """Get consistent pie chart colors."""
    return [STATUS_COLORS.get(s, '#6B7280') for s in statuses]